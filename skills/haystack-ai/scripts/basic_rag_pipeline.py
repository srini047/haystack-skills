"""
Simple RAG Pipeline Example
This script demonstrates a basic retrieval-augmented generation pipeline.
"""

from haystack import Document, Pipeline
from haystack.dataclasses import ChatMessage
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.utils import Secret

from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever


def create_simple_rag():
    """Create a simple RAG pipeline with BM25 retrieval and OpenAI generation."""

    # 1. Document store
    document_store = InMemoryDocumentStore()

    documents = [
        Document(
            content="Haystack is a AI agentic framework for building search and RAG applications.",
            meta={"source": "haystack_docs", "topic": "framework"},
        ),
        Document(
            content="Vector databases store embeddings for semantic search.",
            meta={"source": "db_docs", "topic": "databases"},
        ),
        Document(
            content="Retrieval-augmented generation combines search with LLMs for grounded responses.",
            meta={"source": "ai_docs", "topic": "rag"},
        ),
    ]

    document_store.write_documents(documents)

    print(f"✓ Indexed {len(documents)} documents")

    # 2. Retriever
    retriever = InMemoryBM25Retriever(document_store=document_store)

    # 3. Prompt template (chat format)
    prompt_template = [
        ChatMessage.from_system(
            "Answer the user's question using the provided context."
        ),
        ChatMessage.from_user(
            """
Context:
{% for doc in documents %}
{{ doc.content }}
{% endfor %}

Question: {{query}}
"""
        ),
    ]

    prompt_builder = ChatPromptBuilder()

    # 4. LLM
    llm = OpenAIChatGenerator(
        api_key=Secret.from_env_var("OPENAI_API_KEY"),
        model="gpt-4o-mini",
    )

    # 5. Build pipeline
    pipeline = Pipeline()

    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)

    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "llm.messages")

    print("✓ Pipeline created successfully")

    return pipeline, prompt_template


def run_query(pipeline, prompt_template, query: str) -> str:
    """Run a query through the RAG pipeline."""

    result = pipeline.run(
        data={
            "retriever": {"query": query},
            "prompt_builder": {
                "template": prompt_template,
                "template_variables": {"query": query},
            },
        }
    )

    return result["llm"]["replies"][0].content[0].text


if __name__ == "__main__":
    pipeline, template = create_simple_rag()

    query = "What is Haystack?"
    answer = run_query(pipeline, template, query)

    print(f"Query: {query}")
    print(f"Answer: {answer}")
