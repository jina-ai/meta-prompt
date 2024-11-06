const { AzureOpenAI } = require("openai");

// Load the .env file if it exists
const dotenv = require("dotenv");
dotenv.config();

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINTS"] || "<endpoint>";
const apiKey = process.env["AZURE_OPENAI_API_KEYS"] || "<api key>";
const apiVersion = "2024-05-01-preview";
const deployment = "gpt-4o"; //This must match your deployment name.
require("dotenv/config");

async function promptLLMOpenAI(prompt, modelName) {
  console.log('\x1b[34m%s\x1b[0m', prompt);
  for (let i = 0; i < 5; i++) {
    try {
      console.log('endpoint', endpoint)
      console.log('apiKey', apiKey)
      const client = new AzureOpenAI({ endpoint, apiKey, apiVersion, deployment });
      const result = await client.chat.completions.create({
        messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt }
        ],
        model: modelName,
      });

      const content = result.choices[0].message.content
      console.log('\x1b[32m%s\x1b[0m', content);

      return content;
    } catch (e) {
      console.log('error', e, `retrying ${i} after 10 seconds`)
      await new Promise(resolve => setTimeout(resolve, 10000));
    }
  }
}

module.exports = { promptLLMOpenAI };
