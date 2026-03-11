# Haystack Pipeline Architecture Reference

This document provides reference architectures for common Haystack pipelines. More detailed explanation for right usage of each component can be found in its respective component page under the section `Most common position in a pipeline`.

The goal is to show **where components are typically placed in a pipeline**.
These are conceptual layouts that help design consistent systems.
Feel free to edit based on the use-case and needs.

---

## 1. RAG Architecture

The most common Haystack architecture for question answering.

```mermaid
graph TD
    A[User Query] --> B[Document Store]
    B --> C[Retriever]
    C --> D[Prompt Builder]
    D --> E[LLM Generator]
    E --> F[Answer Builder]
    F --> G[Final Answer]
```

---

## 2. Hybrid Retrieval Architecture

Used when combining **keyword search + semantic search**.

```mermaid
graph TD
    A[User Query] --> B[Query Router]
    B --> C[BM25 Retriever]
    B --> D[Embedding Retriever]
    C --> E[Document Joiner]
    D --> E
    E --> F[Prompt Builder]
    F --> G[Generator]
    G --> H[Answer Builder]
    H --> I[Final Answer]
```

---

# 3. Indexing Pipeline Architecture

This pipeline prepares documents before they are searchable.

```mermaid
graph TD
    A[Data Sources] --> B[Converters]
    B --> C[Document Cleaner]
    C --> D[Document Splitter]
    D --> E[Document Embedder]
    E --> F[Document Writer]
    F --> G[Document Store]
```

---

# 4. Multi-Stage Retrieval Architecture (Advanced RAG)

Used for **high quality retrieval systems**.

```mermaid
graph TD
    A[User Query] --> B[Query Embedder]
    B --> C[Dense Retriever]
    C --> D[Reranker]
    D --> E[Top Documents]
    E --> F[Prompt Builder]
    F --> G[Generator]
    G --> H[Answer Builder]
    H --> I[Final Answer]
```

---
