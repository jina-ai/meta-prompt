const {promptLLMOpenAI} = require("./gpt");
const fs = require('fs');

const testCases = require('./test-cases.json');
const metaPrompt = fs.readFileSync('index-gen.txt', 'utf-8');

async function main() {
    testCases.forEach(async (testCase, index) => {
        const prompt = `\
${testCase.prompt}
Generate the python code without any other wrapping elements or text.
Also no code fencing like \`\`\`python is allowed
I have my jina token as env var: JINA_API_KEY
${metaPrompt}`
        const response = await promptLLMOpenAI(prompt, 'gpt-4o');
        fs.writeFileSync(`testResults/${index}-${testCase.name}.py`, response)
    });
}

main()