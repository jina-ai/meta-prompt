# Meta Prompt for Jina Search Foundation APIs

## Usage

- `curl docs.jina.ai`
- Specific version: `curl docs.jina.ai/v1`
- Pipe into `llm`:
```bash
curl docs.jina.ai/v1 | llm -s 'grab all sentence from hackernews and embed them and visualize the results in a 2d umap with matplotlib' -m claude-3-sonnet
```

## Developer's Guide

- Upload your prompt to `v{x}.txt` in the repository root.
- Use `curl docs.jina.ai/v{x}` to fetch your prompt:
  - No need to include `.txt`; simply use `curl docs.jina.ai/v1`, `curl docs.jina.ai/v2`, `curl docs.jina.ai/v3`, etc.
  - By default, `curl docs.jina.ai` fetches the content of `index.txt`
  - When accessing `docs.jina.ai` in a browser, you'll see a warning frame indicating that the content is intended for LLMs, not humans. This detection is based on the `user-agent` value, so `curl` or programatic requests shouln't trigger this warning (unless they pretend to be a browser)
  - The site is also optimized for search engine crawlers.
