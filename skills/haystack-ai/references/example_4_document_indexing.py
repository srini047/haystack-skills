"""
Document Indexing Pipeline

This example shows how to:
- Load documents from various sources
- Chunk large documents into smaller pieces
- Create metadata for filtering and ranking
- Index documents efficiently

Prerequisites:
- haystack-ai installed
"""

from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore


def create_sample_documents():
    """Create sample documents representing different sources."""
    
    documents = [
        Document(
            content="""
            Retrieval-Augmented Generation (RAG) combines retrieval and generation. 
            It first retrieves relevant documents from a knowledge base, then uses 
            them as context for generating responses. This approach is particularly 
            useful for question-answering systems and factual information retrieval.
            """,
            meta={
                "source": "technical_guide",
                "chapter": "Advanced Techniques",
                "keywords": ["RAG", "retrieval", "generation", "LLM"]
            }
        ),
        Document(
            content="""
            Vector databases store high-dimensional vectors (embeddings) efficiently. 
            They support fast similarity search, which is crucial for semantic search 
            applications. Popular vector databases include Pinecone, Weaviate, and Milvus.
            """,
            meta={
                "source": "technical_guide",
                "chapter": "Infrastructure",
                "keywords": ["vector-db", "similarity-search", "embeddings"]
            }
        ),
        Document(
            content="""
            Prompt engineering is the practice of crafting effective prompts for LLMs. 
            Good prompts include clear instructions, examples, and context. Techniques 
            like chain-of-thought prompting can significantly improve LLM performance.
            """,
            meta={
                "source": "best_practices",
                "chapter": "LLM Optimization",
                "keywords": ["prompt", "engineering", "LLM", "optimization"]
            }
        ),
    ]
    
    return documents


def chunk_document(doc: Document, chunk_size: int = 300) -> list:
    """
    Split a document into chunks with metadata preservation.
    
    Args:
        doc: Document to chunk
        chunk_size: Approximate size of each chunk in words
    
    Returns:
        List of chunked documents
    """
    words = doc.content.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size]
        chunk_content = " ".join(chunk_words)
        
        # Create new document with chunk
        chunk_doc = Document(
            content=chunk_content,
            meta={
                **doc.meta,  # Preserve original metadata
                "chunk_index": len(chunks),
                "chunk_start_word": i,
                "chunk_end_word": i + len(chunk_words)
            }
        )
        chunks.append(chunk_doc)
    
    return chunks


def main():
    print("📖 Document Indexing Example\n")
    print("=" * 60)
    
    # Step 1: Create documents
    print("\n1️⃣  Creating sample documents...")
    documents = create_sample_documents()
    print(f"✓ Created {len(documents)} documents")
    
    # Step 2: Preview documents
    print("\n2️⃣  Document Preview:")
    for i, doc in enumerate(documents, 1):
        print(f"\n   Document {i}:")
        print(f"   Source: {doc.meta['source']}")
        print(f"   Chapter: {doc.meta['chapter']}")
        print(f"   Preview: {doc.content[:100]}...")
    
    # Step 3: Chunk documents
    print("\n\n3️⃣  Chunking documents (chunk_size=300 words)...")
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"   ✓ Document → {len(chunks)} chunks")
    
    print(f"\n✓ Total chunks created: {len(all_chunks)}")
    
    # Step 4: Index chunked documents
    print("\n4️⃣  Indexing documents...")
    document_store = InMemoryDocumentStore()
    document_store.write_documents(all_chunks)
    print(f"✓ Indexed {len(all_chunks)} documents in store\n")
    
    # Step 5: Query and retrieve
    print("5️⃣  Retrieving by metadata filter...")
    print("\n   Filtering by source='technical_guide':")
    
    # In-memory retrieval by metadata
    technical_docs = [
        doc for doc in all_chunks 
        if doc.meta.get("source") == "technical_guide"
    ]
    print(f"   ✓ Found {len(technical_docs)} relevant chunks\n")
    
    # Step 6: Statistics
    print("📊 Indexing Statistics:")
    print(f"   Total documents indexed: {len(all_chunks)}")
    print(f"   Average chunk size: {sum(len(doc.content.split()) for doc in all_chunks) // len(all_chunks)} words")
    
    source_distribution = {}
    for doc in all_chunks:
        source = doc.meta.get("source", "unknown")
        source_distribution[source] = source_distribution.get(source, 0) + 1
    
    print(f"   Distribution by source:")
    for source, count in source_distribution.items():
        print(f"     - {source}: {count} chunks")


if __name__ == "__main__":
    main()
