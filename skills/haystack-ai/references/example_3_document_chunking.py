"""
Document Processing and Chunking

This example shows how to:
- Load documents from various sources
- Split large documents into manageable chunks
- Prepare documents for indexing with metadata

This is a critical step for building effective RAG systems.
"""

from haystack import Document
from haystack.components.splitters import DocumentSplitter, RecursiveDocumentSplitter


# Sample document
LONG_DOCUMENT = """
Chapter 1: Introduction to Artificial Intelligence

Artificial Intelligence (AI) has become one of the most transformative technologies of our time. 
From healthcare to finance, from transportation to entertainment, AI is reshaping how we live and work.

AI refers to computer systems designed to simulate human intelligence. These systems can learn from 
experience, recognize patterns, understand language, and make decisions. The field of AI encompasses 
several subfields including machine learning, deep learning, natural language processing, and computer vision.

The journey of AI began in the 1950s when researchers first attempted to create machines that could simulate 
human thinking. Since then, the field has evolved dramatically, with breakthroughs in deep learning and neural networks 
accelerating progress in recent years.

Chapter 2: Machine Learning Fundamentals

Machine learning is a method of data analysis that enables computers to learn and improve from experience 
without being explicitly programmed. Instead of following preprogrammed instructions, ML systems adjust their 
behavior based on exposure to data.

There are three main types of machine learning:

1. Supervised Learning: The algorithm learns from labeled training data. The input data (features) and 
desired output (labels) are both provided during training.

2. Unsupervised Learning: The algorithm learns patterns from unlabeled data without guidance about what 
the correct output should be. Common tasks include clustering and dimensionality reduction.

3. Reinforcement Learning: An agent learns by interacting with an environment, receiving rewards or 
penalties based on its actions. This is how computers learn to play games or control robots.

Each type has its own algorithms, applications, and challenges. Understanding which type to use for a 
particular problem is crucial for successful machine learning projects.

Chapter 3: Deep Learning and Neural Networks

Deep learning represents a breakthrough in machine learning, enabled by the availability of large datasets 
and powerful computing resources. It uses neural networks with multiple layers to learn hierarchical 
representations of data.

A neural network is inspired by the biological neurons in the brain. It consists of:
- Input layer: Receives the input data
- Hidden layers: Perform computations and extract features
- Output layer: Produces the final prediction

The "deep" in deep learning refers to the multiple hidden layers. Each layer transforms its input into 
increasingly abstract representations, allowing the network to learn complex patterns.

Common deep learning architectures include:
- CNNs (Convolutional Neural Networks): Excellent for image processing
- RNNs (Recurrent Neural Networks): Suitable for sequential data and time series
- Transformers: The foundation of modern NLP models

Deep learning has achieved remarkable results in image recognition, natural language processing, and 
game playing, surpassing human performance in many domains.
"""


def simple_splitter_example():
    """Example using simple document splitter"""
    print("=" * 60)
    print("Simple Document Splitter")
    print("=" * 60)
    
    splitter = DocumentSplitter(
        split_by="line",
        split_length=200,
        split_overlap=50
    )
    
    doc = Document(content=LONG_DOCUMENT, meta={"source": "ai_textbook.pdf"})
    chunks = splitter.split_documents([doc])
    
    print(f"\nOriginal document: {len(doc.content)} characters")
    print(f"Created {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks[:3], 1):
        print(f"--- Chunk {i} ---")
        print(chunk.content[:150] + "...\n")


def recursive_splitter_example():
    """Example using recursive document splitter for better results"""
    print("=" * 60)
    print("Recursive Document Splitter (Recommended)")
    print("=" * 60)
    
    # Try splitting on different separators to preserve meaning
    splitter = RecursiveDocumentSplitter(
        separators=["\n\n", "\n", "sentence", " "],
        split_length=200,
        split_overlap=10
    )
    
    doc = Document(content=LONG_DOCUMENT, meta={"source": "ai_textbook.pdf"})
    chunks = splitter.split_documents([doc])
    
    print(f"\nOriginal document: {len(doc.content)} characters")
    print(f"Created {len(chunks)} chunks\n")
    
    # Show statistics
    lengths = [len(chunk.content) for chunk in chunks]
    print(f"Chunk statistics:")
    print(f"  Min: {min(lengths)} characters")
    print(f"  Max: {max(lengths)} characters")
    print(f"  Avg: {sum(lengths) // len(lengths)} characters\n")
    
    # Show sample chunks
    for i, chunk in enumerate(chunks[:2], 1):
        print(f"--- Chunk {i} (Chapter/Section) ---")
        print(chunk.content[:200] + "...\n")


def metadata_preservation_example():
    """Example showing how metadata is handled during splitting"""
    print("=" * 60)
    print("Metadata Preservation During Splitting")
    print("=" * 60)
    
    splitter = DocumentSplitter(
        separator="\n\n",
        split_length=200,
        split_overlap=50
    )
    
    doc = Document(
        content=LONG_DOCUMENT,
        meta={
            "source": "ai_textbook.pdf",
            "title": "AI Fundamentals",
            "author": "Dr. Smith",
            "year": 2024
        }
    )
    
    chunks = splitter.split_documents([doc])
    
    print(f"\nCreated {len(chunks)} chunks with metadata preservation\n")
    print("Sample chunk metadata:")
    sample_chunk = chunks[0]
    print(f"  Source: {sample_chunk.meta['source']}")
    print(f"  Title: {sample_chunk.meta['title']}")
    print(f"  Author: {sample_chunk.meta['author']}")
    
    if 'chunk_id' in sample_chunk.meta:
        print(f"  Chunk ID: {sample_chunk.meta['chunk_id']}")


if __name__ == "__main__":
    print("\n🔄 Document Chunking Strategies\n")
    
    simple_splitter_example()
    print("\n")
    
    recursive_splitter_example()
    print("\n")
    
    metadata_preservation_example()
    
    print("\n✓ Document processing examples complete!")
