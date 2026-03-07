"""
Hybrid Search Pipeline

This example demonstrates a hybrid retrieval approach that combines:
- BM25 (sparse, keyword-based retrieval)
- Semantic search (dense embeddings)
- Result merging and deduplication

This approach provides better recall than either method alone.

Prerequisites:
- haystack-ai installed
- Access to embedding model (HuggingFace)
"""

from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.joiners import DocumentJoiner
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.dataclasses import ChatMessage


# Sample documents
DOCUMENTS = [
    Document(
        content="Python is a high-level programming language known for its simplicity and readability.",
        meta={"language": "programming", "year": 2020}
    ),
    Document(
        content="JavaScript runs in browsers and is essential for web development and interactivity.",
        meta={"language": "web", "year": 2021}
    ),
    Document(
        content="Go is a systems programming language created by Google for concurrent programming.",
        meta={"language": "systems", "year": 2019}
    ),
    Document(
        content="Python libraries like NumPy and Pandas are crucial for data science and analytics.",
        meta={"language": "data-science", "year": 2022}
    ),
]


def main():
    top_k = 3
    
    # Step 1: Setup document store with embeddings
    print("📚 Setting up hybrid search system...\n")
    
    document_store = InMemoryDocumentStore()
    
    # Embed documents
    embedder = SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    documents_with_embeddings = embedder.run(DOCUMENTS)["documents"]
    document_store.write_documents(documents_with_embeddings)
    print(f"✓ Indexed and embedded {len(DOCUMENTS)} documents\n")
    
    # Step 2: Create retrievers
    print("🔧 Creating retriever components...\n")
    bm25_retriever = InMemoryBM25Retriever(document_store=document_store)
    embedding_retriever = InMemoryEmbeddingRetriever(document_store=document_store)
    
    # Step 3: Build hybrid pipeline
    print("🔗 Building hybrid search pipeline...\n")
    pipeline = Pipeline()
    
    pipeline.add_component("bm25_retriever", bm25_retriever)
    pipeline.add_component("embedding_retriever", embedding_retriever)
    pipeline.add_component("joiner", DocumentJoiner(sort_by_score=True))
    
    pipeline.connect("bm25_retriever.documents", "joiner.documents_left")
    pipeline.connect("embedding_retriever.documents", "joiner.documents_right")
    
    # Step 4: Run hybrid search queries
    print("❓ Running hybrid search queries...\n")
    
    queries = [
        "Python programming",
        "web development languages",
        "data science tools"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        print("─" * 50)
        
        # Embed query
        query_embedding = embedder.run(documents=[Document(content=query)])["documents"][0].embedding
        
        # Run hybrid search
        result = pipeline.run({
            "bm25_retriever": {"query": query},
            "embedding_retriever": {"query_embedding": query_embedding}
        })
        
        merged_docs = result["joiner"]["documents"]
        
        print(f"Found {len(merged_docs)} results:\n")
        for i, doc in enumerate(merged_docs[:top_k], 1):
            print(f"{i}. {doc.content[:80]}...")
            print(f"   Score: {doc.score:.4f}\n")


if __name__ == "__main__":
    main()
