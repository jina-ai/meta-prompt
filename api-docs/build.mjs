#!/usr/bin/env node
// Builds the API reference served at docs.jina.ai/api from the live OpenAPI specs of
// api.jina.ai, r.jina.ai and s.jina.ai. No dependencies, Node >= 18.
//
//   node api-docs/build.mjs
//
// Writes, next to this file:
//   openapi.json  the three specs merged into one (served at docs.jina.ai/api/openapi.json)
//   index.html    Scalar page that renders openapi.json (docs.jina.ai/api in a browser)
//   api.md        the same reference as Markdown (curl docs.jina.ai/api, docs.jina.ai/api.md)
//
// Outputs carry no timestamps, so a rebuild only changes files when a source spec changed.
import { writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = dirname(fileURLToPath(import.meta.url));
const SCALAR_VERSION = '1.74.0';
const METHODS = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'];
const KEY_URL = 'https://jina.ai/?sui=apikey';

const SOURCES = [
  {
    key: 'api',
    url: 'https://api.jina.ai/openapi.json',
    server: 'https://api.jina.ai',
    group: 'Search Foundation API (api.jina.ai)',
  },
  {
    key: 'reader',
    url: 'https://r.jina.ai/openapi.json',
    server: 'https://r.jina.ai',
    group: 'Reader API (r.jina.ai)',
    tag: 'Reader',
    prefix: 'Reader_',
    description: 'Read a URL and get its content back in an LLM-friendly format. Put the target URL after `https://r.jina.ai/`, or pass it as `url`. Most options are `X-*` request headers.',
    summaries: {
      '/': 'Read a URL',
      '/{url}': 'Read a URL (URL in path)',
      '/ephemeral/{encodedFid}': 'Get an ephemeral file',
    },
  },
  {
    key: 'search',
    url: 'https://s.jina.ai/openapi.json',
    server: 'https://s.jina.ai',
    group: 'Search API (s.jina.ai)',
    tag: 'Search',
    prefix: 'Search_',
    description: 'Search the web and get the results back in an LLM-friendly format. Put the query after `https://s.jina.ai/`, or pass it as `q`. Most options are `X-*` request headers.',
    summaries: {
      '/search': 'Search the web',
      '/{q}': 'Search the web (query in path)',
    },
  },
];

async function fetchSpec(src) {
  const res = await fetch(src.url, { headers: { accept: 'application/json' } });
  if (!res.ok) throw new Error(`${src.url}: HTTP ${res.status}`);
  return res.json();
}

// Rename every component schema to prefix + name, and rewrite the $refs that point at them.
function prefixSchemas(spec, prefix) {
  const text = JSON.stringify(spec).replace(
    /"#\/components\/schemas\/([^"]+)"/g,
    (_, name) => `"#/components/schemas/${prefix}${name}"`,
  );
  const out = JSON.parse(text);
  const schemas = (out.components && out.components.schemas) || {};
  out.components = {
    ...out.components,
    schemas: Object.fromEntries(Object.entries(schemas).map(([k, v]) => [prefix + k, v])),
  };
  return out;
}

const slug = (p) => p.replace(/[{}]/g, '').replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '') || 'root';

function merge(loaded) {
  const [base, ...rest] = loaded;
  const out = structuredClone(base.spec);
  const intro = [
    'One reference for three hosts, merged from each host\'s own OpenAPI spec:',
    '',
    ...SOURCES.map((s) => `- \`${new URL(s.server).host}\`: ${s.group.replace(/ \(.*\)$/, '')}, from ${s.url}`),
    '',
    `Every endpoint takes \`Authorization: Bearer <your Jina API key>\`. Get a key at ${KEY_URL}.`,
  ].join('\n');
  out.info = { ...out.info, title: 'Jina AI API', description: `${intro}\n\n${out.info.description || ''}`.trim() };
  out.servers = [{ url: base.src.server }];
  out.tags = [...(out.tags || [])];
  out.components = out.components || {};
  out.components.schemas = out.components.schemas || {};
  const groups = [{ name: base.src.group, tags: out.tags.map((t) => t.name) }];

  for (const { src, spec } of rest) {
    const s = prefixSchemas(spec, src.prefix);
    for (const [name, schema] of Object.entries(s.components.schemas)) {
      if (out.components.schemas[name]) throw new Error(`schema ${name} from ${src.url} already exists`);
      out.components.schemas[name] = schema;
    }
    for (const [p, item] of Object.entries(s.paths || {})) {
      if (out.paths[p]) throw new Error(`path ${p} from ${src.url} already exists`);
      const next = { ...item, servers: [{ url: src.server }] };
      for (const m of METHODS) {
        const op = next[m];
        if (!op) continue;
        op.tags = [src.tag];
        const fixed = src.summaries && src.summaries[p];
        if (fixed) op.summary = fixed;
        op.operationId = op.operationId || `${src.key}_${m}_${slug(p)}`;
        // The Authorization header param becomes the shared HTTPBearer scheme, so "Try it" reuses one key.
        const params = op.parameters || [];
        const auth = params.find((x) => x.in === 'header' && /^authorization$/i.test(x.name));
        if (auth) {
          op.parameters = params.filter((x) => x !== auth);
          op.security = auth.required ? [{ HTTPBearer: [] }] : [{ HTTPBearer: [] }, {}];
        }
      }
      out.paths[p] = next;
    }
    out.tags.push({ name: src.tag, description: src.description });
    groups.push({ name: src.group, tags: [src.tag] });
  }
  out['x-tagGroups'] = groups;
  return out;
}

function renderHtml() {
  const config = {
    url: '/api/openapi.json',
    proxyUrl: 'https://proxy.scalar.com',
    hideModels: true,
    defaultOpenAllTags: true,
    persistAuth: true,
    authentication: { preferredSecurityScheme: 'HTTPBearer' },
    metaData: {
      title: 'Jina AI API reference',
      description: 'Embeddings, reranking, Reader (r.jina.ai) and Search (s.jina.ai) in one reference.',
    },
    customCss: [
      ':root { --scalar-color-accent: #009191; --scalar-background-accent: #00919115; }',
      '.dark-mode { --scalar-color-accent: #81E3EE; --scalar-background-accent: #00919130; }',
    ].join('\n'),
  };
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jina AI API reference</title>
<meta name="description" content="${config.metaData.description}">
<link rel="icon" href="https://jina.ai/favicon.ico">
<link rel="alternate" type="text/markdown" href="/api.md">
</head>
<body>
<!-- Generated by api-docs/build.mjs in github.com/jina-ai/meta-prompt. Do not edit by hand. -->
<noscript>This page needs JavaScript. Plain text version: <a href="/api.md">docs.jina.ai/api.md</a>, OpenAPI spec: <a href="/api/openapi.json">docs.jina.ai/api/openapi.json</a>.</noscript>
<div id="app"></div>
<script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference@${SCALAR_VERSION}"></script>
<script>
Scalar.createApiReference('#app', ${JSON.stringify(config, null, 2)});
</script>
</body>
</html>
`;
}

function renderMarkdown(spec) {
  const lines = [];
  const resolve = (obj) => {
    let cur = obj;
    for (let hops = 0; cur && cur.$ref && hops < 10; hops++) {
      cur = cur.$ref.replace(/^#\//, '').split('/').map(decodeURIComponent)
        .reduce((node, key) => (node ? node[key] : undefined), spec);
    }
    return cur || {};
  };
  const one = (t) => String(t || '').replace(/\s+/g, ' ').trim();
  // Reader/Search schema names look like "Reader_PseudoBoolean@0x10"; show "PseudoBoolean".
  const refName = (ref) => decodeURIComponent(ref.split('/').pop())
    .replace(/^(Reader|Search)_/, '').replace(/@0x[0-9a-f]+$/i, '');
  const enumText = (values) => {
    const shown = values.slice(0, 12).map((v) => JSON.stringify(v));
    return shown.join(' | ') + (values.length > 12 ? ` | ... (${values.length} values)` : '');
  };
  const typeOf = (raw, depth = 0) => {
    if (!raw) return 'any';
    if (raw.$ref) {
      // Objects keep their schema name; enums and aliases of primitives show what they are.
      const d = resolve(raw);
      if (d.properties || d.allOf || depth > 3) return refName(raw.$ref);
      return typeOf(d, depth + 1);
    }
    const alt = raw.anyOf || raw.oneOf;
    if (alt) {
      const kinds = alt.filter((a) => a.type !== 'null').map((a) => typeOf(a, depth + 1));
      return kinds.join(' | ') + (alt.some((a) => a.type === 'null') ? ' | null' : '');
    }
    if (raw.allOf) return raw.allOf.map((a) => typeOf(a, depth + 1)).join(' & ');
    if (raw.enum) return enumText(raw.enum);
    if (raw.type === 'array') return `array<${typeOf(raw.items, depth + 1)}>`;
    if (Array.isArray(raw.type)) return raw.type.join(' | ');
    return raw.type || (raw.properties ? 'object' : 'any');
  };
  const facts = (raw, required) => {
    const d = resolve(raw);
    const bits = [typeOf(raw)];
    if (required) bits.push('required');
    if (d.default !== undefined) bits.push(`default ${JSON.stringify(d.default)}`);
    return bits.join(', ');
  };
  const fields = (raw, depth, pad) => {
    const s = resolve(raw);
    const parts = s.allOf ? s.allOf.map(resolve) : [s];
    const props = Object.assign({}, ...parts.map((x) => x.properties || {}));
    const req = new Set(parts.flatMap((x) => x.required || []));
    let count = 0;
    for (const [name, prop] of Object.entries(props)) {
      count++;
      const d = resolve(prop);
      const desc = one(prop.description || d.description);
      lines.push(`${pad}- \`${name}\` (${facts(prop, req.has(name))})${desc ? `: ${desc}` : ''}`);
      const inner = d.type === 'array' ? resolve(d.items) : d;
      if (depth < 2 && (inner.properties || inner.allOf)) fields(inner, depth + 1, `${pad}  `);
    }
    return count;
  };
  const renderOp = (methods, url, op, pathParams) => {
    lines.push(`#### ${methods} ${url}`, '');
    if (op.summary) lines.push(`${one(op.summary)}.`.replace(/\.\.$/, '.'), '');
    if (op.description) lines.push(op.description.trim(), '');
    if (op.security && op.security.some((s) => Object.keys(s).length === 0)) lines.push('Authentication: optional.', '');
    const params = [...(pathParams || []), ...(op.parameters || [])].map(resolve);
    if (params.length) {
      lines.push('Parameters:');
      for (const x of params) {
        const desc = one(x.description);
        lines.push(`- \`${x.name}\` (${x.in}, ${facts(x.schema, x.required)})${desc ? `: ${desc}` : ''}`);
      }
      lines.push('');
    }
    const body = op.requestBody && resolve(op.requestBody);
    if (body && body.content) {
      const types = Object.keys(body.content);
      const ct = types.find((t) => t.includes('json')) || types[0];
      lines.push(`Request body (\`${ct}\`${body.required ? ', required' : ''}):`);
      const schema = body.content[ct].schema;
      if (!fields(schema, 0, '')) {
        // A union of request shapes (e.g. one per model): list each shape with its fields.
        const top = resolve(schema);
        const variants = (top.anyOf || top.oneOf || []).filter((v) => resolve(v).properties || resolve(v).allOf);
        if (variants.length) {
          lines.push(`One of ${variants.length} shapes:`);
          for (const v of variants) {
            const d = resolve(v);
            const desc = one(d.description).split('. ')[0];
            lines.push(`- \`${typeOf(v)}\`${desc ? `: ${desc.replace(/\.$/, '')}.` : ''}`);
            fields(v, 1, '  ');
          }
        } else {
          lines.push(`- ${typeOf(schema)}`);
        }
      }
      lines.push('');
    }
    const responses = Object.entries(op.responses || {});
    if (responses.length) {
      lines.push('Responses:');
      for (const [code, r] of responses) lines.push(`- \`${code}\`: ${one(resolve(r).description)}`);
      lines.push('');
    }
  };

  lines.push(
    '# Jina AI API reference',
    '',
    `Generated from ${SOURCES.map((s) => s.url).join(', ')}.`,
    'Interactive version: https://docs.jina.ai/api. Merged OpenAPI spec: https://docs.jina.ai/api/openapi.json.',
    `Authentication: \`Authorization: Bearer <your Jina API key>\`. Get a key at ${KEY_URL}.`,
    '',
  );
  for (const group of spec['x-tagGroups']) {
    lines.push(`## ${group.name}`, '');
    for (const tagName of group.tags) {
      const tag = (spec.tags || []).find((t) => t.name === tagName);
      lines.push(`### ${tagName}`, '');
      if (tag && tag.description) lines.push(tag.description.trim().replace(/^#+ /gm, '**') , '');
      for (const [p, item] of Object.entries(spec.paths)) {
        const server = ((item.servers && item.servers[0].url) || spec.servers[0].url).replace(/\/$/, '');
        const ops = METHODS.filter((m) => item[m] && (item[m].tags || []).includes(tagName));
        const seen = new Set();
        for (const m of ops) {
          if (seen.has(m)) continue;
          // Methods whose docs are identical apart from operationId share one entry, e.g. "GET, POST".
          const sig = (o) => JSON.stringify({ ...item[o], operationId: undefined });
          const same = ops.filter((o) => !seen.has(o) && sig(o) === sig(m));
          same.forEach((o) => seen.add(o));
          renderOp(same.map((o) => o.toUpperCase()).join(', '), server + p, item[m], item.parameters);
        }
      }
    }
  }
  return `${lines.join('\n').replace(/\n{3,}/g, '\n\n').trim()}\n`;
}

const loaded = await Promise.all(SOURCES.map(async (src) => ({ src, spec: await fetchSpec(src) })));
const merged = merge(loaded);
await writeFile(join(OUT, 'openapi.json'), `${JSON.stringify(merged, null, 2)}\n`);
await writeFile(join(OUT, 'index.html'), renderHtml());
await writeFile(join(OUT, 'api.md'), renderMarkdown(merged));
const ops = Object.values(merged.paths).reduce((n, item) => n + METHODS.filter((m) => item[m]).length, 0);
console.log(`api-docs: ${Object.keys(merged.paths).length} paths, ${ops} operations, ${Object.keys(merged.components.schemas).length} schemas`);
