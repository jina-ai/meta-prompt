Jina AI APIs on three hosts: Reader (`r.jina.ai`), Search (`s.jina.ai`) and the Search Foundation models (`api.jina.ai`).

| I want to | Endpoint |
|---|---|
| Read a web page or PDF as LLM-friendly Markdown | [GET r.jina.ai/{url}](#tag/reader/GET/{url}) · [POST r.jina.ai](#tag/reader/POST/) |
| Search the web and get the result pages as text | [GET s.jina.ai/{q}](#tag/search/GET/{q}) · [POST s.jina.ai/search](#tag/search/POST/search) |
| Embed text, images, audio, video or PDFs | [POST /v1/embeddings](#tag/search-foundation-models/POST/v1/embeddings) |
| Rerank candidates against a query | [POST /v1/rerank](#tag/search-foundation-models/POST/v1/rerank) |
| Transcribe a document image (OCR) | [POST /v1/chat/completions](#tag/generative-models/POST/v1/chat/completions) |
| Embed a large dataset asynchronously | [POST /v1/batch/embeddings](#tag/batch-embeddings/POST/v1/batch/embeddings) |
| See which models exist and what they cost | [GET /v1/models](#tag/model-list/GET/v1/models) |

**Authentication.** Send `Authorization: Bearer <your Jina API key>`. Get a key at https://jina.ai/?sui=apikey. Reader also answers without a key, at a lower rate limit; Search needs one.

**EU.** `eu.r.jina.ai` and `eu.s.jina.ai` keep all processing inside the EU.

**For LLMs.** `curl docs.jina.ai` returns the meta-prompt, a plain-text guide to these APIs written for coding agents. This reference as Markdown: `curl docs.jina.ai/api.md`.

**Rate limits.** r.jina.ai 500 RPM (5k premium), s.jina.ai 100 RPM (1k premium).
