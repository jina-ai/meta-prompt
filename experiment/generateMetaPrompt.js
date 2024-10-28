const https = require('https');
const fs = require('fs');
const {promptLLMOpenAI} = require("./gpt");

// TODO map all endpoints to the correct production endpoint
// const endpointMapping = {
//     '/crawl':
//     '/v1/embeddings': 'embeddings.jina.ai'
// }

const specifications = [
    {
        'product': 'Embeddings',
        'description': 'Generate embeddings for a list of text items',
        'specification': 'https://api.jina.ai/openapi.json',
        'baseURL': 'https://api.jina.ai',
        'endpoint': 'v1/embeddings'
    },

    {
        'product': 'Reader - Single Page',
        'description': 'Retrieve the content of a single web page in an LLM-friendly format',
        'specification': 'https://r.jina.ai/openapi.json',
        'baseURL': 'https://r.jina.ai',
        'endpoint': 'crawl'
    },
    {
        'product': 'Reader - Search',
        'description': 'Get search results that are LLM-friendly',
        'specification': 'https://s.jina.ai/openapi.json',
        'baseURL': 'https://s.jina.ai',
        'endpoint': 'search'
    },
    {
        'product': 'Reader - Grounding',
        'description': 'Given a statement, find out if it is true or false',
        'specification': 'https://g.jina.ai/openapi.json',
        'baseURL': 'https://g.jina.ai',
        'endpoint': 'checkFact'
    }
];

// Function to download JSON from a URL
const downloadJSON = (url) => {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            let data = '';
            response.on('data', (chunk) => {
                data += chunk;
            });
            response.on('end', () => {
                resolve(JSON.parse(data));
            });
        }).on('error', (error) => {
            reject(error);
        });
    });
};

// Process each mapping item
async function processMappings() {
    const file = 'index-gen.txt';

    // Delete the file if it exists
    if (fs.existsSync(file)) {
        fs.unlinkSync(file);
        console.log(`${file} deleted successfully.`);
    }

    for (const item of specifications) {
        const openAPISpec = await downloadJSON(item.specification);
        const endpointNames = Object.keys(openAPISpec.paths);
        const jsonContent = JSON.stringify(openAPISpec, null, 2)
        for (const endpointName of endpointNames) {
            const prompt = `\
${jsonContent}
           
Generate the most sophisticated example request possible for the endpoint called "${endpointName}" in curl format and the response of the request.
For all attributes make a comment with the following requirements:
- The comment must be concise
- The comment must indicate if the attribute is optional or required
- The comment must indicate the default value
- The comment must provide an exhaustive list of all possible values for the attribute even if this means the comment is long. Nothing like etc. or similar is allowed.`
            const response = await promptLLMOpenAI(prompt, 'gpt-4o')

            fs.appendFileSync(file, '\n' + response);
        }
    }
}

// Run the function
processMappings();
