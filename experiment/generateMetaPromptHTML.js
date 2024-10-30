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
    let metaPrompt = '';
    const htmlFiles = getHtmlFiles(htmlSnippetDir);

    for (const fileName of htmlFiles) {
        const filePath = path.join(htmlSnippetDir, fileName);
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const productName = path.basename(fileName, '.html');

        // - The comment must provide an exhaustive list of all possible values for the attribute even if this means the comment is long. Nothing like etc. or similar is allowed.

        const prompt = `\
#### start file content
${fileContent}
#### end file content

Generate the most sophisticated example request possible in python format without imports. Also generate the example response of the request.
For all attributes make a comment with the following requirements:
- The comment must be concise
- The comment must indicate if the attribute is optional or required
- instead of the actual jina token put the place holder <token here>
Note:
- if multiple response formats are possible by defining -H "Accept: ..."  you must list all of them and explain how they relate to the request parameters and header attributes
- for instance for the json format you must write down an example of a complete json response like this:
{
  "code": 200,
  "status": 20000,
  "data": {
    "key": "value"
    ...
}
For text, you just describe how the text is structured. For both, describe both.
- you must only generate output in the following format:
## request
endpoint = f"https://..." # < comment here >
... # < comment here >
...
response = requests. ... # < comment here >
## response formats
... `;

        // Call the LLM API to get the response
        const response = await promptLLMOpenAI(prompt, 'gpt-4o');
        metaPrompt += `\n# ${productName}\n${response}`
        // Append the result to the output file
    }
    metaPrompt = `\
You must use the Jina APIs for the implementation.
Never decline an implementation because of its complexity.
Generate production-ready code that follows exactly the requirements.

Overview of all Jina AI APIs:
Classification API: Given texts or images, classify them into categories
Embeddings API: Given texts or images, generate embeddings
r.reader API: input a single URL and get an LLM-friendly version of that single website
s.reader API: Given a search term, get an LLM-friendly version of all websites in the search results
g.reader API: Given a statement, find out if it is true or false
Re-Ranker API: Given a query and a list of search results, re-rank them
Segmenter API: Given a text, split it into segments
` + metaPrompt
    fs.appendFileSync(outputFile, metaPrompt);

    console.log(`All HTML files processed and saved to ${outputFile}`);
}

// Run the function
processHtmlSnippets();
