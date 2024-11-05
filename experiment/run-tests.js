const { promptLLMOpenAI } = require("./gpt");
const fs = require('fs');
const path = require('path');
let testCases = require('./test-cases.json');

const { execSync } = require('child_process'); // Import execSync correctly

const additionalTestCases = fs.readdirSync('test-cases').map(file => {
    const filePath = path.join('test-cases', file);
    const name = file.split('.')[0];
    const prompt = fs.readFileSync(filePath, 'utf-8');
    return { name, prompt };
});
testCases = testCases.concat(additionalTestCases);

async function evaluate(version) {
    const versionFolder = `testResults/v${version}`;
    const venvPath = path.join('testResults', 'venv', 'bin', 'python');
    const testFiles = fs.readdirSync(versionFolder).filter(file => file.endsWith('.py'));

    let correctCount = 0;

    for (const testFile of testFiles) {
        const filePath = path.join(versionFolder, testFile);

        try {
            const output = execSync(`${venvPath} ${filePath}`, { encoding: 'utf-8' });
            const prompt = `Given the following program output:\n\n${output}\n\nDoes this output indicate the program works correctly? Respond with either "correct" or "incorrect" and nothing else.`;

            const evaluation = await promptLLMOpenAI(prompt, 'gpt-4o').then(res => res.trim());

            if (evaluation === 'correct') {
                correctCount += 1;
            }
        } catch (error) {
            console.error(`Error executing file ${testFile}: ${error.message}`);
        }
    }

    // Calculate the percentage of correct programs
    const totalTests = testFiles.length;
    return (correctCount / totalTests) * 100;
}


async function main(versions = [4], isSelfEvaluation = false) {
    const scores = {};
    for (const version of versions) {
        const metaPromptPath = `../v${version}.txt`;
        if (!fs.existsSync(metaPromptPath)) {
            console.log(`Prompt file for version v${version} not found at ${metaPromptPath}`);
            continue;
        }

        const metaPrompt = fs.readFileSync(metaPromptPath, 'utf-8');
        const versionFolder = `testResults/v${version}`;

        if (!fs.existsSync(versionFolder)) {
            fs.mkdirSync(versionFolder, { recursive: true });
        }

        const batchSize = 10;
        for (let i = 0; i < testCases.length; i += batchSize) {
            const batch = testCases.slice(i, i + batchSize).map(async (testCase, index) => {
                const prompt = `\
${testCase.prompt}
Generate the python code without any other wrapping elements or text.
You can read the authentication token from the environment variable "JINA_API_KEY".
Also no code fencing like \`\`\`python is allowed
${metaPrompt}`;

                const response = await promptLLMOpenAI(prompt, 'gpt-4o');
                const filePath = path.join(versionFolder, `${i + index}-${testCase.name}.py`);
                fs.writeFileSync(filePath, response);
                console.log(`Saved result for test case "${testCase.name}" in ${filePath}`);
            });
            await Promise.all(batch);
        }
        scores[version] = await evaluate(version);
        console.log('scores so far', scores);
    }
}

main([0, 1, 2, 3, 4], true);
