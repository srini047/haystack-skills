"""
Document Indexing Pipeline

Demonstrates:
- Document creation
- Automatic chunking
- Metadata preservation
- Indexing into a document store
"""

from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.preprocessors import DocumentSplitter


def create_sample_documents():
    """Create sample documents."""

    documents = [
        Document(
            content="""
            Retrieval-Augmented Generation (RAG) combines retrieval and generation.
            It first retrieves relevant documents from a knowledge base, then uses
            them as context for generating responses.
            """,
            meta={
                "source": "technical_guide",
                "chapter": "Advanced Techniques",
                "keywords": ["RAG", "retrieval", "generation", "LLM"],
            },
        ),
        Document(
            content="""
            Vector databases store high-dimensional vectors (embeddings) efficiently.
            They support fast similarity search which is crucial for semantic search
            applications like RAG systems.
            """,
            meta={
                "source": "technical_guide",
                "chapter": "Infrastructure",
                "keywords": ["vector-db", "similarity-search", "embeddings"],
            },
        ),
        Document(
            content="""
            Prompt engineering is the practice of crafting effective prompts for LLMs.
            Techniques like chain-of-thought prompting can significantly improve model
            reasoning and response quality.
            """,
            meta={
                "source": "best_practices",
                "chapter": "LLM Optimization",
                "keywords": ["prompt", "engineering", "LLM", "optimization"],
            },
        ),
    ]

    return documents


def main():

    print("📖 Document Indexing Example")
    print("=" * 60)

    # Create document store
    documents = create_sample_documents()
    document_store = InMemoryDocumentStore()
    print(f"✓ Created {len(documents)} documents")

    # Document splitter
    splitter = DocumentSplitter(
        split_by="line",
        split_length=80,
        split_overlap=20,
    )

    # Build indexing pipeline
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("splitter", splitter)

    # Run indexing pipeline
    print("🔧 Chunking documents...")
    result = indexing_pipeline.run({
            "splitter": {"documents": documents}
    })
    chunks = result["splitter"]["documents"]
    print(f"✓ Created {len(chunks)} chunks")

    # Write to document store
    print("📚 Indexing chunks...")
    document_store.write_documents(chunks)
    print(f"✓ Indexed {len(chunks)} documents")

    # Metadata filtering example
    print("🔎 Filtering by metadata (source='technical_guide')")
    technical_docs = document_store.filter_documents(
        filters={"field": "meta.source", "operator": "==", "value": "technical_guide"}
    )
    print(f"✓ Found {len(technical_docs)} relevant chunks")

    # Statistics
    print("📊 Indexing Statistics")
    avg_chunk_size = sum(len(doc.content.split()) for doc in chunks) // len(chunks)
    print(f"Total chunks indexed: {len(chunks)}")
    print(f"Average chunk size: {avg_chunk_size} words")

    source_distribution = {}
    for doc in chunks:
        source = doc.meta.get("source", "unknown")
        source_distribution[source] = source_distribution.get(source, 0) + 1

    print("Distribution by source:")
    for source, count in source_distribution.items():
        print(f" - {source}: {count} chunks")


if __name__ == "__main__":
    main()
