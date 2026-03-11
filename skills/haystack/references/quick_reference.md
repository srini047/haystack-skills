# Haystack Quick Reference Guide

A minimal guide for common best practices, debugging tips, and design reminders
when working with Haystack AI agentic framework.

## Pipeline Design Tips

Keep pipelines simple and modular.

Recommended structure for most applications:
```
Query → Retriever → Prompt Builder → Generator → Answer
```

Guidelines:
- Keep components single-purpose  
- Prefer small pipelines over complex graphs  
- Separate indexing pipelines from query pipelines  
- Avoid putting heavy preprocessing inside query pipelines

Good practices:

- Indexing pipeline
- - `Data → Converter → Splitter → Embedder → Document Store`
- Query pipeline
- - `Query → Retriever → Prompt Builder → Generator → Answer`

## Component Connection Rules

Always check component inputs and outputs.

Example:

Retriever → output: documents

PromptBuilder → input: documents

Correct connection: `retriever.documents → prompt_builder.documents`

Tips:
- Always check component docs for required inputs  
- Input/output names must match when connecting components  
- Most errors come from incorrect socket names

## Secret & API Key Handling

Never hardcode secrets. Its a vulnerablity.

Recommended approach: Use environment variables or Haystack secrets.

Example:
```
from haystack.utils import Secret

Secret.from_env_var("OPENAI_API_KEY")
```

Benefits:
- safer configuration
- easier deployment
- environment portability

## Document Processing Best Practices

When indexing documents:
- clean text before embedding  
- chunk large documents (200–500 tokens)  
- store metadata for filtering  

Recommended metadata fields:
```
source
document_type
created_at
topic
tags
```

## Retrieval Best Practices

Improve retrieval quality by:
- using hybrid retrieval (BM25 + embeddings)
- limiting retriever `top_k`
- reranking results
- filtering using metadata

Typical values:
```
retriever.top_k = 5–10  
reranker.top_k = 3–5
```

## Prompt Construction Tips

Keep prompts structured and on point for its usage.

Example format:
```
Context:
{documents}

Question:
{query}

Answer:
```

Tips:
- limit context length
- avoid sending too many documents
- prioritize top ranked documents

## Performance Tips

For faster pipelines:
- preload embedding models
- use async component calls
- limit document size
- reduce retriever top_k
- use batching when indexing

Heavy components:
- embedders
- LLM generators
- rerankers

## Debugging Pipelines

Debug component outputs using: `include_outputs_from`

Example:
```
pipeline.run(
    data={...},
    include_outputs_from=["prompt_builder"]
)
```
This lets you inspect intermediate outputs during development.

Useful debugging checks:
- retriever returns documents  
- prompt contains context  
- generator receives correct prompt  

## Common Errors

- Component connection errors
- - Cause: Incorrect input/output name.
- - Fix: Check component socket names.

- LLM returns irrelevant answers
- - Cause: Bad retrieval.
- - Fix: Improve retriever or use hybrid search.

- Empty retrieval results
- - Cause: Documents not indexed or embeddings missing.
- - Fix: Check indexing pipeline.

- Generic Issue (Cannot find where the bug lies)
- - Add more debug logs to check which part of code breaks

## Reference Project Structure

Example layout for a Haystack project:

```
project/
├── pyproject.toml
├── src/
│   └── my_haystack_app/
│       ├── __init__.py
│       ├── pipelines/
│       │   ├── __init__.py
│       │   ├── rag_pipeline.py
│       │   └── hybrid_pipeline.py
│       └── indexing/
│           └── __init__.py
│           └── document_indexing.py
│
├── scripts/
│   └── run_pipeline.py
│
├── configs/
│   └── pipeline_config.yaml
│
└── README.md
```
