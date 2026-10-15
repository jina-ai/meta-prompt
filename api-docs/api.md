# Jina AI API reference

Generated from https://api.jina.ai/openapi.json, https://r.jina.ai/openapi.json, https://s.jina.ai/openapi.json.
Interactive version: https://docs.jina.ai/api. Merged OpenAPI spec: https://docs.jina.ai/api/openapi.json.
Authentication: `Authorization: Bearer <your Jina API key>`. Get a key at https://jina.ai/?sui=apikey.

## Search Foundation API (api.jina.ai)

### Model List

Every model this API serves, in OpenRouter-compatible form: identifiers, input and output modalities, context lengths and prices. Read it before hardcoding a model name — the catalogue moves.

#### GET https://api.jina.ai/v1/models

List Models.

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

Get Model.

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

Embeddings.

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

Rerank.

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

Chat Completions.

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

Create a batch embedding job.

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

Get batch job status.

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

Cancel a batch job.

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

List batch jobs.

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

Download batch job output.

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

Download batch job error file.

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

## Reader API (r.jina.ai)

### Reader

Read a URL and get its content back in an LLM-friendly format. Put the target URL after `https://r.jina.ai/`, or pass it as `url`. Most options are `X-*` request headers.

#### GET https://r.jina.ai/

Read a URL.

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string)
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
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

#### POST https://r.jina.ai/

Read a URL.

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string)
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `preloadUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `noServiceWorker` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `html` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `base` ("initial" | "final", default "initial"): - Cast to: &lt; **&quot;initial&quot; | &quot;final&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;initial&#39;
- `pdf` (string | string): Base64 encoded PDF. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `file` (string | string): Base64 encoded file. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `page` (number): Steer which page to return for document files (1-indexed). - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; Number.isInteger(v) &amp;&amp; v &gt;= 1
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): - Cast to: &lt; **&quot;content&quot; | &quot;markdown&quot; | &quot;html&quot; | &quot;text&quot; | &quot;pageshot&quot; | &quot;screenshot&quot; | &quot;vlm&quot; | &quot;readerlm-v2&quot; | &quot;frontmatter&quot; | &quot;readability&quot; | &quot;...|string** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;content&#39;
- `withGeneratedAlt` (boolean | string): - Cast to: &lt; **PseudoBoolean** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;alt&quot; | &quot;all_p&quot; | &quot;alt_p&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): - Cast to: &lt; **&quot;none&quot; | &quot;text&quot; | &quot;link&quot; | &quot;image&quot; | &quot;html&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;link&#39;
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): - Cast to: &lt; **&quot;reader&quot; | &quot;index&quot; | &quot;research&quot; | &quot;agent&quot; | &quot;spider&quot; | &quot;ocr&quot; | &quot;ocr+&quot; | &quot;ocr++&quot; | &quot;pdf&quot; | &quot;pdf+&quot; | &quot;pdf++&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;text&quot; | &quot;gpt-oss&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `withLinksSummary` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withImagesSummary` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noCache` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeOverlay` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `detachInvisibles` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noGfm` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `cacheTolerance` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `targetSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `waitForSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `keepImgDataUrl` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `withIframe` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withShadowDom` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `skipCertVerification` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `setCookies` (array<any | string>): - Cast to: &lt; **Array&lt;object|string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `storageState` (StorageState): - Cast to: &lt; **StorageState** &gt; - Member of &lt;CrawlerOptions&gt;
  - `cookies` (array<Cookie>, default []): - Cast to: &lt; **Array&lt;Cookie&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `name` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `value` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `domain` (string): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `path` (string, default "/"): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt; - Defaults to: &#39;/&#39;
    - `expires` (string): - Cast to: &lt; **Date** &gt; - Member of &lt;Cookie&gt;
    - `httpOnly` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `secure` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `sameSite` ("Strict" | "Lax" | "None" | string): - Cast to: &lt; **&quot;Strict&quot; | &quot;Lax&quot; | &quot;None&quot;|string** &gt; - Member of &lt;Cookie&gt;
  - `origins` (array<LocalStorageOrigin>, default []): - Cast to: &lt; **Array&lt;LocalStorageOrigin&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `origin` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;LocalStorageOrigin&gt;
    - `localStorage` (array<LocalStorageItem>, default []): - Cast to: &lt; **Array&lt;LocalStorageItem&gt;** &gt; - Member of &lt;LocalStorageOrigin&gt; - Defaults to: []
- `exportStorageState` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyResources` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxy` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `userAgent` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `engine` ("auto" | "browser" | "curl" | "cf-browser-rendering" | string): - Cast to: &lt; **&quot;auto&quot; | &quot;browser&quot; | &quot;curl&quot; | &quot;cf-browser-rendering&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectPageScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectFrameScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `timeout` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `referer` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `tokenBudget` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `assertStatusCode` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `viewport` (Viewport): - Cast to: &lt; **Viewport** &gt; - Member of &lt;CrawlerOptions&gt;
  - `width` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `height` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `deviceScaleFactor` (number): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt;
  - `isMobile` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `isLandscape` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `hasTouch` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
- `instruction` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object. - Cast to: &lt; **object** &gt; - Member of &lt;CrawlerOptions&gt;
- `robotsTxt` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `zeroDataRetention` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdown` (TurnDownTweakableOptions): - Cast to: &lt; **TurnDownTweakableOptions** &gt; - Member of &lt;CrawlerOptions&gt;
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle - Cast to: &lt; **&quot;setext&quot; | &quot;atx&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `hr` (string): Turndown options > hr - Cast to: &lt; **string** &gt; - Member of &lt;TurnDownTweakableOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker - Cast to: &lt; **&quot;-&quot; | &quot;+&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter - Cast to: &lt; **&quot;_&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter - Cast to: &lt; **&quot;__&quot; | &quot;**&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle - Cast to: &lt; **&quot;inlined&quot; | &quot;referenced&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle - Cast to: &lt; **&quot;full&quot; | &quot;collapsed&quot; | &quot;shortcut&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
- `ocr` (OCRPreferences): - Cast to: &lt; **OCRPreferences** &gt; - Member of &lt;CrawlerOptions&gt;
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): - Cast to: &lt; **&quot;html&quot; | &quot;visible-content&quot; | &quot;mutation-idle&quot; | &quot;resource-idle&quot; | &quot;media-idle&quot; | &quot;network-idle&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): - Cast to: &lt; **&quot;true&quot; | &quot;h1&quot; | &quot;h2&quot; | &quot;h3&quot; | &quot;h4&quot; | &quot;h5&quot; | &quot;structured&quot; | &quot;s1&quot; | &quot;s2&quot; | &quot;s3&quot; | &quot;s4&quot; | &quot;s5&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `maxTokens` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object): - Cast to: &lt; **Record&lt;string, string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;

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

Read a URL (URL in path).

Authentication: optional.

Parameters:
- `url` (path, string, required)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string)
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
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

#### POST https://r.jina.ai/{url}

Read a URL (URL in path).

Authentication: optional.

Parameters:
- `url` (path, string, required)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "auto" | "browser" | "curl" | "cf-browser-rendering" | string)
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `preloadUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `noServiceWorker` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `html` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `base` ("initial" | "final", default "initial"): - Cast to: &lt; **&quot;initial&quot; | &quot;final&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;initial&#39;
- `pdf` (string | string): Base64 encoded PDF. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `file` (string | string): Base64 encoded file. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `page` (number): Steer which page to return for document files (1-indexed). - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; Number.isInteger(v) &amp;&amp; v &gt;= 1
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): - Cast to: &lt; **&quot;content&quot; | &quot;markdown&quot; | &quot;html&quot; | &quot;text&quot; | &quot;pageshot&quot; | &quot;screenshot&quot; | &quot;vlm&quot; | &quot;readerlm-v2&quot; | &quot;frontmatter&quot; | &quot;readability&quot; | &quot;...|string** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;content&#39;
- `withGeneratedAlt` (boolean | string): - Cast to: &lt; **PseudoBoolean** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;alt&quot; | &quot;all_p&quot; | &quot;alt_p&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): - Cast to: &lt; **&quot;none&quot; | &quot;text&quot; | &quot;link&quot; | &quot;image&quot; | &quot;html&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;link&#39;
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): - Cast to: &lt; **&quot;reader&quot; | &quot;index&quot; | &quot;research&quot; | &quot;agent&quot; | &quot;spider&quot; | &quot;ocr&quot; | &quot;ocr+&quot; | &quot;ocr++&quot; | &quot;pdf&quot; | &quot;pdf+&quot; | &quot;pdf++&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;text&quot; | &quot;gpt-oss&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `withLinksSummary` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withImagesSummary` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noCache` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeOverlay` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `detachInvisibles` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noGfm` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `cacheTolerance` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `targetSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `waitForSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `keepImgDataUrl` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `withIframe` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withShadowDom` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `skipCertVerification` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `setCookies` (array<any | string>): - Cast to: &lt; **Array&lt;object|string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `storageState` (StorageState): - Cast to: &lt; **StorageState** &gt; - Member of &lt;CrawlerOptions&gt;
  - `cookies` (array<Cookie>, default []): - Cast to: &lt; **Array&lt;Cookie&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `name` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `value` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `domain` (string): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `path` (string, default "/"): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt; - Defaults to: &#39;/&#39;
    - `expires` (string): - Cast to: &lt; **Date** &gt; - Member of &lt;Cookie&gt;
    - `httpOnly` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `secure` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `sameSite` ("Strict" | "Lax" | "None" | string): - Cast to: &lt; **&quot;Strict&quot; | &quot;Lax&quot; | &quot;None&quot;|string** &gt; - Member of &lt;Cookie&gt;
  - `origins` (array<LocalStorageOrigin>, default []): - Cast to: &lt; **Array&lt;LocalStorageOrigin&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `origin` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;LocalStorageOrigin&gt;
    - `localStorage` (array<LocalStorageItem>, default []): - Cast to: &lt; **Array&lt;LocalStorageItem&gt;** &gt; - Member of &lt;LocalStorageOrigin&gt; - Defaults to: []
- `exportStorageState` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyResources` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxy` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `userAgent` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `engine` ("auto" | "browser" | "curl" | "cf-browser-rendering" | string): - Cast to: &lt; **&quot;auto&quot; | &quot;browser&quot; | &quot;curl&quot; | &quot;cf-browser-rendering&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectPageScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectFrameScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `timeout` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `referer` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `tokenBudget` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `assertStatusCode` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `viewport` (Viewport): - Cast to: &lt; **Viewport** &gt; - Member of &lt;CrawlerOptions&gt;
  - `width` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `height` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `deviceScaleFactor` (number): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt;
  - `isMobile` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `isLandscape` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `hasTouch` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
- `instruction` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object. - Cast to: &lt; **object** &gt; - Member of &lt;CrawlerOptions&gt;
- `robotsTxt` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `zeroDataRetention` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdown` (TurnDownTweakableOptions): - Cast to: &lt; **TurnDownTweakableOptions** &gt; - Member of &lt;CrawlerOptions&gt;
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle - Cast to: &lt; **&quot;setext&quot; | &quot;atx&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `hr` (string): Turndown options > hr - Cast to: &lt; **string** &gt; - Member of &lt;TurnDownTweakableOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker - Cast to: &lt; **&quot;-&quot; | &quot;+&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter - Cast to: &lt; **&quot;_&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter - Cast to: &lt; **&quot;__&quot; | &quot;**&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle - Cast to: &lt; **&quot;inlined&quot; | &quot;referenced&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle - Cast to: &lt; **&quot;full&quot; | &quot;collapsed&quot; | &quot;shortcut&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
- `ocr` (OCRPreferences): - Cast to: &lt; **OCRPreferences** &gt; - Member of &lt;CrawlerOptions&gt;
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): - Cast to: &lt; **&quot;html&quot; | &quot;visible-content&quot; | &quot;mutation-idle&quot; | &quot;resource-idle&quot; | &quot;media-idle&quot; | &quot;network-idle&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): - Cast to: &lt; **&quot;true&quot; | &quot;h1&quot; | &quot;h2&quot; | &quot;h3&quot; | &quot;h4&quot; | &quot;h5&quot; | &quot;structured&quot; | &quot;s1&quot; | &quot;s2&quot; | &quot;s3&quot; | &quot;s4&quot; | &quot;s5&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `maxTokens` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object): - Cast to: &lt; **Record&lt;string, string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;

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

#### GET https://r.jina.ai/ephemeral/{encodedFid}

Get an ephemeral file.

Parameters:
- `encodedFid` (path, string, required)
- `t` (query, string)
- `s` (query, string)
- `crop` (query, string)

Responses:
- `200`: OK
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found

#### POST https://r.jina.ai/ephemeral/{encodedFid}

Get an ephemeral file.

Parameters:
- `encodedFid` (path, string, required)
- `t` (query, string)
- `s` (query, string)
- `crop` (query, string)

Request body (`application/json`):
- `encodedFid` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Endpoint parameter of *getEphemeral*
- `t` (string, required): [REQUIRED] - Cast to: &lt; **Date** &gt; - Endpoint parameter of *getEphemeral*
- `s` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Endpoint parameter of *getEphemeral*
- `crop` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *getEphemeral*

Responses:
- `200`: OK
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found

## Search API (s.jina.ai)

### Search

Search the web and get the results back in an LLM-friendly format. Put the query after `https://s.jina.ai/`, or pass it as `q`. Most options are `X-*` request headers.

#### GET https://s.jina.ai/{q}

Search the web (query in path).

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "google" | "bing" | "reader")
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
- `ext` (query, string)
- `filetype` (query, string)
- `intitle` (query, string)
- `loc` (query, string)
- `site` (query, string)
- `type` (query, "web" | "images" | "news", default "web")
- `num` (query, number)
- `count` (query, number)
- `provider` (query, "google" | "bing" | "reader")
- `gl` (query, string)
- `hl` (query, string)
- `location` (query, string)
- `fallback` (query, boolean)
- `q` (path, string, required)
- `nfpr` (query, boolean)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
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

#### POST https://s.jina.ai/{q}

Search the web (query in path).

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "google" | "bing" | "reader")
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
- `ext` (query, string)
- `filetype` (query, string)
- `intitle` (query, string)
- `loc` (query, string)
- `site` (query, string)
- `type` (query, "web" | "images" | "news", default "web")
- `num` (query, number)
- `count` (query, number)
- `provider` (query, "google" | "bing" | "reader")
- `gl` (query, string)
- `hl` (query, string)
- `location` (query, string)
- `fallback` (query, boolean)
- `q` (path, string, required)
- `nfpr` (query, boolean)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `preloadUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `noServiceWorker` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `html` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `base` ("initial" | "final", default "initial"): - Cast to: &lt; **&quot;initial&quot; | &quot;final&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;initial&#39;
- `pdf` (string | string): Base64 encoded PDF. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `file` (string | string): Base64 encoded file. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `page` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *search*
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): - Cast to: &lt; **&quot;content&quot; | &quot;markdown&quot; | &quot;html&quot; | &quot;text&quot; | &quot;pageshot&quot; | &quot;screenshot&quot; | &quot;vlm&quot; | &quot;readerlm-v2&quot; | &quot;frontmatter&quot; | &quot;readability&quot; | &quot;...|string** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;content&#39;
- `withGeneratedAlt` (boolean | string): - Cast to: &lt; **PseudoBoolean** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;alt&quot; | &quot;all_p&quot; | &quot;alt_p&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): - Cast to: &lt; **&quot;none&quot; | &quot;text&quot; | &quot;link&quot; | &quot;image&quot; | &quot;html&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;link&#39;
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): - Cast to: &lt; **&quot;reader&quot; | &quot;index&quot; | &quot;research&quot; | &quot;agent&quot; | &quot;spider&quot; | &quot;ocr&quot; | &quot;ocr+&quot; | &quot;ocr++&quot; | &quot;pdf&quot; | &quot;pdf+&quot; | &quot;pdf++&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;text&quot; | &quot;gpt-oss&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `withLinksSummary` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withImagesSummary` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noCache` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeOverlay` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `detachInvisibles` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noGfm` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `cacheTolerance` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `targetSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `waitForSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `keepImgDataUrl` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `withIframe` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withShadowDom` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `skipCertVerification` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `setCookies` (array<any | string>): - Cast to: &lt; **Array&lt;object|string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `storageState` (StorageState): - Cast to: &lt; **StorageState** &gt; - Member of &lt;CrawlerOptions&gt;
  - `cookies` (array<Cookie>, default []): - Cast to: &lt; **Array&lt;Cookie&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `name` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `value` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `domain` (string): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `path` (string, default "/"): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt; - Defaults to: &#39;/&#39;
    - `expires` (string): - Cast to: &lt; **Date** &gt; - Member of &lt;Cookie&gt;
    - `httpOnly` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `secure` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `sameSite` ("Strict" | "Lax" | "None" | string): - Cast to: &lt; **&quot;Strict&quot; | &quot;Lax&quot; | &quot;None&quot;|string** &gt; - Member of &lt;Cookie&gt;
  - `origins` (array<LocalStorageOrigin>, default []): - Cast to: &lt; **Array&lt;LocalStorageOrigin&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `origin` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;LocalStorageOrigin&gt;
    - `localStorage` (array<LocalStorageItem>, default []): - Cast to: &lt; **Array&lt;LocalStorageItem&gt;** &gt; - Member of &lt;LocalStorageOrigin&gt; - Defaults to: []
- `exportStorageState` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyResources` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxy` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `userAgent` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `engine` ("google" | "bing" | "reader"): - Cast to: &lt; **&quot;google&quot; | &quot;bing&quot; | &quot;reader&quot;** &gt; - Endpoint parameter of *search*
- `injectPageScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectFrameScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `timeout` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `referer` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `tokenBudget` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `assertStatusCode` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `viewport` (Viewport): - Cast to: &lt; **Viewport** &gt; - Member of &lt;CrawlerOptions&gt;
  - `width` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `height` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `deviceScaleFactor` (number): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt;
  - `isMobile` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `isLandscape` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `hasTouch` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
- `instruction` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object. - Cast to: &lt; **object** &gt; - Member of &lt;CrawlerOptions&gt;
- `robotsTxt` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `zeroDataRetention` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdown` (TurnDownTweakableOptions): - Cast to: &lt; **TurnDownTweakableOptions** &gt; - Member of &lt;CrawlerOptions&gt;
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle - Cast to: &lt; **&quot;setext&quot; | &quot;atx&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `hr` (string): Turndown options > hr - Cast to: &lt; **string** &gt; - Member of &lt;TurnDownTweakableOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker - Cast to: &lt; **&quot;-&quot; | &quot;+&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter - Cast to: &lt; **&quot;_&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter - Cast to: &lt; **&quot;__&quot; | &quot;**&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle - Cast to: &lt; **&quot;inlined&quot; | &quot;referenced&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle - Cast to: &lt; **&quot;full&quot; | &quot;collapsed&quot; | &quot;shortcut&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
- `ocr` (OCRPreferences): - Cast to: &lt; **OCRPreferences** &gt; - Member of &lt;CrawlerOptions&gt;
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): - Cast to: &lt; **&quot;html&quot; | &quot;visible-content&quot; | &quot;mutation-idle&quot; | &quot;resource-idle&quot; | &quot;media-idle&quot; | &quot;network-idle&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): - Cast to: &lt; **&quot;true&quot; | &quot;h1&quot; | &quot;h2&quot; | &quot;h3&quot; | &quot;h4&quot; | &quot;h5&quot; | &quot;structured&quot; | &quot;s1&quot; | &quot;s2&quot; | &quot;s3&quot; | &quot;s4&quot; | &quot;s5&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `maxTokens` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object): - Cast to: &lt; **Record&lt;string, string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `ext` (array<string>): Returns web pages with a specific file extension. Example: to find the Honda GX120 Owner’s manual in PDF, type “Honda GX120 ownners manual ext:pdf”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `filetype` (array<string>): Returns web pages created in the specified file type. Example: to find a web page created in PDF format about the evaluation of age-related cognitive changes, type “evaluation of age cognitive changes filetype:pdf”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `intitle` (array<string>): Returns webpages containing the specified term in the title of the page. Example: to find pages about SEO conferences making sure the results contain 2023 in the title, type “seo conference intitle:2023”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `loc` (array<string>): Returns web pages written in the specified language. The language code must be in the ISO 639-1 two-letter code format. Example: to find information on visas only in Spanish, type “visas lang:es”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `site` (array<string>): Returns web pages coming only from a specific web site. Example: to find information about Goggles only on Brave pages, type “goggles site:brave.com”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `type` ("web" | "images" | "news", default "web"): - Cast to: &lt; **&quot;web&quot; | &quot;images&quot; | &quot;news&quot;** &gt; - Endpoint parameter of *search* - Defaults to: &#39;web&#39;
- `num` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *search* - Some validators will be applied on value(s): (v) =&gt; v &gt;= 0 &amp;&amp; v &lt;= 20
- `count` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *search* - Some validators will be applied on value(s): (v) =&gt; v &gt;= 0 &amp;&amp; v &lt;= 20
- `provider` ("google" | "bing" | "reader"): - Cast to: &lt; **&quot;google&quot; | &quot;bing&quot; | &quot;reader&quot;** &gt; - Endpoint parameter of *search*
- `gl` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *search* - Some validators will be applied on value(s): (v) =&gt; WORLD_COUNTRY_CODES.includes(v?.toLowerCase())
- `hl` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *search* - Some validators will be applied on value(s): (v) =&gt; serper_search_2.WORLD_LANGUAGES.some(l =&gt; l.code === v)
- `location` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *search*
- `fallback` (boolean): - Cast to: &lt; **boolean** &gt; - Endpoint parameter of *search*
- `q` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *search*
- `nfpr` (boolean): - Cast to: &lt; **boolean** &gt; - Endpoint parameter of *search*

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

#### GET https://s.jina.ai/search

Search the web.

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "google" | "bing" | "reader")
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
- `ext` (query, string)
- `filetype` (query, string)
- `intitle` (query, string)
- `loc` (query, string)
- `site` (query, string)
- `type` (query, "web" | "images" | "news", default "web")
- `num` (query, number)
- `count` (query, number)
- `provider` (query, "google" | "bing" | "reader")
- `gl` (query, string)
- `hl` (query, string)
- `location` (query, string)
- `fallback` (query, boolean)
- `q` (query, string)
- `nfpr` (query, boolean)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
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

Search the web.

Authentication: optional.

Parameters:
- `url` (query, string)
- `preloadUrl` (query, string)
- `noServiceWorker` (query, boolean | string)
- `html` (query, string)
- `base` (query, "initial" | "final", default "initial")
- `pdf` (query, string | string)
- `file` (query, string | string)
- `page` (query, number)
- `respondWith` (query, "content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content")
- `withGeneratedAlt` (query, boolean | string)
- `retainImages` (query, "none" | "all" | "alt" | "all_p" | "alt_p", default "all")
- `retainMedia` (query, "none" | "text" | "link" | "image" | "html", default "link")
- `preset` (query, "reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++")
- `retainLinks` (query, "none" | "all" | "text" | "gpt-oss", default "all")
- `withLinksSummary` (query, boolean | string | string)
- `withImagesSummary` (query, boolean | string)
- `noCache` (query, boolean | string)
- `removeOverlay` (query, boolean | string)
- `detachInvisibles` (query, boolean | string)
- `noGfm` (query, boolean | string | string)
- `cacheTolerance` (query, number)
- `targetSelector` (query, string)
- `waitForSelector` (query, string)
- `removeSelector` (query, string)
- `keepImgDataUrl` (query, boolean | string)
- `withIframe` (query, boolean | string | string)
- `withShadowDom` (query, boolean | string)
- `skipCertVerification` (query, boolean | string)
- `setCookies` (query, any | string)
- `exportStorageState` (query, boolean | string)
- `proxyUrl` (query, string)
- `proxyResources` (query, boolean | string)
- `proxy` (query, string)
- `userAgent` (query, string)
- `engine` (query, "google" | "bing" | "reader")
- `injectPageScript` (query, string)
- `injectFrameScript` (query, string)
- `timeout` (query, number)
- `locale` (query, string)
- `referer` (query, string)
- `tokenBudget` (query, number)
- `assertStatusCode` (query, number)
- `instruction` (query, string)
- `jsonSchema` (query, any)
- `robotsTxt` (query, string)
- `zeroDataRetention` (query, boolean | string)
- `respondTiming` (query, "html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle")
- `markdownChunking` (query, "true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string)
- `maxTokens` (query, number)
- `ext` (query, string)
- `filetype` (query, string)
- `intitle` (query, string)
- `loc` (query, string)
- `site` (query, string)
- `type` (query, "web" | "images" | "news", default "web")
- `num` (query, number)
- `count` (query, number)
- `provider` (query, "google" | "bing" | "reader")
- `gl` (query, string)
- `hl` (query, string)
- `location` (query, string)
- `fallback` (query, boolean)
- `q` (query, string)
- `nfpr` (query, boolean)
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
- `X-Page` (header, string): Steer which page to return for uploaded files (PDF, DOC, XLS, PPT, etc.). 1-indexed; ignored when no file/PDF is uploaded.
- `X-Preload-Url` (header, string): URL to preload before scraping. Ignored when no URL is provided.
- `X-No-Service-Worker` (header, string): Disable service workers when running the browser. Useful for bypassing service-worker-based caching or interception.

Request body (`application/json`):
- `url` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `preloadUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `noServiceWorker` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `html` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `base` ("initial" | "final", default "initial"): - Cast to: &lt; **&quot;initial&quot; | &quot;final&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;initial&#39;
- `pdf` (string | string): Base64 encoded PDF. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `file` (string | string): Base64 encoded file. - Cast to: &lt; **FancyFile|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `page` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *searchIndex*
- `respondWith` ("content" | "markdown" | "html" | "text" | "pageshot" | "screenshot" | "vlm" | "readerlm-v2" | "frontmatter" | "readability" | "jina-ocr-v1" | "jina-ocr" | ... (15 values) | string, default "content"): - Cast to: &lt; **&quot;content&quot; | &quot;markdown&quot; | &quot;html&quot; | &quot;text&quot; | &quot;pageshot&quot; | &quot;screenshot&quot; | &quot;vlm&quot; | &quot;readerlm-v2&quot; | &quot;frontmatter&quot; | &quot;readability&quot; | &quot;...|string** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;content&#39;
- `withGeneratedAlt` (boolean | string): - Cast to: &lt; **PseudoBoolean** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainImages` ("none" | "all" | "alt" | "all_p" | "alt_p", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;alt&quot; | &quot;all_p&quot; | &quot;alt_p&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `retainMedia` ("none" | "text" | "link" | "image" | "html", default "link"): - Cast to: &lt; **&quot;none&quot; | &quot;text&quot; | &quot;link&quot; | &quot;image&quot; | &quot;html&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;link&#39;
- `preset` ("reader" | "index" | "research" | "agent" | "spider" | "ocr" | "ocr+" | "ocr++" | "pdf" | "pdf+" | "pdf++"): - Cast to: &lt; **&quot;reader&quot; | &quot;index&quot; | &quot;research&quot; | &quot;agent&quot; | &quot;spider&quot; | &quot;ocr&quot; | &quot;ocr+&quot; | &quot;ocr++&quot; | &quot;pdf&quot; | &quot;pdf+&quot; | &quot;pdf++&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `retainLinks` ("none" | "all" | "text" | "gpt-oss", default "all"): - Cast to: &lt; **&quot;none&quot; | &quot;all&quot; | &quot;text&quot; | &quot;gpt-oss&quot;** &gt; - Member of &lt;CrawlerOptions&gt; - Defaults to: &#39;all&#39;
- `withLinksSummary` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withImagesSummary` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noCache` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeOverlay` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `detachInvisibles` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `noGfm` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `cacheTolerance` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `targetSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `waitForSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `removeSelector` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `keepImgDataUrl` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `withIframe` (boolean | string | string): - Cast to: &lt; **PseudoBoolean|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `withShadowDom` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `skipCertVerification` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `setCookies` (array<any | string>): - Cast to: &lt; **Array&lt;object|string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `storageState` (StorageState): - Cast to: &lt; **StorageState** &gt; - Member of &lt;CrawlerOptions&gt;
  - `cookies` (array<Cookie>, default []): - Cast to: &lt; **Array&lt;Cookie&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `name` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `value` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `domain` (string): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt;
    - `path` (string, default "/"): - Cast to: &lt; **string** &gt; - Member of &lt;Cookie&gt; - Defaults to: &#39;/&#39;
    - `expires` (string): - Cast to: &lt; **Date** &gt; - Member of &lt;Cookie&gt;
    - `httpOnly` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `secure` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Cookie&gt;
    - `sameSite` ("Strict" | "Lax" | "None" | string): - Cast to: &lt; **&quot;Strict&quot; | &quot;Lax&quot; | &quot;None&quot;|string** &gt; - Member of &lt;Cookie&gt;
  - `origins` (array<LocalStorageOrigin>, default []): - Cast to: &lt; **Array&lt;LocalStorageOrigin&gt;** &gt; - Member of &lt;StorageState&gt; - Defaults to: []
    - `origin` (string, required): [REQUIRED] - Cast to: &lt; **string** &gt; - Member of &lt;LocalStorageOrigin&gt;
    - `localStorage` (array<LocalStorageItem>, default []): - Cast to: &lt; **Array&lt;LocalStorageItem&gt;** &gt; - Member of &lt;LocalStorageOrigin&gt; - Defaults to: []
- `exportStorageState` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyUrl` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxyResources` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `proxy` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `userAgent` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `engine` ("google" | "bing" | "reader"): - Cast to: &lt; **&quot;google&quot; | &quot;bing&quot; | &quot;reader&quot;** &gt; - Endpoint parameter of *searchIndex*
- `injectPageScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `injectFrameScript` (array<string>): - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `timeout` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt; 0 &amp;&amp; v &lt;= 180
- `locale` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `referer` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `tokenBudget` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `assertStatusCode` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt;
- `viewport` (Viewport): - Cast to: &lt; **Viewport** &gt; - Member of &lt;CrawlerOptions&gt;
  - `width` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `height` (number, default 1280): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt; - Defaults to: 1280
  - `deviceScaleFactor` (number): - Cast to: &lt; **number** &gt; - Member of &lt;Viewport&gt;
  - `isMobile` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `isLandscape` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
  - `hasTouch` (boolean): - Cast to: &lt; **boolean** &gt; - Member of &lt;Viewport&gt;
- `instruction` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `jsonSchema` (any): Can be any value - string, number, boolean, array or object. - Cast to: &lt; **object** &gt; - Member of &lt;CrawlerOptions&gt;
- `robotsTxt` (string): - Cast to: &lt; **string** &gt; - Member of &lt;CrawlerOptions&gt;
- `zeroDataRetention` (boolean | string): - Cast to: &lt; **PseudoBooleanLoose** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdown` (TurnDownTweakableOptions): - Cast to: &lt; **TurnDownTweakableOptions** &gt; - Member of &lt;CrawlerOptions&gt;
  - `headingStyle` ("setext" | "atx"): Turndown options > headingStyle - Cast to: &lt; **&quot;setext&quot; | &quot;atx&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `hr` (string): Turndown options > hr - Cast to: &lt; **string** &gt; - Member of &lt;TurnDownTweakableOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v.length &gt; 0 &amp;&amp; v.length &lt;= 128
  - `bulletListMarker` ("-" | "+" | "*"): Turndown options > bulletListMarker - Cast to: &lt; **&quot;-&quot; | &quot;+&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `emDelimiter` ("_" | "*"): Turndown options > emDelimiter - Cast to: &lt; **&quot;_&quot; | &quot;*&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `strongDelimiter` ("__" | "**"): Turndown options > strongDelimiter - Cast to: &lt; **&quot;__&quot; | &quot;**&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkStyle` ("inlined" | "referenced" | "discarded"): Turndown options > linkStyle - Cast to: &lt; **&quot;inlined&quot; | &quot;referenced&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
  - `linkReferenceStyle` ("full" | "collapsed" | "shortcut" | "discarded"): Turndown options > linkReferenceStyle - Cast to: &lt; **&quot;full&quot; | &quot;collapsed&quot; | &quot;shortcut&quot; | &quot;discarded&quot;** &gt; - Member of &lt;TurnDownTweakableOptions&gt;
- `ocr` (OCRPreferences): - Cast to: &lt; **OCRPreferences** &gt; - Member of &lt;CrawlerOptions&gt;
  - `preferEndToEnd` (boolean): Prefer end-to-end OCR mode (over PDF text) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `preferImgOrder` (boolean): Prefer better image order over particular markdown format (only applies in end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `inlineFormula` (boolean): Blocks with inline formulas should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt;
  - `blockFormula` (boolean, default true): Formula blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
  - `table` (boolean, default true): Table blocks should go through OCR (only applies in non-end-to-end mode) - Cast to: &lt; **boolean** &gt; - Member of &lt;OCRPreferences&gt; - Defaults to: true
- `respondTiming` ("html" | "visible-content" | "mutation-idle" | "resource-idle" | "media-idle" | "network-idle"): - Cast to: &lt; **&quot;html&quot; | &quot;visible-content&quot; | &quot;mutation-idle&quot; | &quot;resource-idle&quot; | &quot;media-idle&quot; | &quot;network-idle&quot;** &gt; - Member of &lt;CrawlerOptions&gt;
- `markdownChunking` ("true" | "h1" | "h2" | "h3" | "h4" | "h5" | "structured" | "s1" | "s2" | "s3" | "s4" | "s5" | string): - Cast to: &lt; **&quot;true&quot; | &quot;h1&quot; | &quot;h2&quot; | &quot;h3&quot; | &quot;h4&quot; | &quot;h5&quot; | &quot;structured&quot; | &quot;s1&quot; | &quot;s2&quot; | &quot;s3&quot; | &quot;s4&quot; | &quot;s5&quot;|string** &gt; - Member of &lt;CrawlerOptions&gt;
- `maxTokens` (number): - Cast to: &lt; **number** &gt; - Member of &lt;CrawlerOptions&gt; - Some validators will be applied on value(s): (v) =&gt; v &gt;= 500
- `customHeader` (object): - Cast to: &lt; **Record&lt;string, string&gt;** &gt; - Member of &lt;CrawlerOptions&gt;
- `ext` (array<string>): Returns web pages with a specific file extension. Example: to find the Honda GX120 Owner’s manual in PDF, type “Honda GX120 ownners manual ext:pdf”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `filetype` (array<string>): Returns web pages created in the specified file type. Example: to find a web page created in PDF format about the evaluation of age-related cognitive changes, type “evaluation of age cognitive changes filetype:pdf”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `intitle` (array<string>): Returns webpages containing the specified term in the title of the page. Example: to find pages about SEO conferences making sure the results contain 2023 in the title, type “seo conference intitle:2023”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `loc` (array<string>): Returns web pages written in the specified language. The language code must be in the ISO 639-1 two-letter code format. Example: to find information on visas only in Spanish, type “visas lang:es”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `site` (array<string>): Returns web pages coming only from a specific web site. Example: to find information about Goggles only on Brave pages, type “goggles site:brave.com”. - Cast to: &lt; **Array&lt;string&gt;** &gt; - Member of &lt;GoogleSearchExplicitOperatorsDto&gt;
- `type` ("web" | "images" | "news", default "web"): - Cast to: &lt; **&quot;web&quot; | &quot;images&quot; | &quot;news&quot;** &gt; - Endpoint parameter of *searchIndex* - Defaults to: &#39;web&#39;
- `num` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *searchIndex* - Some validators will be applied on value(s): (v) =&gt; v &gt;= 0 &amp;&amp; v &lt;= 20
- `count` (number): - Cast to: &lt; **number** &gt; - Endpoint parameter of *searchIndex* - Some validators will be applied on value(s): (v) =&gt; v &gt;= 0 &amp;&amp; v &lt;= 20
- `provider` ("google" | "bing" | "reader"): - Cast to: &lt; **&quot;google&quot; | &quot;bing&quot; | &quot;reader&quot;** &gt; - Endpoint parameter of *searchIndex*
- `gl` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *searchIndex* - Some validators will be applied on value(s): (v) =&gt; WORLD_COUNTRY_CODES.includes(v?.toLowerCase())
- `hl` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *searchIndex* - Some validators will be applied on value(s): (v) =&gt; serper_search_2.WORLD_LANGUAGES.some(l =&gt; l.code === v)
- `location` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *searchIndex*
- `fallback` (boolean): - Cast to: &lt; **boolean** &gt; - Endpoint parameter of *searchIndex*
- `q` (string): - Cast to: &lt; **string** &gt; - Endpoint parameter of *searchIndex*
- `nfpr` (boolean): - Cast to: &lt; **boolean** &gt; - Endpoint parameter of *searchIndex*

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
