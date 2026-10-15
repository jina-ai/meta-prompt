# Undocumented parameters

Visible operations only. Add the missing texts to `api-docs/overrides.mjs`; they survive every rebuild.

28 of 464 parameters and body fields have no description.

## POST r.jina.ai/

- query `instruction`
- query `zeroDataRetention`

## GET r.jina.ai/{url}

- query `instruction`
- query `zeroDataRetention`

## GET s.jina.ai/{q}

- query `instruction`
- query `zeroDataRetention`

## POST s.jina.ai/search

- query `instruction`
- query `zeroDataRetention`

## GET api.jina.ai/v1/models/{model_id}

- path `model_id`

## POST api.jina.ai/v1/chat/completions

- body `messages`
- body `stream`
- body `stream_options`
- body `max_completion_tokens`
- body `temperature`
- body `top_p`
- body `presence_penalty`
- body `frequency_penalty`
- body `stop`
- body `seed`
- body `logprobs`
- body `top_logprobs`
- body `logit_bias`
- body `response_format`

## GET api.jina.ai/v1/batch/{batch_id}

- path `batch_id`

## DELETE api.jina.ai/v1/batch/{batch_id}

- path `batch_id`

## GET api.jina.ai/v1/batches

- query `limit`

## GET api.jina.ai/v1/batch/{batch_id}/output

- path `batch_id`

## GET api.jina.ai/v1/batch/{batch_id}/errors

- path `batch_id`
