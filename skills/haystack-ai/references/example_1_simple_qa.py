"""
Simple Question-Answering System

This example shows how to build a basic question-answering system that:
- Indexes a collection of documents
- Retrieves relevant documents for a query
- Generates answers using an LLM

Prerequisites:
- haystack-ai installed
- OpenAI API key set as OPENAI_API_KEY environment variable
"""

from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.generators import OpenAIGenerator


# Sample documents
DOCUMENTS = [
    Document(
        content="""
        Machine Learning is a subset of artificial intelligence that enables systems 
        to learn and improve from experience without being explicitly programmed. 
        It uses algorithms to analyze data, identify patterns, and make decisions 
        with minimal human intervention.
        """,
        meta={"title": "What is Machine Learning", "category": "AI"}
    ),
    Document(
        content="""
        Deep Learning is a subset of machine learning that uses neural networks with 
        multiple layers to learn hierarchical representations of data. It has 
        revolutionized computer vision, natural language processing, and many other domains.
        """,
        meta={"title": "Understanding Deep Learning", "category": "AI"}
    ),
    Document(
        content="""
        Natural Language Processing (NLP) is a branch of AI that focuses on the 
        interaction between computers and human language. It enables computers to 
        understand, interpret, and generate human language in meaningful ways.
        """,
        meta={"title": "Introduction to NLP", "category": "AI"}
    ),
]


def main():
    # Step 1: Create and populate document store
    print("📚 Setting up document store...")
    document_store = InMemoryDocumentStore()
    document_store.write_documents(DOCUMENTS)
    print(f"✓ Indexed {len(DOCUMENTS)} documents\n")
    
    # Step 2: Create pipeline components
    print("🔧 Creating pipeline components...")
    retriever = InMemoryBM25Retriever(document_store=document_store)
    
    prompt_template = """
    Answer the question based on the provided documents.
    
    Documents:
    {% for doc in documents %}
    - {{ doc.content | trim }}
    {% endfor %}
    
    Question: {{ query }}
    Answer:
    """
    
    prompt_builder = PromptBuilder(template=prompt_template)
    generator = OpenAIGenerator(
        api_key="YOUR-API-KEY",
        model="gpt-3.5-turbo"
    )
    
    # Step 3: Build pipeline
    print("🔗 Building pipeline...")
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", generator)
    
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")
    print("✓ Pipeline ready\n")
    
    # Step 4: Run queries
    print("❓ Running queries...\n")
    
    queries = [
        "What is Machine Learning?",
        "Explain the difference between Machine Learning and Deep Learning",
        "What does NLP stand for?"
    ]
    
    for query in queries:
        print(f"Q: {query}")
        try:
            result = pipeline.run({
                "retriever": {"query": query},
                "prompt_builder": {"query": query}
            })
            answer = result["generator"]["replies"][0]
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
