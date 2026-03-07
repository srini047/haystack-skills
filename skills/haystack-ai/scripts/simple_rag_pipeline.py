"""
Simple RAG Pipeline Example

This script demonstrates a basic retrieval-augmented generation pipeline
that indexes documents and answers questions.
"""

from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.generators import OpenAIGenerator
from haystack.utils import ComponentDefaultSetting


def create_simple_rag():
    """Create a simple RAG pipeline with BM25 retrieval and OpenAI generation."""
    
    # 1. Set up document store and index documents
    document_store = InMemoryDocumentStore()
    
    documents = [
        Document(
            content="Haystack is a framework for building search and RAG applications.",
            meta={"source": "haystack_docs", "topic": "framework"}
        ),
        Document(
            content="Vector databases store embeddings for semantic search.",
            meta={"source": "db_docs", "topic": "databases"}
        ),
        Document(
            content="Retrieval-augmented generation combines search with LLMs for grounded responses.",
            meta={"source": "ai_docs", "topic": "rag"}
        ),
    ]
    
    document_store.write_documents(documents)
    print(f"✓ Indexed {len(documents)} documents")
    
    # 2. Create pipeline components
    retriever = InMemoryBM25Retriever(document_store=document_store)
    
    prompt_template = """
    Context:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}
    
    Question: {{ query }}
    
    Answer:
    """
    
    prompt_builder = PromptBuilder(template=prompt_template)
    generator = OpenAIGenerator(
        api_key="your-api-key-here",
        model="gpt-3.5-turbo"
    )
    
    # 3. Create and connect the pipeline
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", generator)
    
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")
    
    print("✓ Pipeline created successfully")
    
    return pipeline


def run_query(pipeline, query: str) -> str:
    """Run a query through the RAG pipeline."""
    result = pipeline.run({
        "retriever": {"query": query},
        "prompt_builder": {"query": query}
    })
    return result["generator"]["replies"][0]


if __name__ == "__main__":
    # Create and run pipeline
    pipeline = create_simple_rag()
    
    # Example query
    query = "What is Haystack?"
    answer = run_query(pipeline, query)
    
    print(f"\nQuery: {query}")
    print(f"Answer: {answer}")
