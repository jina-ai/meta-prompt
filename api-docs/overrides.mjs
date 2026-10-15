// Hand-written layer on top of the live OpenAPI specs. build.mjs never writes this file,
// so anything here survives every rebuild. Edit freely, then run `node api-docs/build.mjs`.
//
// Keys:
//   order       source order in the sidebar and in api.md (keys of SOURCES in build.mjs)
//   operations  '<source> <METHOD> <path>' -> { summary, description, hidden }
//               hidden operations stay callable but are left out of the page and api.md
//   parameters  '<source>' -> { <name>: description }, for query/header/path params and
//               request-body fields of that source; replaces whatever the spec says
//   tags        '<tag>' -> { description }
//
// The intro block with the navigation table is api-docs/intro.md.
// After a build, api-docs/coverage.md lists every visible parameter that still has no
// description, and the build warns about keys here that no longer match anything.
//
// Sources for the texts below: the meta-prompt (v14.txt) and github.com/jina-ai/reader.

export default {
  order: ['reader', 'search', 'api'],

  operations: {
    'reader GET /{url}': {
      summary: 'Read a URL',
      description: [
        'Put the target URL right after `https://r.jina.ai/`, e.g. `https://r.jina.ai/https://example.com`.',
        'Returns the page as LLM-friendly Markdown. Every option is an `X-*` header, or the query parameter of the same name.',
      ].join('\n\n'),
    },
    'reader POST /': {
      summary: 'Read a URL (JSON body)',
      description: [
        'Send `{"url": "..."}` as JSON, with the same `X-*` headers as the GET form.',
        '`Accept: application/json` returns JSON: the content is in `data.content`, and with `X-With-Links-Summary` / `X-With-Images-Summary` the links and images are in `data.links` and `data.images`. `Accept: text/event-stream` streams the result.',
      ].join('\n\n'),
    },
    'reader GET /': { hidden: true },
    'reader POST /{url}': { hidden: true },
    'reader GET /ephemeral/{encodedFid}': { hidden: true },
    'reader POST /ephemeral/{encodedFid}': { hidden: true },

    'search GET /{q}': {
      summary: 'Search the web',
      description: [
        'Put the query right after `https://s.jina.ai/`, e.g. `https://s.jina.ai/jina%20ai`.',
        'Returns the top results with each page\'s content as LLM-friendly text. `X-Respond-With: no-content` returns the results without page content; `X-Site` keeps results to one domain.',
      ].join('\n\n'),
    },
    'search POST /search': {
      summary: 'Search the web (JSON body)',
      description: 'Send `{"q": "..."}` as JSON, optionally with `gl`, `hl`, `location`, `num` and `page`. Same `X-*` headers as the GET form.',
    },
    'search POST /{q}': { hidden: true },
    'search GET /search': { hidden: true },
  },

  parameters: {
    reader: {
      url: 'The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).',
      html: 'Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.',
      file: 'Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.',
      noGfm: 'Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.',
      setCookies: 'Cookies to send when fetching the URL, for pages that need a login. Requests with cookies are not cached.',
      injectPageScript: 'JavaScript to run in the page before extraction, inline or as a URL, e.g. to change the DOM.',
      injectFrameScript: 'Like `injectPageScript`, for frames.',
    },
    search: {
      q: 'The search query. Not needed when the query is already in the path (`https://s.jina.ai/<query>`).',
      gl: 'Country to search from, as a two-letter country code.',
      hl: 'Language of the search, as a two-letter language code.',
      location: 'Where the search should originate from. City level works best.',
      num: 'Maximum number of results, 0 to 20, default 10. Larger values can add latency and drop special result types.',
      count: 'Same as `num`.',
      type: 'Result type: `web` (default), `images` or `news`.',
      provider: 'Search engine to use: `google`, `bing` or `reader`.',
      fallback: 'If `true` and the search returns nothing, fall back to local search results. Default `false`.',
      nfpr: 'Passed to the search engine; on Google, `true` turns off query auto-correction.',
      site: 'Keep results to this domain, e.g. `https://jina.ai`. Same as the `X-Site` header.',
      filetype: 'Search operator `filetype:`, e.g. `pdf`.',
      ext: 'Search operator `ext:` (file extension).',
      intitle: 'Search operator `intitle:`: words that must appear in the page title.',
      loc: 'Search operator `loc:` (location).',
      url: 'The URL to read. Not needed when the URL is already in the path (`https://r.jina.ai/<url>`).',
      html: 'Raw HTML to convert, instead of fetching a URL. Used when no `url` is given.',
      file: 'Base64-encoded file (PDF, DOC, XLS, PPT, ...) to convert instead of a URL.',
      noGfm: 'Opt out of GitHub Flavored Markdown. `true` disables GFM; `table` drops only GFM tables and keeps the table HTML.',
      setCookies: 'Cookies to send when fetching each result page, for pages that need a login. Requests with cookies are not cached.',
      injectPageScript: 'JavaScript to run in each result page before extraction, inline or as a URL.',
      injectFrameScript: 'Like `injectPageScript`, for frames.',
    },
  },

  tags: {},
};
