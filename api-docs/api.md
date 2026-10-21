# Jina AI API reference

Jina AI APIs on three hosts: Reader (`r.jina.ai`), Search (`s.jina.ai`) and the Search Foundation models (`api.jina.ai`).

| I want to | Endpoint |
|---|---|
| Read a web page or PDF as LLM-friendly Markdown | [GET r.jina.ai/{url}](https://docs.jina.ai/#tag/reader/GET/{url}) · [POST r.jina.ai](https://docs.jina.ai/#tag/reader/POST/) |
| Search the web and get the result pages as text | [GET s.jina.ai/{q}](https://docs.jina.ai/#tag/search/GET/{q}) · [POST s.jina.ai/search](https://docs.jina.ai/#tag/search/POST/search) |
| Embed text, images, audio, video or PDFs | [POST /v1/embeddings](https://docs.jina.ai/#tag/search-foundation-models/POST/v1/embeddings) |
| Rerank candidates against a query | [POST /v1/rerank](https://docs.jina.ai/#tag/search-foundation-models/POST/v1/rerank) |
| Transcribe a document image (OCR) | [POST /v1/chat/completions](https://docs.jina.ai/#tag/generative-models/POST/v1/chat/completions) |
| Embed a large dataset asynchronously | [POST /v1/batch/embeddings](https://docs.jina.ai/#tag/batch-embeddings/POST/v1/batch/embeddings) |
| See which models exist and what they cost | [GET /v1/models](https://docs.jina.ai/#tag/model-list/GET/v1/models) |

**Authentication.** Send `Authorization: Bearer <your Jina API key>`. Get a key at https://jina.ai/?sui=apikey. Reader also answers without a key, at a lower rate limit; Search needs one.

**EU.** `eu.r.jina.ai` and `eu.s.jina.ai` keep all processing inside the EU.

**For LLMs.** `curl docs.jina.ai` returns the meta-prompt, a plain-text guide to these APIs written for coding agents. This reference as Markdown: `curl docs.jina.ai/api.md`.

**Rate limits.** r.jina.ai 500 RPM (5k premium), s.jina.ai 100 RPM (1k premium).

_Merged from https://api.jina.ai/openapi.json, https://r.jina.ai/openapi.json, https://s.jina.ai/openapi.json. Plain text: https://docs.jina.ai/api.md. Spec: https://docs.jina.ai/openapi.json._

Best-in-class embeddings, rerankers and document models for multilingual and multimodal search.

### Capabilities

- **Text embeddings** — dense vectors for semantic search, similarity, clustering and classification, in 100+ languages.
- **Multimodal embeddings** — images, video, audio and PDFs embedded into the same space as text, so a query in one modality retrieves another.
- **Reranking** — score a query against a candidate set and reorder it; more accurate than embedding similarity, and the usual second stage after it.
- **Document OCR** — read a page image and return its content as text or markdown, with tables and layout preserved, over the OpenAI chat completions schema.
- **Batch embeddings** — the same embedding models over JSONL, asynchronously, for workloads too large to send inline.

### Authentication

Every endpoint except `GET /v1/models` requires a key:

```
Authorization: Bearer jina_YOUR_API_KEY
```

Get one at [jina.ai/api-dashboard/key-manager](https://jina.ai/api-dashboard/key-manager).

### Rate limits

Requests per minute and tokens per minute. Anything over a limit answers `429`.

| Endpoint | Free | Paid | Premium |
|---|---|---|---|
| `/v1/embeddings` | 500 RPM · 1M TPM | 500 RPM · 10M TPM | 5,000 RPM · 100M TPM |
| `/v1/rerank` | 500 RPM · 1M TPM | 500 RPM · 10M TPM | 5,000 RPM · 100M TPM |
| `/v1/chat/completions` | 100 RPM · 500K TPM | 100 RPM · 5M TPM | 1,000 RPM · 50M TPM |

### Errors

Failures carry a `detail`, a `code` from the table below and the `request_id` to quote in a support request. `/v1/chat/completions` is the exception: it answers in OpenAI's error envelope, with the same code inside it.

| Code | Status | Meaning |
|---|---|---|
| `INPUT_INVALID_LABELS` | 400 | Invalid training labels |
| `INPUT_LABEL_LIMIT_EXCEEDED` | 400 | Label limit exceeded: <current> labels provided, maximum <limit> allowed for your plan |
| `INPUT_MODEL_NOT_FOUND` | 400 | Model '<model>' not found |
| `INPUT_TOKEN_LIMIT_EXCEEDED` | 400 | Input text exceeds the model's maximum of <max_tokens> tokens |
| `AUTH_INVALID_API_KEY` | 401 | Invalid API key |
| `AUTH_INVALID_FORMAT` | 401 | Invalid authorization format |
| `AUTH_MISSING_API_KEY` | 401 | Authentication required |
| `AUTHZ_INSUFFICIENT_BALANCE` | 403 | Insufficient account balance |
| `AUTHZ_RESOURCE_LIMIT_EXCEEDED` | 403 | Resource limit exceeded for your plan |
| `RESOURCE_NOT_FOUND` | 404 | <resource_type> '<resource_id>' not found or access denied |
| `CONFLICT_RESOURCE_BUSY` | 409 | <resource_type> '<resource_id>' is currently being modified |
| `RATE_CONCURRENCY_LIMIT_EXCEEDED` | 429 | Concurrency limit exceeded: <current>/<limit> concurrent requests |
| `RATE_IP_LIMIT_EXCEEDED` | 429 | IP rate limit exceeded |
| `RATE_REQUEST_LIMIT_EXCEEDED` | 429 | Request rate limit exceeded: <current>/<limit> requests per minute |
| `RATE_TOKEN_LIMIT_EXCEEDED` | 429 | Token rate limit exceeded: <current>/<limit> tokens per minute |
| `INTERNAL_ERROR` | 500 | An unexpected error occurred |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `SERVICE_TIMEOUT` | 504 | Service request timed out |

## Reader API (r.jina.ai)

### Reader

Read a URL and get its content back in an LLM-friendly format.

#### POST https://r.jina.ai/

**Read a URL (JSON body)**

Send `{"url": "..."}` as JSON, with the same `X-*` headers as the GET form.

`Accept: application/json` returns JSON: the content is in `data.content`, and with `X-With-Links-Summary` / `X-With-Images-Summary` the links and images are in `data.links` and `data.images`. `Accept: text/event-stream` streams the result.

Authentication: optional.

Parameters:
- `url` (query, string): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (query, string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (query, boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (query, string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` (query, "initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (query, string): Base64 encoded PDF.
- `file` (query, string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (query, integer | string | array<integer | string>): Steer which page(s) to return for document files. See PageSelection.
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (query, boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (query, boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (query, boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (query, boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (query, boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (query, boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (query, boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (query, number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (query, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (query, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (query, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (query, boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (query, boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (query, boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (query, boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (query, any | string): Cookies to send when fetching the URL, for pages that need a login. Requests with cookies are not cached.
- `exportStorageState` (query, boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (query, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (query, boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (query, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (query, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (query, string): JavaScript to run in the page before extraction, inline or as a URL, e.g. to change the DOM.
- `injectFrameScript` (query, string): Like `injectPageScript`, for frames.
- `timeout` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (query, string): Specify browser locale for the page.
- `referer` (query, string): Specify referer for the page.
- `tokenBudget` (query, number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (query, number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `instruction` (query, string)
- `jsonSchema` (query, any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (query, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `Accept` (header, string): Specifies your preference for the response format. Supported formats: - text/event-stream - application/json or text/json - text/plain
- `X-Cache-Tolerance` (header, string): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `X-No-Cache` (header, string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `X-Respond-With` (header, string): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `X-Wait-For-Selector` (header, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `X-Target-Selector` (header, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `X-Remove-Selector` (header, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `X-Keep-Img-Data-Url` (header, string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `X-Proxy-Url` (header, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `X-Proxy-Resources` (header, string): Whether to load resources like image/style/scripts via the proxy server.
- `X-Proxy` (header, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `X-Robots-Txt` (header, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `DNT` (header, string): When set to 1, prevent the result of this request to be cached in the system.
- `X-Set-Cookie` (header, string): Sets cookie(s) to the headless browser for your request. Syntax is the same with standard Set-Cookie
- `X-Export-Storage-State` (header, string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `X-With-Generated-Alt` (header, string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `X-With-Images-Summary` (header, string): Enable dedicated summary section for images on the page.
- `X-With-links-Summary` (header, string): Enable dedicated summary section for hyper links on the page.
- `X-Retain-Links` (header, string): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `X-Retain-Images` (header, string): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `X-Retain-Media` (header, string): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `X-Preset` (header, string): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `X-With-Iframe` (header, string): Enable filling iframe contents into main. (violates standards)
- `X-With-Shadow-Dom` (header, string): Enable filling shadow dom contents into main. (violates standards)
- `X-Skip-Cert-Verification` (header, string): Enable skipping SSL certificate verification. (violates security best practices)
- `X-User-Agent` (header, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `X-Timeout` (header, string): Specify timeout in seconds. Max 180.
- `X-Locale` (header, string): Specify browser locale for the page.
- `X-Referer` (header, string): Specify referer for the page.
- `X-Token-Budget` (header, string): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `X-Max-Tokens` (header, string): Trim the response content at a maximum number of tokens.
- `X-Assert-Status-Code` (header, string): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `X-Respond-Timing` (header, string): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `X-Engine` (header, string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `X-Base` (header, string): Select base modes of relative URLs. Supported: initial, final
- `X-Remove-Overlay` (header, string): Specify whether to remove overlay elements from the page.
- `X-Detach-Invisibles` (header, string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `X-Markdown-Chunking` (header, string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `X-Md-Heading-Style` (header, string): Heading style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: setext, atx
- `X-Md-Hr` (header, string): Hr text of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options).
- `X-Md-Bullet-List-Marker` (header, string): Bullet list marker of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: -, +, *
- `X-Md-Em-Delimiter` (header, string): Em delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: _, *
- `X-Md-Strong-Delimiter` (header, string): Strong delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: **, __
- `X-Md-Link-Style` (header, string): Link style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: inlined, referenced, discarded
- `X-Md-Link-Reference-Style` (header, string): Link reference style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: full, collapsed, shortcut, discarded
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` ("initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (string): Base64 encoded PDF.
- `file` (string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (integer | string | array<integer | string>): Steer which page(s) to return for document files. See PageSelection.
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (array<string>): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (array<string>): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (array<string>): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (array<any | string>): Cookies to send when fetching the URL, for pages that need a login. Requests with cookies are not cached.
- `storageState` (StorageState)
  - `cookies` (array<Cookie>, default [])
    - `name` (string, required): [REQUIRED]
    - `value` (string, required): [REQUIRED]
    - `domain` (string)
    - `path` (string, default "/")
    - `expires` (string)
    - `httpOnly` (boolean)
    - `secure` (boolean)
    - `sameSite` ("Strict" | "Lax" | "None" | string)
  - `origins` (array<LocalStorageOrigin>, default [])
    - `origin` (string, required): [REQUIRED]
    - `localStorage` (array<LocalStorageItem>, default [])
- `exportStorageState` (boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` ("auto" | "browser" | "curl" | "cf-browser-rendering" | string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (array<string>): JavaScript to run in the page before extraction, inline or as a URL, e.g. to change the DOM.
- `injectFrameScript` (array<string>): Like `injectPageScript`, for frames.
- `timeout` (number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): Specify browser locale for the page.
- `referer` (string): Specify referer for the page.
- `tokenBudget` (number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `viewport` (Viewport)
  - `width` (number, default 1280)
  - `height` (number, default 1280)
  - `deviceScaleFactor` (number)
  - `isMobile` (boolean)
  - `isLandscape` (boolean)
  - `hasTouch` (boolean)
- `instruction` (string)
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (boolean | string)
- `markdown` (TurnDownTweakableOptions)
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle
  - `hr` (string): Turndown options > hr - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle
- `ocr` (OCRPreferences)
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text)
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode)
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode)
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode)
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode)
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object)

Responses:
- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
- `402`: Payment Required
- `403`: Forbidden
- `409`: Conflict
- `413`: Payload Too Large
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `451`: Unavailable For Legal Reasons
- `500`: Internal Server Error
- `503`: Service Unavailable

#### GET https://r.jina.ai/{url}

**Read a URL**

Put the target URL right after `https://r.jina.ai/`, e.g. `https://r.jina.ai/https://example.com`.

Returns the page as LLM-friendly Markdown. Every option is an `X-*` header, or the query parameter of the same name.

Authentication: optional.

Parameters:
- `url` (path, string, required): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (query, string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (query, boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (query, string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` (query, "initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (query, string): Base64 encoded PDF.
- `file` (query, string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (query, integer | string | array<integer | string>): Steer which page(s) to return for document files. See PageSelection.
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (query, boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (query, boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (query, boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (query, boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (query, boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (query, boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (query, boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (query, number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (query, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (query, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (query, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (query, boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (query, boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (query, boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (query, boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (query, any | string): Cookies to send when fetching the URL, for pages that need a login. Requests with cookies are not cached.
- `exportStorageState` (query, boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (query, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (query, boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (query, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (query, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (query, string): JavaScript to run in the page before extraction, inline or as a URL, e.g. to change the DOM.
- `injectFrameScript` (query, string): Like `injectPageScript`, for frames.
- `timeout` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (query, string): Specify browser locale for the page.
- `referer` (query, string): Specify referer for the page.
- `tokenBudget` (query, number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (query, number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `instruction` (query, string)
- `jsonSchema` (query, any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (query, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `Accept` (header, string): Specifies your preference for the response format. Supported formats: - text/event-stream - application/json or text/json - text/plain
- `X-Cache-Tolerance` (header, string): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `X-No-Cache` (header, string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `X-Respond-With` (header, string): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `X-Wait-For-Selector` (header, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `X-Target-Selector` (header, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `X-Remove-Selector` (header, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `X-Keep-Img-Data-Url` (header, string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `X-Proxy-Url` (header, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `X-Proxy-Resources` (header, string): Whether to load resources like image/style/scripts via the proxy server.
- `X-Proxy` (header, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `X-Robots-Txt` (header, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `DNT` (header, string): When set to 1, prevent the result of this request to be cached in the system.
- `X-Set-Cookie` (header, string): Sets cookie(s) to the headless browser for your request. Syntax is the same with standard Set-Cookie
- `X-Export-Storage-State` (header, string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `X-With-Generated-Alt` (header, string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `X-With-Images-Summary` (header, string): Enable dedicated summary section for images on the page.
- `X-With-links-Summary` (header, string): Enable dedicated summary section for hyper links on the page.
- `X-Retain-Links` (header, string): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `X-Retain-Images` (header, string): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `X-Retain-Media` (header, string): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `X-Preset` (header, string): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `X-With-Iframe` (header, string): Enable filling iframe contents into main. (violates standards)
- `X-With-Shadow-Dom` (header, string): Enable filling shadow dom contents into main. (violates standards)
- `X-Skip-Cert-Verification` (header, string): Enable skipping SSL certificate verification. (violates security best practices)
- `X-User-Agent` (header, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `X-Timeout` (header, string): Specify timeout in seconds. Max 180.
- `X-Locale` (header, string): Specify browser locale for the page.
- `X-Referer` (header, string): Specify referer for the page.
- `X-Token-Budget` (header, string): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `X-Max-Tokens` (header, string): Trim the response content at a maximum number of tokens.
- `X-Assert-Status-Code` (header, string): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `X-Respond-Timing` (header, string): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `X-Engine` (header, string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `X-Base` (header, string): Select base modes of relative URLs. Supported: initial, final
- `X-Remove-Overlay` (header, string): Specify whether to remove overlay elements from the page.
- `X-Detach-Invisibles` (header, string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `X-Markdown-Chunking` (header, string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `X-Md-Heading-Style` (header, string): Heading style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: setext, atx
- `X-Md-Hr` (header, string): Hr text of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options).
- `X-Md-Bullet-List-Marker` (header, string): Bullet list marker of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: -, +, *
- `X-Md-Em-Delimiter` (header, string): Em delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: _, *
- `X-Md-Strong-Delimiter` (header, string): Strong delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: **, __
- `X-Md-Link-Style` (header, string): Link style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: inlined, referenced, discarded
- `X-Md-Link-Reference-Style` (header, string): Link reference style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: full, collapsed, shortcut, discarded
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Responses:
- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
- `402`: Payment Required
- `403`: Forbidden
- `409`: Conflict
- `413`: Payload Too Large
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `451`: Unavailable For Legal Reasons
- `500`: Internal Server Error
- `503`: Service Unavailable

#### GET https://r.jina.ai/echo/{rest}

**echo**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Parameters:
- `rest` (path, any, required)

Responses:
- `200`: OK

#### PUT https://r.jina.ai/echo/{rest}

**echo**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Parameters:
- `rest` (path, any, required)

Request body (`application/json`):
- 

Responses:
- `200`: OK

#### POST https://r.jina.ai/echo/{rest}

**echo**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Parameters:
- `rest` (path, any, required)

Request body (`application/json`):
- 

Responses:
- `200`: OK

#### DELETE https://r.jina.ai/echo/{rest}

**echo**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Parameters:
- `rest` (path, any, required)

Responses:
- `200`: OK

#### PATCH https://r.jina.ai/echo/{rest}

**echo**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Parameters:
- `rest` (path, any, required)

Request body (`application/json`):
- 

Responses:
- `200`: OK

#### GET https://r.jina.ai/echo

**echoAtRoot**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Responses:
- `200`: OK

#### PUT https://r.jina.ai/echo

**echoAtRoot**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Request body (`application/json`):
- 

Responses:
- `200`: OK

#### POST https://r.jina.ai/echo

**echoAtRoot**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Request body (`application/json`):
- 

Responses:
- `200`: OK

#### DELETE https://r.jina.ai/echo

**echoAtRoot**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Responses:
- `200`: OK

#### PATCH https://r.jina.ai/echo

**echoAtRoot**

Echo back the details of the incoming HTTP request, with the Cloudflare-reported country of the client IP.

Request body (`application/json`):
- 

Responses:
- `200`: OK

## Search API (s.jina.ai)

### Search

Search the web and get the result pages back in an LLM-friendly format.

#### GET https://s.jina.ai/{q}

**Search the web**

Put the query right after `https://s.jina.ai/`, e.g. `https://s.jina.ai/jina%20ai`.

Returns the top results with each page's content as LLM-friendly text. `X-Respond-With: no-content` returns the results without page content; `X-Site` keeps results to one domain.

Authentication: optional.

Parameters:
- `url` (query, string): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (query, string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (query, boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (query, string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` (query, "initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (query, string): Base64 encoded PDF.
- `file` (query, string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (query, number): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (query, boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (query, boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (query, boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (query, boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (query, boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (query, boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (query, boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (query, number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (query, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (query, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (query, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (query, boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (query, boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (query, boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (query, boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (query, any | string): Cookies to send when fetching each result page, for pages that need a login. Requests with cookies are not cached.
- `exportStorageState` (query, boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (query, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (query, boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (query, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (query, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` (query, "google" | "bing" | "reader"): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (query, string): JavaScript to run in each result page before extraction, inline or as a URL.
- `injectFrameScript` (query, string): Like `injectPageScript`, for frames.
- `timeout` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (query, string): Specify browser locale for the page.
- `referer` (query, string): Specify referer for the page.
- `tokenBudget` (query, number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (query, number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `instruction` (query, string)
- `jsonSchema` (query, any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (query, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `ext` (query, string): Search operator `ext:` (file extension).
- `filetype` (query, string): Search operator `filetype:`, e.g. `pdf`.
- `intitle` (query, string): Search operator `intitle:`: words that must appear in the page title.
- `loc` (query, string): Search operator `loc:` (location).
- `site` (query, string): Keep results to this domain, e.g. `https://jina.ai`. Same as the `X-Site` header.
- `type` (query, "web" | "images" | "news", default "web"): Result type: `web` (default), `images` or `news`.
- `num` (query, number): Maximum number of results, 0 to 20, default 10. Larger values can add latency and drop special result types.
- `count` (query, number): Same as `num`.
- `provider` (query, "google" | "bing" | "reader"): Search engine to use: `google`, `bing` or `reader`.
- `gl` (query, string): Country to search from, as a two-letter country code.
- `hl` (query, string): Language of the search, as a two-letter language code.
- `location` (query, string): Where the search should originate from. City level works best.
- `fallback` (query, boolean): If `true` and the search returns nothing, fall back to local search results. Default `false`.
- `q` (path, string, required): The search query. Not needed when the query is already in the path (`https://s.jina.ai/<query>`).
- `nfpr` (query, boolean): Passed to the search engine; on Google, `true` turns off query auto-correction.
- `Accept` (header, string): Specifies your preference for the response format. Supported formats: - text/event-stream - application/json or text/json - text/plain
- `X-Cache-Tolerance` (header, string): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `X-No-Cache` (header, string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `X-Respond-With` (header, string): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `X-Wait-For-Selector` (header, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `X-Target-Selector` (header, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `X-Remove-Selector` (header, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `X-Keep-Img-Data-Url` (header, string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `X-Proxy-Url` (header, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `X-Proxy-Resources` (header, string): Whether to load resources like image/style/scripts via the proxy server.
- `X-Proxy` (header, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `X-Robots-Txt` (header, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `DNT` (header, string): When set to 1, prevent the result of this request to be cached in the system.
- `X-Set-Cookie` (header, string): Sets cookie(s) to the headless browser for your request. Syntax is the same with standard Set-Cookie
- `X-Export-Storage-State` (header, string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `X-With-Generated-Alt` (header, string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `X-With-Images-Summary` (header, string): Enable dedicated summary section for images on the page.
- `X-With-links-Summary` (header, string): Enable dedicated summary section for hyper links on the page.
- `X-Retain-Links` (header, string): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `X-Retain-Images` (header, string): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `X-Retain-Media` (header, string): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `X-Preset` (header, string): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `X-With-Iframe` (header, string): Enable filling iframe contents into main. (violates standards)
- `X-With-Shadow-Dom` (header, string): Enable filling shadow dom contents into main. (violates standards)
- `X-Skip-Cert-Verification` (header, string): Enable skipping SSL certificate verification. (violates security best practices)
- `X-User-Agent` (header, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `X-Timeout` (header, string): Specify timeout in seconds. Max 180.
- `X-Locale` (header, string): Specify browser locale for the page.
- `X-Referer` (header, string): Specify referer for the page.
- `X-Token-Budget` (header, string): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `X-Max-Tokens` (header, string): Trim the response content at a maximum number of tokens.
- `X-Assert-Status-Code` (header, string): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `X-Respond-Timing` (header, string): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `X-Engine` (header, string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `X-Base` (header, string): Select base modes of relative URLs. Supported: initial, final
- `X-Remove-Overlay` (header, string): Specify whether to remove overlay elements from the page.
- `X-Detach-Invisibles` (header, string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `X-Markdown-Chunking` (header, string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `X-Md-Heading-Style` (header, string): Heading style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: setext, atx
- `X-Md-Hr` (header, string): Hr text of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options).
- `X-Md-Bullet-List-Marker` (header, string): Bullet list marker of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: -, +, *
- `X-Md-Em-Delimiter` (header, string): Em delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: _, *
- `X-Md-Strong-Delimiter` (header, string): Strong delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: **, __
- `X-Md-Link-Style` (header, string): Link style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: inlined, referenced, discarded
- `X-Md-Link-Reference-Style` (header, string): Link reference style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: full, collapsed, shortcut, discarded
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Responses:
- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
- `402`: Payment Required
- `403`: Forbidden
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `500`: Internal Server Error
- `503`: Service Unavailable

#### POST https://s.jina.ai/search

**Search the web (JSON body)**

Send `{"q": "..."}` as JSON, optionally with `gl`, `hl`, `location`, `num` and `page`. Same `X-*` headers as the GET form.

Authentication: optional.

Parameters:
- `url` (query, string): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (query, string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (query, boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (query, string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` (query, "initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (query, string): Base64 encoded PDF.
- `file` (query, string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (query, number): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (query, boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (query, boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (query, boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (query, boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (query, boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (query, boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (query, boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (query, number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (query, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (query, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (query, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (query, boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (query, boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (query, boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (query, boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (query, any | string): Cookies to send when fetching each result page, for pages that need a login. Requests with cookies are not cached.
- `exportStorageState` (query, boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (query, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (query, boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (query, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (query, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` (query, "google" | "bing" | "reader"): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (query, string): JavaScript to run in each result page before extraction, inline or as a URL.
- `injectFrameScript` (query, string): Like `injectPageScript`, for frames.
- `timeout` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (query, string): Specify browser locale for the page.
- `referer` (query, string): Specify referer for the page.
- `tokenBudget` (query, number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (query, number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `instruction` (query, string)
- `jsonSchema` (query, any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (query, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (query, number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `ext` (query, string): Search operator `ext:` (file extension).
- `filetype` (query, string): Search operator `filetype:`, e.g. `pdf`.
- `intitle` (query, string): Search operator `intitle:`: words that must appear in the page title.
- `loc` (query, string): Search operator `loc:` (location).
- `site` (query, string): Keep results to this domain, e.g. `https://jina.ai`. Same as the `X-Site` header.
- `type` (query, "web" | "images" | "news", default "web"): Result type: `web` (default), `images` or `news`.
- `num` (query, number): Maximum number of results, 0 to 20, default 10. Larger values can add latency and drop special result types.
- `count` (query, number): Same as `num`.
- `provider` (query, "google" | "bing" | "reader"): Search engine to use: `google`, `bing` or `reader`.
- `gl` (query, string): Country to search from, as a two-letter country code.
- `hl` (query, string): Language of the search, as a two-letter language code.
- `location` (query, string): Where the search should originate from. City level works best.
- `fallback` (query, boolean): If `true` and the search returns nothing, fall back to local search results. Default `false`.
- `q` (query, string): The search query. Not needed when the query is already in the path (`https://s.jina.ai/<query>`).
- `nfpr` (query, boolean): Passed to the search engine; on Google, `true` turns off query auto-correction.
- `Accept` (header, string): Specifies your preference for the response format. Supported formats: - text/event-stream - application/json or text/json - text/plain
- `X-Cache-Tolerance` (header, string): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `X-No-Cache` (header, string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `X-Respond-With` (header, string): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `X-Wait-For-Selector` (header, string): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `X-Target-Selector` (header, string): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `X-Remove-Selector` (header, string): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `X-Keep-Img-Data-Url` (header, string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `X-Proxy-Url` (header, string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `X-Proxy-Resources` (header, string): Whether to load resources like image/style/scripts via the proxy server.
- `X-Proxy` (header, string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `X-Robots-Txt` (header, string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `DNT` (header, string): When set to 1, prevent the result of this request to be cached in the system.
- `X-Set-Cookie` (header, string): Sets cookie(s) to the headless browser for your request. Syntax is the same with standard Set-Cookie
- `X-Export-Storage-State` (header, string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `X-With-Generated-Alt` (header, string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `X-With-Images-Summary` (header, string): Enable dedicated summary section for images on the page.
- `X-With-links-Summary` (header, string): Enable dedicated summary section for hyper links on the page.
- `X-Retain-Links` (header, string): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `X-Retain-Images` (header, string): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `X-Retain-Media` (header, string): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `X-Preset` (header, string): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `X-With-Iframe` (header, string): Enable filling iframe contents into main. (violates standards)
- `X-With-Shadow-Dom` (header, string): Enable filling shadow dom contents into main. (violates standards)
- `X-Skip-Cert-Verification` (header, string): Enable skipping SSL certificate verification. (violates security best practices)
- `X-User-Agent` (header, string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `X-Timeout` (header, string): Specify timeout in seconds. Max 180.
- `X-Locale` (header, string): Specify browser locale for the page.
- `X-Referer` (header, string): Specify referer for the page.
- `X-Token-Budget` (header, string): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `X-Max-Tokens` (header, string): Trim the response content at a maximum number of tokens.
- `X-Assert-Status-Code` (header, string): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `X-Respond-Timing` (header, string): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `X-Engine` (header, string): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `X-Base` (header, string): Select base modes of relative URLs. Supported: initial, final
- `X-Remove-Overlay` (header, string): Specify whether to remove overlay elements from the page.
- `X-Detach-Invisibles` (header, string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `X-Markdown-Chunking` (header, string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `X-Md-Heading-Style` (header, string): Heading style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: setext, atx
- `X-Md-Hr` (header, string): Hr text of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options).
- `X-Md-Bullet-List-Marker` (header, string): Bullet list marker of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: -, +, *
- `X-Md-Em-Delimiter` (header, string): Em delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: _, *
- `X-Md-Strong-Delimiter` (header, string): Strong delimiter of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: **, __
- `X-Md-Link-Style` (header, string): Link style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: inlined, referenced, discarded
- `X-Md-Link-Reference-Style` (header, string): Link reference style of the generated markdown. This is an option passed through to [Turndown](https://github.com/mixmark-io/turndown?tab=readme-ov-file#options). Supported: full, collapsed, shortcut, discarded
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).
- `preloadUrl` (string): URL to preload before scraping. Ignored when no URL is provided.
- `noServiceWorker` (boolean | string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.
- `html` (string): Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.
- `base` ("initial" | "final", default "initial"): Select base modes of relative URLs. Supported: initial, final
- `pdf` (string): Base64 encoded PDF.
- `file` (string): Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.
- `page` (number): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed, 0 is the same as 1. Accepts a page number, a list and/or ranges like `1,3,5-7`. At most 35 pages can be selected. With multiple pages, DocLayout / OCR runs over each selected page. Ignored when the target is not a document.
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): Specifies the (non-default) form of the crawled data you prefer. Supported formats: - markdown - html - text - pageshot - screenshot - content - frontmatter - any combination of the above - vlm - jina-ocr-v1 - jina-ocr - readerlm-v2 Default: content
- `withGeneratedAlt` (boolean | string): Enable automatic alt-text generating for images without an meaningful alt-text. Note: Does not work when `X-Respond-With` is specified
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): Image retention modes. Supported modes: - all: all images - none: no images - alt: only alt text - all_p: all images and with generated alt text - alt_p: only alt text and with generated alt
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): Media retention modes for video, audio, and embedded video iframes. Supported modes: - none: no media - text: plain label, e.g. `Video 1` - link: markdown link, e.g. `[Video 1](url)` (default) - image: markdown image syntax, e.g. `![Video 1](url)` - html: original HTML with irrelevant attributes (class, id, style, data-*, aria-*) stripped
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): Apply a preset configuration for common scenarios. Supported presets: - reader: optimized for display to human users - index: optimized for semantic indexing - research: optimized for academic/research AI agents - agent: optimized for day-to-day AI agents - spider: optimized for recursive site crawling Preset values are applied only to options not explicitly set by the caller.
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): Link retention modes. Supported modes: - all: all links - none: no links - text: only link text - gpt-oss: gpt-oss link citation format `【{id}†.*】`
- `withLinksSummary` (boolean | string | string): Enable dedicated summary section for hyper links on the page.
- `withImagesSummary` (boolean | string): Enable dedicated summary section for images on the page.
- `noCache` (boolean | string): Ignores internal cache if this header is specified with a value. Equivalent to X-Cache-Tolerance: 0
- `removeOverlay` (boolean | string): Specify whether to remove overlay elements from the page.
- `detachInvisibles` (boolean | string): Temporarily detach elements with computed `display:none` before snapshotting, then restore them. Requires the browser engine and disables caching.
- `noGfm` (boolean | string | string): Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.
- `cacheTolerance` (number): Sets internal cache tolerance in seconds if this header is specified with a integer.
- `targetSelector` (array<string>): Specifies a CSS selector for return target instead of the full html. Implies `X-Wait-For-Selector: (same selector)`
- `waitForSelector` (array<string>): Specifies a CSS selector to wait for the appearance of such an element before returning. Example: `X-Wait-For-Selector: .content-block`
- `removeSelector` (array<string>): Specifies a CSS selector to remove elements from the full html. Example `X-Remove-Selector: nav`
- `keepImgDataUrl` (boolean | string): Keep data-url as it instead of transforming them to object-url. (Only applicable when targeting markdown format) Example `X-Keep-Img-Data-Url: true`
- `withIframe` (boolean | string | string): Enable filling iframe contents into main. (violates standards)
- `withShadowDom` (boolean | string): Enable filling shadow dom contents into main. (violates standards)
- `skipCertVerification` (boolean | string): Enable skipping SSL certificate verification. (violates security best practices)
- `setCookies` (array<any | string>): Cookies to send when fetching each result page, for pages that need a login. Requests with cookies are not cached.
- `storageState` (StorageState)
  - `cookies` (array<Cookie>, default [])
    - `name` (string, required): [REQUIRED]
    - `value` (string, required): [REQUIRED]
    - `domain` (string)
    - `path` (string, default "/")
    - `expires` (string)
    - `httpOnly` (boolean)
    - `secure` (boolean)
    - `sameSite` ("Strict" | "Lax" | "None" | string)
  - `origins` (array<LocalStorageOrigin>, default [])
    - `origin` (string, required): [REQUIRED]
    - `localStorage` (array<LocalStorageItem>, default [])
- `exportStorageState` (boolean | string): Export the browser storage state (cookies and per-origin localStorage) accumulated during the crawl. When enabled, the JSON response includes a `storageState` field whose shape mirrors the `storageState` request option, so it can be fed back into a subsequent request. Requires the browser engine and disables caching.
- `proxyUrl` (string): Specifies your custom proxy if you prefer to use one. Supported protocols: - http - https - socks4 - socks5 For authentication, https://user:pass@host:port
- `proxyResources` (boolean | string): Whether to load resources like image/style/scripts via the proxy server.
- `proxy` (string): Use a proxy server provided by us. Optionally specify two-letter country code.
- `userAgent` (string): Override User-Agent. Several special values: - browser: use the internal browser UA - auto: pass-through your UA if it starts with `Mozilla/5.0`, otherwise use the internal browser UA - inherit / pass-through: use the User-Agent from the request context if applicable - bot: Use a pre-defined bot User-Agent from this service - diversify: Use a diversified browser User-Agent Or specify your own user agent string. Note: anonymous users specifying a browser UA will have no effect and will fall back to the internal browser UA. Default: browser
- `engine` ("google" | "bing" | "reader"): Specify the engine to use for crawling. Supported: browser, direct, cf-browser-rendering
- `injectPageScript` (array<string>): JavaScript to run in each result page before extraction, inline or as a URL.
- `injectFrameScript` (array<string>): Like `injectPageScript`, for frames.
- `timeout` (number): - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): Specify browser locale for the page.
- `referer` (string): Specify referer for the page.
- `tokenBudget` (number): Specify a budget in tokens. If the resulting token cost exceeds the budget, the request is rejected. Note this parameter is ignored for the search endpoint.
- `assertStatusCode` (number): Assert the HTTP status code of the crawled page. If the actual status code does not match the asserted one, the request is rejected with 422 Unprocessable Entity.
- `viewport` (Viewport)
  - `width` (number, default 1280)
  - `height` (number, default 1280)
  - `deviceScaleFactor` (number)
  - `isMobile` (boolean)
  - `isLandscape` (boolean)
  - `hasTouch` (boolean)
- `instruction` (string)
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object.
- `robotsTxt` (string): Load and conform to the respective robot.txt on the target origin. Optionally specify a bot UA to check against.
- `zeroDataRetention` (boolean | string)
- `markdown` (TurnDownTweakableOptions)
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle
  - `hr` (string): Turndown options > hr - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle
- `ocr` (OCRPreferences)
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text)
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode)
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode)
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode)
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode)
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): Explicitly specify the respond timing. One of the following: - html: directly return unrendered HTML - visible-content: return immediately when any content becomes available - mutation-idle: wait for DOM mutations to settle and remain unchanged for at least 0.2s - resource-idle: wait for no additional resources that would affect page logic and content has SUCCEEDED loading in 0.5s - media-idle: wait for no additional resources, including media resources, has SUCCEEDED loading in 0.5s - network-idle: wait for full load of webpage, also known as networkidle0.
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): Opt-in markdown chunking. Supported values: - true - h1 - h2 - h3 - h4 - h5 - structured - s1 - s2 - s3 - s4 - s5 Note if you are expecting text return, the chunking is done by injecting character \u001D
- `maxTokens` (number): - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object)
- `ext` (array<string>): Search operator `ext:` (file extension).
- `filetype` (array<string>): Search operator `filetype:`, e.g. `pdf`.
- `intitle` (array<string>): Search operator `intitle:`: words that must appear in the page title.
- `loc` (array<string>): Search operator `loc:` (location).
- `site` (array<string>): Keep results to this domain, e.g. `https://jina.ai`. Same as the `X-Site` header.
- `type` ("web" | "images" | "news", default "web"): Result type: `web` (default), `images` or `news`.
- `num` (number): Maximum number of results, 0 to 20, default 10. Larger values can add latency and drop special result types.
- `count` (number): Same as `num`.
- `provider` ("google" | "bing" | "reader"): Search engine to use: `google`, `bing` or `reader`.
- `gl` (string): Country to search from, as a two-letter country code.
- `hl` (string): Language of the search, as a two-letter language code.
- `location` (string): Where the search should originate from. City level works best.
- `fallback` (boolean): If `true` and the search returns nothing, fall back to local search results. Default `false`.
- `q` (string): The search query. Not needed when the query is already in the path (`https://s.jina.ai/<query>`).
- `nfpr` (boolean): Passed to the search engine; on Google, `true` turns off query auto-correction.

Responses:
- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
- `402`: Payment Required
- `403`: Forbidden
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `500`: Internal Server Error
- `503`: Service Unavailable

## Search Foundation API (api.jina.ai)

### Model List

Every model this API serves, in OpenRouter-compatible form: identifiers, input and output modalities, context lengths and prices. Read it before hardcoding a model name — the catalogue moves.

#### GET https://api.jina.ai/v1/models

**List Models**

Every model in the catalogue, with its modalities, limits and price.

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### GET https://api.jina.ai/v1/models/{model_id}

**Get Model**

One model by id, in full (`jina-ai/jina-embeddings-v3`) or short
(`jina-embeddings-v3`) form.

Parameters:
- `model_id` (path, string, required)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

### Search Foundation Models

**Embeddings** turn text, images, audio, video and PDFs into dense vectors for semantic search, RAG, clustering and classification. Task-specific variants (`retrieval.query`, `retrieval.passage`, `text-matching`, `clustering`, `classification`) are selected per request rather than per model, and `dimensions` truncates the output where a model supports it.

**Reranking** scores a query against a candidate set and returns it reordered, which is more accurate than embedding similarity and slower — the usual shape is embeddings to retrieve, reranking to refine.

Each endpoint's `model` field lists the models it accepts.

#### POST https://api.jina.ai/v1/embeddings

**Embeddings**

Embed text, images, audio, video or PDFs as dense vectors.

`model` selects the request shape as well as the model: each one below
lists the inputs and options it accepts.

Request body (`application/json`, required):
One of 10 shapes:
- `EmbeddingsV2Request`: Jina Embeddings v2 text embedding models.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `model` ("jina-embeddings-v2-base-en" | "jina-embeddings-v2-base-zh" | "jina-embeddings-v2-base-de" | "jina-embeddings-v2-base-es" | "jina-embeddings-v2-base-code", required): The embedding model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Text to embed: a string, `TextDoc`, or a list of items.
- `EmbeddingsV3Request`: Jina Embeddings v3 with task-specific optimization and flexible dimensions.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `model` (string, required): The embedding model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Text to embed: a string, `TextDoc`, or a list of items.
  - `task` ("retrieval.query" | "retrieval.passage" | "text-matching" | "classification" | "separation" | null): Task optimization: `retrieval.query` for queries, `retrieval.passage` for documents, `text-matching` for similarity, `classification`, or `separation` for clustering.
  - `late_chunking` (boolean | null): If true, concatenates all inputs and processes as one sequence before splitting. Useful for context across chunks.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-1024.
- `EmbeddingsV4Request`: Jina Embeddings v4 multimodal model for text, images, and PDFs.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `model` (string, required): The embedding model to use.
  - `input` (string | TextDoc | ImageDoc | PDFDoc | array<string | TextDoc | ImageDoc>, required): Content to embed: a string, `TextDoc`, `ImageDoc`, `PDFDoc`, or a list of items. PDFs must be sent individually. Images up to 8MB; PDFs up to 8MB.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `late_chunking` (boolean | null): If true, concatenates all text inputs and processes as one sequence before splitting. Only works with text.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-2048.
  - `task` ("text-matching" | "retrieval.query" | "retrieval.passage" | "code.query" | "code.passage" | null, default "text-matching"): Task optimization: `text-matching` (default), `retrieval.query`, `retrieval.passage`, `code.query`, or `code.passage`.
  - `return_multivector` (boolean | null, default false): If true, returns one embedding per token. Cannot be used with `dimensions`.
  - `return_tokenized_input` (boolean | null, default false): If true, returns tokens alongside multi-vector embeddings. Requires `return_multivector=true`.
- `EmbeddingsV5Request`: Jina Embeddings v5, with task-specific adapters and truncatable dimensions.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `model` ("jina-embeddings-v5-text-nano" | "jina-embeddings-v5-text-small" | "jina-embeddings-v5-omni-small" | "jina-embeddings-v5-omni-nano", required): The embedding model to use.
  - `input` (string | TextDoc | ImageDoc | VideoDoc | AudioDoc | PDFDoc | array<string | TextDoc | ImageDoc | VideoDoc | AudioDoc | MergedContentGroup>, required): Content to embed: a string, `TextDoc`, `ImageDoc`, `VideoDoc`, `AudioDoc`, `PDFDoc`, or a list of these. A list item may also be a `{content: [...]}` group, fused into one embedding. A PDF must be sent on its own, not inside a list.
  - `task` ("retrieval.query" | "retrieval.passage" | "text-matching" | "clustering" | "classification" | null, default "text-matching"): Task optimization: `retrieval.query` for queries, `retrieval.passage` for documents, `text-matching` for similarity, `clustering`, or `classification`.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-1024.
- `CodeEmbeddings500MRequest`: Code embeddings (0.5b) for search over source, and between source and prose.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `model` (string, required): The code embedding model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Code or text to embed: a string, `TextDoc`, or a list of items.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-896.
  - `task` ("nl2code.query" | "nl2code.passage" | "qa.query" | "qa.passage" | "code2code.query" | "code2code.passage" | "code2nl.query" | "code2nl.passage" | "code2completion.query" | "code2completion.passage" | null, default "nl2code.query"): Task type: `nl2code`, `qa`, `code2code`, `code2nl`, or `code2completion`. Use `.query` for queries, `.passage` for documents.
- `CodeEmbeddings1500MRequest`: Code embeddings (1.5b) for search over source, and between source and prose.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `model` (string, required): The code embedding model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Code or text to embed: a string, `TextDoc`, or a list of items.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-1536.
  - `task` ("nl2code.query" | "nl2code.passage" | "qa.query" | "qa.passage" | "code2code.query" | "code2code.passage" | "code2nl.query" | "code2nl.passage" | "code2completion.query" | "code2completion.passage" | null, default "nl2code.query"): Task type: `nl2code`, `qa`, `code2code`, `code2nl`, or `code2completion`. Use `.query` for queries, `.passage` for documents.
- `ClipV1Request`: CLIP v1 multimodal model for images and text in a shared vector space.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `model` (string, required): The CLIP model to use.
  - `input` (string | TextDoc | ImageDoc | PDFDoc | array<string | TextDoc | ImageDoc>, required): Content to embed: a string, `TextDoc`, `ImageDoc`, `PDFDoc`, or a list of items. PDFs must be sent individually. Images up to 8MB.
- `ClipV2Request`: CLIP v2 with Matryoshka representation learning for flexible dimensions.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
  - `truncate` (boolean | null, default false): If true, truncates input exceeding the model's max token limit instead of returning an error.
  - `model` (string, required): The CLIP model to use.
  - `input` (string | TextDoc | ImageDoc | PDFDoc | array<string | TextDoc | ImageDoc>, required): Content to embed: a string, `TextDoc`, `ImageDoc`, `PDFDoc`, or a list of items. PDFs must be sent individually. Images up to 8MB.
  - `task` (string | null): Set to `retrieval.query` to optimize for search queries. Leave unset for documents.
  - `dimensions` (integer | null): Number of dimensions for the output embedding. Range: 1-1024.
- `ColbertV1Request`: ColBERT v1 for token-level late interaction retrieval.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `model` (string, required): The ColBERT model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Text to embed: a string, `TextDoc`, or a list of items.
  - `input_type` ("query" | "document" | null, default "document"): Role of the input: `query` for search queries, `document` for passages.
- `ColbertV2Request`: ColBERT v2 with Matryoshka representation learning for flexible dimensions.
  - `embedding_type` ("float" | "base64" | "binary" | "ubinary" | array<"float" | "base64" | "binary" | "ubinary"> | null): Output encoding format: `float`, `base64`, `binary`, `ubinary`, or a list of these.
  - `model` (string, required): The ColBERT model to use.
  - `input` (string | TextDoc | array<string | TextDoc>, required): Text to embed: a string, `TextDoc`, or a list of items.
  - `input_type` ("query" | "document" | null, default "document"): Role of the input: `query` for search queries, `document` for passages.
  - `dimensions` (64 | 96 | 128 | null): Dimensions per token: `64`, `96`, or `128`. Defaults to 128.

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### POST https://api.jina.ai/v1/rerank

**Rerank**

Score documents against a query and return them reordered.

Results come back sorted by `relevance_score`, each carrying the index
it held in the request so the caller can map them back.

Request body (`application/json`, required):
One of 3 shapes:
- `TextRerankerRequest`: Pointwise text reranker: scores each document against the query.
  - `query` (string, required): The search query to rank documents against.
  - `top_n` (integer | null): Number of top results to return. If not set, returns all documents.
  - `return_documents` (boolean | null, default true): If true (default), includes document content in each result.
  - `model` ("jina-reranker-v2-base-multilingual" | "jina-reranker-v1-tiny-en" | "jina-reranker-v1-turbo-en" | "jina-reranker-v1-base-en" | "jina-colbert-v1-en" | "jina-colbert-v2", required): The reranking model to use.
  - `documents` (array<string | TextDoc>, required): Documents to rank: strings or `TextDoc` objects.
- `RerankerM0Request`: Multimodal reranker: the query and the documents may each be text or an image.
  - `query` (string | ImageDoc, required): The query to rank documents against: a text string, or an image object (`{"image": <url|base64>}`) for a visual query.
  - `top_n` (integer | null): Number of top results to return. If not set, returns all documents.
  - `return_documents` (boolean | null, default true): If true (default), includes document content in each result.
  - `model` (string, required): The multimodal reranking model to use.
  - `documents` (array<string | TextDoc | ImageDoc>, required): Documents to rank: strings, `TextDoc`, or `ImageDoc` objects.
- `RerankerV3Request`: Listwise multilingual reranker: scores the candidate set as a whole rather than one document at a time.
  - `query` (string, required): The search query to rank documents against.
  - `top_n` (integer | null): Number of top results to return. If not set, returns all documents.
  - `return_documents` (boolean | null, default true): If true (default), includes document content in each result.
  - `model` ("jina-reranker-v3" | "jina-reranker-v3.5", required): The reranking model to use.
  - `documents` (array<string | TextDoc>, required): Documents to rank: strings or `TextDoc` objects.
  - `max_doc_length` (integer | null): Maximum tokens per document (1-8192). Omit to use the model's default (2048 for jina-reranker-v3, 8192 for jina-reranker-v3.5).
  - `return_embeddings` (boolean | null): If true, returns the document embedding alongside the relevance score.

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

### Generative Models

Document transcription over the OpenAI chat completions schema. Point any OpenAI-compatible client at the server URL above with `/v1` appended, set `model`, and send a page image; the response is the page as text or markdown, tables and layout preserved.

`stream: true` returns server-sent events. `response_format` with a `json_schema` constrains the output to that schema instead of prose. Parameters outside the supported set are accepted and ignored rather than rejected, so an SDK-generated payload always works.

#### POST https://api.jina.ai/v1/chat/completions

**Chat Completions**

Transcribe a document image. Send the page as an `image_url` content part and the reply is its text; `response_format` with a `json_schema` constrains that to a schema instead.

Request body (`application/json`, required):
- `messages` (array<ChatMessage>, required)
  - `role` ("system" | "developer" | "user" | "assistant", required)
  - `content` (string | array<TextContentPart | ImageContentPart> | null)
- `model` (string, required): The model to use.
- `stream` (boolean, default false)
- `stream_options` (StreamOptions | null)
- `max_completion_tokens` (integer | null)
- `temperature` (number | null)
- `top_p` (number | null)
- `presence_penalty` (number | null)
- `frequency_penalty` (number | null)
- `stop` (string | array<string> | null)
- `seed` (integer | null)
- `logprobs` (boolean | null)
- `top_logprobs` (integer | null)
- `logit_bias` (object | null)
- `response_format` (ResponseFormatText | ResponseFormatJSONObject | ResponseFormatJSONSchema | null)

Responses:
- `200`: An OpenAI chat completion, or a stream of `chat.completion.chunk` events when `stream` is true.
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

### Batch Embeddings

Asynchronous embedding for large workloads: up to 50,000 inputs from a GCS file URL, or 10,000 inline.

Submit with `POST /v1/batch/embeddings`, poll `GET /v1/batch/{batch_id}` until the status is `completed`, then fetch `GET /v1/batch/{batch_id}/output`. Input is OpenAI-compatible JSONL with `custom_id` and `body.input`. Output files expire after 24 hours, and a webhook can be called on completion.

#### POST https://api.jina.ai/v1/batch/embeddings

**Create a batch embedding job**

Submit a batch of texts for asynchronous embedding processing.

Request body (`application/json`, required):
- `model` ("jina-embeddings-v5-text-nano" | "jina-embeddings-v5-text-small", required): The embedding model to use for batch processing.
- `input_url` (string | null): URL to input JSONL file (GCS, S3, or HTTP). Either input_url or input must be provided.
- `input` (array<object> | null): Inline JSONL lines for small batches. Either input_url or input must be provided.
- `task` (string | null, default "text-matching"): Task optimization: retrieval, text-matching, clustering, or classification.
- `dimensions` (integer | null): Number of dimensions for output embeddings (1-1024).
- `normalized` (boolean | null, default true): If true (default), embeddings are L2-normalized to unit length.
- `webhook_url` (string | null): URL to POST notification when job completes.

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### GET https://api.jina.ai/v1/batch/{batch_id}

**Get batch job status**

Retrieve the status of a batch embedding job.

Parameters:
- `batch_id` (path, string, required)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### DELETE https://api.jina.ai/v1/batch/{batch_id}

**Cancel a batch job**

Cancel a pending or processing batch job.

Parameters:
- `batch_id` (path, string, required)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### GET https://api.jina.ai/v1/batches

**List batch jobs**

List recent batch jobs for the authenticated user.

Parameters:
- `limit` (query, integer, default 20)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### GET https://api.jina.ai/v1/batch/{batch_id}/output

**Download batch job output**

Stream the output JSONL file for a completed batch job.

Parameters:
- `batch_id` (path, string, required)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`

#### GET https://api.jina.ai/v1/batch/{batch_id}/errors

**Download batch job error file**

Stream the error JSONL file for a completed batch job.

Parameters:
- `batch_id` (path, string, required)

Responses:
- `200`: Successful Response
- `400`: Bad Request: `INPUT_INVALID_LABELS`, `INPUT_LABEL_LIMIT_EXCEEDED`, `INPUT_MODEL_NOT_FOUND`, `INPUT_TOKEN_LIMIT_EXCEEDED`
- `401`: Unauthorized: `AUTH_INVALID_API_KEY`, `AUTH_INVALID_FORMAT`, `AUTH_MISSING_API_KEY`
- `403`: Forbidden: `AUTHZ_INSUFFICIENT_BALANCE`, `AUTHZ_RESOURCE_LIMIT_EXCEEDED`
- `404`: Not Found: `RESOURCE_NOT_FOUND`
- `409`: Conflict: `CONFLICT_RESOURCE_BUSY`
- `422`: The request body failed schema validation. `errors` names each field.
- `429`: Too Many Requests: `RATE_CONCURRENCY_LIMIT_EXCEEDED`, `RATE_IP_LIMIT_EXCEEDED`, `RATE_REQUEST_LIMIT_EXCEEDED`, `RATE_TOKEN_LIMIT_EXCEEDED`
- `500`: Internal Server Error: `INTERNAL_ERROR`
- `503`: Service Unavailable: `SERVICE_UNAVAILABLE`
- `504`: Gateway Timeout: `SERVICE_TIMEOUT`
