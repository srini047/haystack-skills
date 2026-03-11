---
name: haystack
description: Build retrieval-augmented generation (RAG) systems and advanced search applications using the Haystack framework. Use when creating document pipelines, implementing semantic search, integrating LLMs with retrieval (RAG), building QA systems, or managing document stores and indexing.
---

# Haystack

This skill is for building intelligent search and retrieval systems with Haystack, combining document processing, semantic search, and LLM integration.

## Overview

This skill provides guidance for working with Haystack 2.0+, a modern framework for building production-grade RAG and search applications. Haystack enables building systems that combine:
- Document processing and indexing
- Semantic and hybrid search capabilities
- LLM integration for question-answering and reasoning
- Multi-stage pipelines for complex workflows
- Vector and keyword-based retrieval strategies

## When to use

Use this skill when the user is working on:
- **Building RAG Systems**: Creating retrieval-augmented generation pipelines that combine document search with LLM reasoning
- **Document Search & Indexing**: Implementing semantic or hybrid search over document collections
- **Question-Answering Systems**: Building QA systems that retrieve relevant context and answer questions
- **LLM Integration**: Connecting language models with retrieval systems for grounded responses
- **Pipeline Development**: Creating multi-stage processing workflows with Haystack components
- **Document Processing**: Preparing, chunking, and indexing documents for retrieval
- **Vector Store Setup**: Configuring and managing document embeddings and vector databases

## Core Concepts

### Key Haystack Components
- **DocumentStore**: Storage backends for documents (ElasticsearchDocumentStore, InMemoryDocumentStore, WeaviateDocumentStore, etc.)
- **Retriever**: Components that fetch relevant documents (BM25Retriever, EmbeddingRetriever, HybridRetriever)
- **Pipeline**: DAG-based orchestration of components
- **Generators/Answerers**: LLM-powered components that generate responses
- **Preprocessors**: Components for text chunking, cleaning, and normalization

## Architecture Patterns

### 1. Simple RAG Pipeline
```
Query → Retriever → LLM Generator → Answer
```

### 2. Hybrid Search Pipeline
```
Query → BM25 Retriever ⟶  Embedding Retriever ⟶ Document Joiner → LLM Generator → Answer
```

### 3. Multi-Stage Retrieval
```
Query → Dense Retriever → Reranker → LLM Generator → Answer
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip or conda package manager
- LLM API access (OpenAI, HuggingFace, Cohere, etc.) for generation tasks

### Basic Installation
```bash
pip install haystack-ai
```

### Optional Dependencies by Use Case
```bash
# For HuggingFace models
pip install sentence-transformers
```

## Common Usage Patterns

### Pattern 1: Setting Up a Document Store
- Initialize the appropriate DocumentStore type
- Configure indexing settings and metadata fields
- Prepare documents with required structure
- Handle document chunking and preprocessing

### Pattern 2: Building a Retriever
- Choose retriever type (BM25, Embedding, Hybrid)
- Configure similarity metrics and thresholds
- Set up embedding model if using dense retrieval
- Optimize for recall vs latency trade-offs

### Pattern 3: Creating a Pipeline
- Define component connections
- Handle component inputs/outputs
- Add error handling and validation
- Implement caching for performance

### Pattern 4: Integrating with LLMs
- Choose LLM provider and model
- Configure prompt templates for context injection
- Handle token limits and chunking
- Implement fallback strategies

## Best Practices

### Document Preparation
- Split documents into appropriate chunk sizes (typically 100-500 tokens)
- Preserve metadata for filtering and ranking
- Normalize text format and encoding
- Handle special characters and multi-language content

### Retrieval Optimization
- Use hybrid retrieval (BM25 + semantic) for better coverage
- Implement result deduplication
- Consider reranking for top-k results
- Monitor and tune retrieval parameters

### LLM Integration
- Use system prompts to guide answer generation
- Include relevant metadata in prompts
- Implement result validation
- Handle empty or low-confidence results gracefully

### Performance & Scaling
- Profile and optimize hot paths
- Use batch processing for document indexing
- Cache embeddings appropriately
- Monitor resource usage in production

## Troubleshooting Common Issues

### Retrieval Not Finding Relevant Documents
- Verify document preprocessing and chunk sizes
- Check embedding model dimensions and compatibility
- Consider hybrid search approach
- Review metadata filtering logic

### Low Quality Answers
- Improve retrieved context relevance
- Adjust prompt templates
- Implement reranking strategies
- Use better embedding models

### Performance Issues
- Split into seperate pipelines
- Use async processing where possible
- Optimize document store queries
- Consider batch processing

## Example Workflows

### Workflow 1: Building a Simple Document QA System
1. Prepare and index documents
2. Create retriever for document search
3. Connect retriever to LLM generator
4. Test with example questions

### Workflow 2: Implementing Hybrid Search
1. Set up BM25 component for keyword search
2. Configure embedding model and dense retriever
3. Combine results using document merger
4. Add ranking/reranking if needed

### Workflow 3: Production RAG System
1. Design document chunking strategy
2. Set up vector database (Elasticsearch, Weaviate, etc.)
3. Implement multi-stage retrieval
4. Add evaluation and monitoring

## Key Integration Points

- **LLM Providers**: OpenAI, HuggingFace, Cohere, Ollama
- **Vector Databases**: Elasticsearch, Weaviate, Pinecone, FAISS
- **Document Stores**: In-memory, Elasticsearch, Qdrant
- **Embedding Models**: Sentence Transformers, OpenAI embeddings
- **Evaluation Tools**: Haystack's evaluation suite, Ragas

## Resources

- **Official Documentation**: https://docs.haystack.deepset.ai/
- **GitHub Repository**: https://github.com/deepset-ai/haystack
- **Examples**: https://github.com/deepset-ai/haystack-cookbook/
