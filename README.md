# Meta-Prompt for Jina Search Foundation APIs

## Usage
- `curl docs.jina.ai`: load default version defined in [`default`](default)
- Specific version: `curl docs.jina.ai/v1`
- Pipe into [`llm`](https://github.com/simonw/llm):
```bash
curl docs.jina.ai/v1 | llm -s 'grab all sentences from Hacker News, embed them, and visualize the results in a 2D UMAP with matplotlib' -m claude-3.5-sonnet
```

## Note
- Opening docs.jina.ai in a browser gives you a `text/html` response, but programmatic access gives you a clean `text/plain` response. This is due to the `user-agent` value.
- For browser JS `fetch` where you can't change the `user-agent` or in scenarios where you pretend to be a browser by `user-agent` spoofing, you can add 'accept': 'text/plain' to the header to force the `text/plain` response.

## API reference
- `docs.jina.ai` in a browser: one interactive [Scalar](https://github.com/scalar/scalar) reference for `api.jina.ai`, `r.jina.ai` and `s.jina.ai`. `curl docs.jina.ai` (and any other non-browser client) still gets the meta-prompt text, unchanged. `/v{x}` in a browser still shows that meta-prompt version as HTML.
- `docs.jina.ai/api.md`: the reference as Markdown.
- `docs.jina.ai/openapi.json`: the three hosts' OpenAPI specs merged into one.
- The old `docs.jina.ai/api` and `docs.jina.ai/api/openapi.json` redirect (301) to the addresses above.
- Built by [`api-docs/build.mjs`](api-docs/build.mjs) (Node >= 18, no dependencies) from each host's live `/openapi.json`. Reader and Search paths keep their own server, so "Try it" calls the right host; their schemas are prefixed `Reader_` / `Search_` to avoid name clashes.
- [`.github/workflows/api-docs.yml`](.github/workflows/api-docs.yml) rebuilds every 6 hours and commits only when a spec changed. Run it by hand with `node api-docs/build.mjs`.
- **Customising without losing it on rebuild**: the build never writes these two files, it layers them on top of the live specs every time.
  - [`api-docs/intro.md`](api-docs/intro.md): the intro and the "I want to" navigation table at the top of the page and of `api.md`. Links like `#tag/reader/GET/{url}` jump to an operation.
  - [`api-docs/overrides.mjs`](api-docs/overrides.mjs): section order, hidden operations, and summaries / descriptions for operations, parameters and body fields.
  - Undocumented query params of Reader/Search reuse the text of their `X-*` header twin automatically; the generated `- Cast to ...` / `- Member of ...` lines are dropped.
  - [`api-docs/coverage.md`](api-docs/coverage.md) (generated) lists every visible parameter that still has no description; the build warns when an override no longer matches anything.

## Worker
- docs.jina.ai is the Cloudflare worker in [`worker/`](worker/) (`metaprompt`). It reads everything from this repo's `main` branch on raw.githubusercontent.com, so pushing to `main` publishes.
- Deploy worker changes with `cd worker && wrangler deploy`.

## Developer's Guide
- Upload your prompt to `v{x}.txt` in the repository root.
- Use `curl docs.jina.ai/v{x}` to fetch your prompt:
  - No need to include `.txt`; simply use `curl docs.jina.ai/v1`, `curl docs.jina.ai/v2`, `curl docs.jina.ai/v3`, etc.
  - [`index.html`](index.html) is the `text/html` response template with placeholder variables inside; this file is only for browser/bot view and for human readability. Eye-candy stuff.
  - [`headers.json`](headers.json) defines some response header that *may be respected* by AI-browsers/apps in the future; one can use `curl -svo. docs.jina.ai` to check them.
