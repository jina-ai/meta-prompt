#!/usr/bin/env node
// Builds the API reference served at docs.jina.ai/api from the live OpenAPI specs of
// api.jina.ai, r.jina.ai and s.jina.ai. No dependencies, Node >= 18.
//
//   node api-docs/build.mjs
//
// Hand-written inputs (never touched by this script, so edits survive every rebuild):
//   intro.md       intro block with the navigation table, shown first on the page and in api.md
//   overrides.mjs  order, hidden operations, and summaries/descriptions for operations and parameters
//
// Generated outputs, next to this file:
//   openapi.json   the three specs merged into one (docs.jina.ai/api/openapi.json)
//   index.html     Scalar page that renders openapi.json (docs.jina.ai/api in a browser)
//   api.md         the same reference as Markdown (curl docs.jina.ai/api, docs.jina.ai/api.md)
//   coverage.md    visible parameters that still have no description
//
// Outputs carry no timestamps, so a rebuild only changes files when an input changed.
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = dirname(fileURLToPath(import.meta.url));
const SCALAR_VERSION = '1.74.0';
const METHODS = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'];
const PAGE_URL = 'https://docs.jina.ai/api';

const overrides = (await import('./overrides.mjs')).default;
const introMd = (await readFile(join(OUT, 'intro.md'), 'utf8')).trim();

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
    description: 'Read a URL and get its content back in an LLM-friendly format.',
  },
  {
    key: 'search',
    url: 'https://s.jina.ai/openapi.json',
    server: 'https://s.jina.ai',
    group: 'Search API (s.jina.ai)',
    tag: 'Search',
    prefix: 'Search_',
    description: 'Search the web and get the result pages back in an LLM-friendly format.',
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
// "X-With-Links-Summary", "withLinksSummary" and "withlinkssummary" all become "withlinkssummary".
const norm = (name) => String(name).toLowerCase().replace(/^x-/, '').replace(/[^a-z0-9]/g, '');
const hasText = (s) => typeof s === 'string' && s.trim().length > 0;
// Reader/Search specs pad descriptions with generated lines ("- Cast to: < string >",
// "- Member of <CrawlerOptions>", ...). They explain nothing, so they are dropped; a param left
// with no text counts as undocumented and gets its header twin's text or an override.
const NOISE = /^\s*-\s*(Cast to|Member of|Endpoint parameter of|Defaults to|Sub-?type of|Type)\b/i;
const clean = (s) => (typeof s === 'string'
  ? s.split('\n').filter((line) => !NOISE.test(line)).join('\n').replace(/\n{3,}/g, '\n\n').trim()
  : s);
const paramDesc = (p) => (hasText(p.description) ? p.description : (p.schema && hasText(p.schema.description) ? p.schema.description : ''));

function merge(loaded) {
  const used = new Set();
  const opOverride = (key) => {
    const o = overrides.operations && overrides.operations[key];
    if (o) used.add(`operations['${key}']`);
    return o;
  };
  const paramOverride = (srcKey, name) => {
    const d = overrides.parameters && overrides.parameters[srcKey] && overrides.parameters[srcKey][name];
    if (d) used.add(`parameters.${srcKey}.${name}`);
    return d;
  };

  // Many Reader/Search query params are undocumented while their X-* header twin is documented;
  // the twin's text is reused. Overrides win over both.
  const headerDescs = (spec) => {
    const map = {};
    for (const item of Object.values(spec.paths || {})) {
      for (const m of METHODS) {
        for (const p of (item[m] && item[m].parameters) || []) {
          const d = clean(p.description);
          if (p.in === 'header' && hasText(d) && !map[norm(p.name)]) map[norm(p.name)] = d;
        }
      }
    }
    return map;
  };
  const lookup = (map, name) => map[norm(name)] || map[norm(name).replace(/s$/, '')] || '';

  const annotateOps = (srcKey, paths, twins) => {
    for (const [p, item] of Object.entries(paths)) {
      for (const m of METHODS) {
        const op = item[m];
        if (!op) continue;
        const o = opOverride(`${srcKey} ${m.toUpperCase()} ${p}`);
        if (o) {
          if (o.summary) op.summary = o.summary;
          if (o.description) op.description = o.description;
          if (o.hidden) op['x-scalar-ignore'] = true;
        }
        for (const param of op.parameters || []) {
          if (param.$ref) continue;
          if (twins) {
            param.description = clean(param.description);
            if (param.schema) param.schema.description = clean(param.schema.description);
            if (!hasText(param.description)) delete param.description;
            if (param.schema && !hasText(param.schema.description)) delete param.schema.description;
          }
          const ov = paramOverride(srcKey, param.name);
          if (ov) param.description = ov;
          else if (!paramDesc(param) && twins) {
            const twin = lookup(twins, param.name);
            if (twin) param.description = twin;
          }
        }
      }
    }
  };
  const annotateSchemas = (srcKey, schemas, twins) => {
    for (const schema of Object.values(schemas)) {
      for (const [name, prop] of Object.entries(schema.properties || {})) {
        if (twins) {
          prop.description = clean(prop.description);
          if (!hasText(prop.description)) delete prop.description;
        }
        const ov = paramOverride(srcKey, name);
        if (ov) prop.description = ov;
        else if (!hasText(prop.description) && twins) {
          const twin = lookup(twins, name);
          if (twin) prop.description = twin;
        }
      }
    }
  };

  const parts = {};
  for (const { src, spec } of loaded) {
    if (src.key === 'api') {
      const s = structuredClone(spec);
      annotateOps('api', s.paths, null);
      annotateSchemas('api', (s.components && s.components.schemas) || {}, null);
      parts.api = {
        paths: s.paths,
        schemas: (s.components && s.components.schemas) || {},
        tags: s.tags || [],
        group: { name: src.group, tags: (s.tags || []).map((t) => t.name) },
      };
      continue;
    }
    const twins = headerDescs(spec);
    const s = prefixSchemas(spec, src.prefix);
    // Request bodies are often inline schemas inside the operation, so walk the whole spec:
    // scrub every description, then fill every object that has properties.
    const holders = [];
    const walk = (node) => {
      if (!node || typeof node !== 'object') return;
      if (typeof node.description === 'string') {
        node.description = clean(node.description);
        if (!hasText(node.description)) delete node.description;
      }
      if (node.properties && typeof node.properties === 'object') holders.push(node);
      for (const v of Object.values(node)) walk(v);
    };
    walk(s);
    annotateSchemas(src.key, holders, twins);
    const paths = {};
    for (const [p, item] of Object.entries(s.paths || {})) {
      const next = { ...item, servers: [{ url: src.server }] };
      for (const m of METHODS) {
        const op = next[m];
        if (!op) continue;
        op.tags = [src.tag];
        op.operationId = op.operationId || `${src.key}_${m}_${slug(p)}`;
        // The Authorization header param becomes the shared HTTPBearer scheme, so "Try it" reuses one key.
        const params = op.parameters || [];
        const auth = params.find((x) => x.in === 'header' && /^authorization$/i.test(x.name));
        if (auth) {
          op.parameters = params.filter((x) => x !== auth);
          op.security = auth.required ? [{ HTTPBearer: [] }] : [{ HTTPBearer: [] }, {}];
        }
      }
      paths[p] = next;
    }
    annotateOps(src.key, paths, twins);
    parts[src.key] = {
      paths,
      schemas: s.components.schemas,
      tags: [{ name: src.tag, description: src.description }],
      group: { name: src.group, tags: [src.tag] },
    };
  }

  const order = [...(overrides.order || []), ...SOURCES.map((s) => s.key)]
    .filter((k, i, all) => parts[k] && all.indexOf(k) === i);
  const base = loaded.find((l) => l.src.key === 'api').spec;
  const out = structuredClone(base);
  out.info = {
    ...out.info,
    title: 'Jina AI API',
    description: [
      introMd,
      `_Merged from ${SOURCES.map((s) => s.url).join(', ')}. Plain text: ${PAGE_URL}.md. Spec: ${PAGE_URL}/openapi.json._`,
      out.info.description || '',
    ].join('\n\n').trim(),
  };
  out.servers = [{ url: SOURCES.find((s) => s.key === 'api').server }];
  out.paths = {};
  out.components = { ...(out.components || {}), schemas: {} };
  out.tags = [];
  for (const k of order) {
    for (const [p, item] of Object.entries(parts[k].paths)) {
      if (out.paths[p]) throw new Error(`path ${p} from ${k} already exists`);
      out.paths[p] = item;
    }
    for (const [name, schema] of Object.entries(parts[k].schemas)) {
      if (out.components.schemas[name]) throw new Error(`schema ${name} from ${k} already exists`);
      out.components.schemas[name] = schema;
    }
    out.tags.push(...parts[k].tags);
  }
  for (const tag of out.tags) {
    const o = overrides.tags && overrides.tags[tag.name];
    if (o) {
      used.add(`tags['${tag.name}']`);
      if (o.description) tag.description = o.description;
    }
  }
  out['x-tagGroups'] = order.map((k) => parts[k].group);

  const declared = [
    ...Object.keys(overrides.operations || {}).map((k) => `operations['${k}']`),
    ...Object.entries(overrides.parameters || {}).flatMap(([s, ps]) => Object.keys(ps).map((n) => `parameters.${s}.${n}`)),
    ...Object.keys(overrides.tags || {}).map((k) => `tags['${k}']`),
  ];
  const stale = declared.filter((k) => !used.has(k));
  return { spec: out, stale };
}

// Visible operations whose params or top-level body fields have no description.
function coverage(spec) {
  const resolve = makeResolver(spec);
  const lines = ['# Undocumented parameters', '', 'Visible operations only. Add the missing texts to `api-docs/overrides.mjs`; they survive every rebuild.', ''];
  let missing = 0;
  let total = 0;
  for (const [p, item] of Object.entries(spec.paths)) {
    const host = ((item.servers && item.servers[0].url) || spec.servers[0].url).replace(/^https:\/\//, '').replace(/\/$/, '');
    for (const m of METHODS) {
      const op = item[m];
      if (!op || op['x-scalar-ignore']) continue;
      const gaps = [];
      for (const param of [...(item.parameters || []), ...(op.parameters || [])].map(resolve)) {
        total++;
        if (!paramDesc(param)) gaps.push(`${param.in} \`${param.name}\``);
      }
      const body = op.requestBody && resolve(op.requestBody);
      const json = body && body.content && (body.content['application/json'] || Object.values(body.content)[0]);
      if (json) {
        const top = resolve(json.schema);
        const shapes = top.properties ? [top] : (top.anyOf || top.oneOf || []).map(resolve);
        const seen = new Set();
        for (const shape of shapes) {
          for (const [name, prop] of Object.entries(shape.properties || {})) {
            if (seen.has(name)) continue;
            seen.add(name);
            total++;
            if (!hasText(prop.description) && !hasText(resolve(prop).description)) gaps.push(`body \`${name}\``);
          }
        }
      }
      if (gaps.length) {
        missing += gaps.length;
        lines.push(`## ${m.toUpperCase()} ${host}${p}`, '', ...gaps.map((g) => `- ${g}`), '');
      }
    }
  }
  lines.splice(4, 0, `${missing} of ${total} parameters and body fields have no description.`, '');
  return { text: `${lines.join('\n').trim()}\n`, missing, total };
}

function makeResolver(spec) {
  return (obj) => {
    let cur = obj;
    for (let hops = 0; cur && cur.$ref && hops < 10; hops++) {
      cur = cur.$ref.replace(/^#\//, '').split('/').map(decodeURIComponent)
        .reduce((node, key) => (node ? node[key] : undefined), spec);
    }
    return cur || {};
  };
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
      description: 'Reader (r.jina.ai), Search (s.jina.ai), embeddings and reranking in one reference.',
    },
    customCss: [
      ':root { --scalar-color-accent: #009191; --scalar-background-accent: #00919115; }',
      '.dark-mode { --scalar-color-accent: #81E3EE; --scalar-background-accent: #00919130; }',
      '.markdown table { font-size: 0.95em; }',
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
  const resolve = makeResolver(spec);
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
      const kinds = [...new Set(alt.filter((a) => a.type !== 'null').map((a) => typeOf(a, depth + 1)))];
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
  const renderOp = (method, url, op, pathParams) => {
    lines.push(`#### ${method} ${url}`, '');
    if (op.summary) lines.push(`**${one(op.summary).replace(/\.$/, '')}**`, '');
    if (op.description) lines.push(op.description.trim(), '');
    if (op.security && op.security.some((s) => Object.keys(s).length === 0)) lines.push('Authentication: optional.', '');
    const params = [...(pathParams || []), ...(op.parameters || [])].map(resolve);
    if (params.length) {
      lines.push('Parameters:');
      for (const x of params) {
        const desc = one(paramDesc(x));
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

  // Page-relative links (#tag/...) from intro.md point at the interactive page in plain text.
  const absolute = (md) => md.replace(/\]\(#/g, `](${PAGE_URL}#`);
  lines.push('# Jina AI API reference', '', absolute(spec.info.description).replace(/^(#{1,5}) /gm, '#$1 '), '');
  for (const group of spec['x-tagGroups']) {
    lines.push(`## ${group.name}`, '');
    for (const tagName of group.tags) {
      const tag = (spec.tags || []).find((t) => t.name === tagName);
      lines.push(`### ${tagName}`, '');
      if (tag && tag.description) lines.push(absolute(tag.description.trim()).replace(/^#+ /gm, '**'), '');
      for (const [p, item] of Object.entries(spec.paths)) {
        const server = ((item.servers && item.servers[0].url) || spec.servers[0].url).replace(/\/$/, '');
        for (const m of METHODS) {
          const op = item[m];
          if (!op || op['x-scalar-ignore'] || !(op.tags || []).includes(tagName)) continue;
          renderOp(m.toUpperCase(), server + p, op, item.parameters);
        }
      }
    }
  }
  return `${lines.join('\n').replace(/\n{3,}/g, '\n\n').trim()}\n`;
}

const loaded = await Promise.all(SOURCES.map(async (src) => ({ src, spec: await fetchSpec(src) })));
const { spec: merged, stale } = merge(loaded);
const cov = coverage(merged);
await writeFile(join(OUT, 'openapi.json'), `${JSON.stringify(merged, null, 2)}\n`);
await writeFile(join(OUT, 'index.html'), renderHtml());
await writeFile(join(OUT, 'api.md'), renderMarkdown(merged));
await writeFile(join(OUT, 'coverage.md'), cov.text);
const ops = Object.values(merged.paths).flatMap((item) => METHODS.filter((m) => item[m]).map((m) => item[m]));
const visible = ops.filter((op) => !op['x-scalar-ignore']).length;
console.log(`api-docs: ${ops.length} operations (${visible} shown), ${Object.keys(merged.components.schemas).length} schemas, ${cov.missing}/${cov.total} parameters undocumented (see coverage.md)`);
for (const key of stale) console.warn(`warning: overrides.mjs ${key} matches nothing in the current specs`);
