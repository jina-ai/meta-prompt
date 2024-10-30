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

Generate the an example request that contains as many parameters, attributes, header fileds as possible in python format without imports. Also generate the example response of the request.
Make sure to include -H "Accept: application/json" in the request to get a json response.
Instead of the actual jina token put the place holder <token here>.
For all parameters, attributes, or header fileds make a comment with the following requirements:
- The comment must be concise
- The comment must indicate if the attribute is optional or required
Note:
- write down an example of a complete json response like this:
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
Never use placeholder data.
Always make JSON requests by including the header -H "Accept: application/json".

Overview of all Jina AI APIs:
Classification API: Given texts or images, classify them into categories
Embeddings API: Given texts or images, generate embeddings.
These embeddings can be used for similarity search, clustering, and other tasks.
r.reader API: Input a single website URL and get an LLM-friendly version of that single website.
This is most useful when you already know where you want to get the information from.
s.reader API: Given a search term, get an LLM-friendly version of all websites in the search results.
This is useful when you don't know where to get the information from, but you just know what you are looking for.
g.reader API: Given a statement, find out if it is true or false.
This is useful for fact-checking, fake news detection, and general knowledge verification.
Re-Ranker API: Given a query and a list of search results, re-rank them.
This is useful for improving the relevance of search results.
Segmenter API: Given a text e.g. the output from r.reader or s.reader, split it into segments.
This is useful for breaking down long texts into smaller, more manageable parts.
Usually this is done to get the chunks that are passed to the embeddings API.

Note:
For every request to any of the Jina APIs, you must include the header -H "Accept: application/json" to specify that the response should be in JSON format.
It is not JSON by default. So you must explicitly specify it in the request headers.
` + metaPrompt
    fs.appendFileSync(outputFile, metaPrompt);

    console.log(`All HTML files processed and saved to ${outputFile}`);
}

// Run the function
processHtmlSnippets();
