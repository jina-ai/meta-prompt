# Meta Prompt for Jina Search Foundation APIs

## Usage
- `curl docs.jina.ai` 
- Specific version: `curl docs.jina.ai/v1`
- Pipe into [`llm`](https://github.com/simonw/llm):
```bash
curl docs.jina.ai/v1 | llm -s 'grab all sentences from Hacker News, embed them, and visualize the results in a 2D UMAP with matplotlib' -m claude-3-sonnet
```

## Note
- Opening docs.jina.ai in a browser gives you a `text/html` response, but programmatic access gives you a clean `text/plain` response. This is due to the `user-agent` value.
- For browser JS `fetch` where you can't change the `user-agent` or in scenarios where you pretend to be a browser by `user-agent` spoofing, you can add 'accept': 'text/plain' to the header to force the `text/plain` response.

## Developer's Guide
- Upload your prompt to `v{x}.txt` in the repository root.
- Use `curl docs.jina.ai/v{x}` to fetch your prompt:
  - No need to include `.txt`; simply use `curl docs.jina.ai/v1`, `curl docs.jina.ai/v2`, `curl docs.jina.ai/v3`, etc.
  - By default, `curl docs.jina.ai` fetches the version defined in `default`
  
