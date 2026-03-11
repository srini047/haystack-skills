# Haystack Components Reference

This document lists the Haystack components that can be used (this is not an exhaustive list, but a reference for commonly used components in this project). 
Haystack pipelines are built by connecting modular components that process data
and pass outputs to the next component in the pipeline.

---

## 1. Document Stores

Document stores hold indexed documents and embeddings.

Common options:

- InMemoryDocumentStore
- ChromaDocumentStore
- ElasticsearchDocumentStore
- QdrantDocumentStore

Use cases:

- Store indexed documents
- Support BM25 or vector search
- Provide metadata filtering

---

## 2. Retrievers

Retrievers search the document store and return relevant documents.

### Sparse Retrieval

Keyword-based retrieval methods.

Examples:

- InMemoryBM25Retriever
- ElasticsearchBM25Retriever

### Dense Retrieval

Vector-based semantic search using embeddings.

Examples:

- InMemoryEmbeddingRetriever
- ElasticsearchEmbeddingRetriever
- WeaviateEmbeddingRetriever

### Hybrid Retrieval

Examples:

Retrival combining more than one retrieval methods.

- QdrantHybridRetriever
- WeaviateHybridRetriever

Use cases:

- Semantic similarity search
- Retrieval in RAG systems

---

## 3. Embedders

Embedders convert text into vector embeddings.

Two types exist:

### Document Embedders
Examples:

- SentenceTransformersDocumentEmbedder
- OpenAIDocumentEmbedder
- CohereDocumentEmbedder

### Text Embedders
Examples:

- SentenceTransformersTextEmbedder
- OpenAITextEmbedder
- CohereTextEmbedder

---

## 4. Prompt Builders

Prompt builders construct prompts for LLMs using templates.

Examples:

- PromptBuilder
- ChatPromptBuilder

Usage:

- Insert retrieved documents into prompts
- Format system and user instructions

Example template:
```
Context:
{{documents}}

Question:
{{query}}
Answer:
```

Note: For more templates refer `references/prompts.md`

---

## 5. Generators (LLMs)

Generators produce text responses using large language models.

Examples:

- OpenAIChatGenerator
- HuggingFaceLocalGenerator
- AzureOpenAIChatGenerator
- CohereChatGenerator

Use cases:

- Answer generation
- Summarization
- Reasoning with context

---

## 6. Joiners

Joiners merge outputs from multiple retrievers.

Examples:

- DocumentJoiner
- AnswerJoiner

Use cases:

- Hybrid retrieval
- Combining BM25 + vector results

---

## 7. Rankers

Rankers reorder retrieved documents based on relevance.

Examples:

- TransformersSimilarityRanker
- SentenceTransformersSimilarityRanker
- JinaRanker

Use cases:

- Reranking retrieved documents
- Improving retrieval accuracy

---

## 8. Preprocessors

Preprocessors prepare documents before indexing.

Examples:

- DocumentSplitter
- DocumentCleaner
- CSVDocumentSplitter

Use cases:

- Chunking documents
- Removing noise
- Preparing text for embedding

---

## 9. Converters

Converters transform files into Haystack Document objects.

Examples:

- PyPDFToDocument
- HTMLToDocument
- TextFileToDocument
- MarkdownToDocument

Use cases:

- Ingest PDFs
- Ingest HTML pages
- Convert files for indexing

---

## 10. Writers

Writers store documents into document stores.

Examples:

- DocumentWriter

Use cases:

- Indexing pipeline
- Saving documents with embeddings

---

## 11. Routers

Routers control pipeline flow based on conditions.

Examples:

- MetadataRouter
- ConditionalRouter
- TransformersZeroShotTextRouter

Use cases:

- Route documents based on metadata
- Dynamic pipeline branching
