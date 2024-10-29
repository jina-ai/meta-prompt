const fs = require('fs');
const path = require('path');
const { promptLLMOpenAI } = require("./gpt");

const htmlSnippetDir = './html-snippets';  // Directory containing HTML snippet files
const outputFile = 'index-gen.txt';

// Delete the output file if it exists
if (fs.existsSync(outputFile)) {
    fs.unlinkSync(outputFile);
    console.log(`${outputFile} deleted successfully.`);
}

// Function to read HTML files from the directory
const getHtmlFiles = (dir) => {
    return fs.readdirSync(dir).filter(file => file.endsWith('.html'));
};

// Process each HTML file
async function processHtmlSnippets() {
    const htmlFiles = getHtmlFiles(htmlSnippetDir);

    for (const fileName of htmlFiles) {
        const filePath = path.join(htmlSnippetDir, fileName);
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const productName = path.basename(fileName, '.html');

        // Generate prompt using HTML content directly
        const prompt = `\
#### start file content
${fileContent}
#### end file content

Generate the most sophisticated example request possible in python format without imports. Also generate the example response of the request.
For all attributes make a comment with the following requirements:
- The comment must be concise
- The comment must indicate if the attribute is optional or required
- The comment must indicate the default value
- The comment must provide an exhaustive list of all possible values for the attribute even if this means the comment is long. Nothing like etc. or similar is allowed.

Note:
you must only generate output in the following format:
## request
endpoint = f"https://..." # < comment here >
... # < comment here >
...
response = requests. ... # < comment here >
## response
... # < comment here >
...`;

        // Call the LLM API to get the response
        const response = await promptLLMOpenAI(prompt, 'gpt-4o');

        // Append the result to the output file
        fs.appendFileSync(outputFile, `\n# ${productName}\n${response}`);
    }

    console.log(`All HTML files processed and saved to ${outputFile}`);
}

// Run the function
processHtmlSnippets();
