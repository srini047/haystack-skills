"""
Hybrid Search Pipeline

Combines:
- BM25 keyword retrieval
- Dense embedding retrieval
- Result merging and ranking
"""

from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore

from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.joiners import DocumentJoiner


DOCUMENTS = [
    Document(
        content="Python is a high-level programming language known for its simplicity and readability.",
        meta={"language": "programming", "year": 2020},
    ),
    Document(
        content="JavaScript runs in browsers and is essential for web development and interactivity.",
        meta={"language": "web", "year": 2021},
    ),
    Document(
        content="Go is a systems programming language created by Google for concurrent programming.",
        meta={"language": "systems", "year": 2019},
    ),
    Document(
        content="Python libraries like NumPy and Pandas are crucial for data science and analytics.",
        meta={"language": "data-science", "year": 2022},
    ),
]


def main():
    top_k = 3

    print("📚 Setting up hybrid search system...")

    # Document Store
    document_store = InMemoryDocumentStore()

    # Document embedding
    doc_embedder = SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    docs_with_embeddings = doc_embedder.run(documents=DOCUMENTS)["documents"]
    document_store.write_documents(docs_with_embeddings)
    print(f"✓ Indexed and embedded {len(DOCUMENTS)} documents")

    # Retrievers
    bm25_retriever = InMemoryBM25Retriever(
        document_store=document_store,
        top_k=top_k,
    )
    embedding_retriever = InMemoryEmbeddingRetriever(
        document_store=document_store,
        top_k=top_k,
    )

    # Query embedder
    query_embedder = SentenceTransformersTextEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Document Joiner
    joiner = DocumentJoiner(sort_by_score=True)

    # Pipeline
    print("🔗 Building hybrid search pipeline...")
    pipeline = Pipeline()

    pipeline.add_component("bm25_retriever", bm25_retriever)
    pipeline.add_component("query_embedder", query_embedder)
    pipeline.add_component("embedding_retriever", embedding_retriever)
    pipeline.add_component("joiner", joiner)

    pipeline.connect("query_embedder.embedding", "embedding_retriever.query_embedding")
    pipeline.connect("bm25_retriever.documents", "joiner.documents")
    pipeline.connect("embedding_retriever.documents", "joiner.documents")

    print("✓ Hybrid pipeline ready")

    # Queries
    queries = [
        "Python programming",
        "web development languages",
        "data science tools",
    ]

    for query in queries:
        print(f"Query: {query}")
        print("─" * 50)

        result = pipeline.run(
            {
                "bm25_retriever": {"query": query},
                "query_embedder": {"text": query},
            }
        )
        merged_docs = result["joiner"]["documents"]

        print(f"Found {len(merged_docs)} results:")
        for i, doc in enumerate(merged_docs[:top_k], 1):
            print(f"{i}. {doc.content[:80]}...")
            print(f"Score: {doc.score:.4f}")


if __name__ == "__main__":
    main()
