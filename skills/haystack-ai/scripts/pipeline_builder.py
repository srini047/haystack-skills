"""
Haystack Pipeline Builder Utility

Helper script for constructing and configuring Haystack pipelines.
Supports RAG, hybrid search, and multi-stage retrieval patterns.

Usage:
    python pipeline_builder.py --type rag --llm openai --output pipeline.yaml
    python pipeline_builder.py --type hybrid --embedder sentence-transformers --output pipeline.yaml
"""

import argparse
import json
from typing import Dict, Any, Optional
from enum import Enum


class PipelineType(Enum):
    """Supported pipeline types"""
    SIMPLE_RAG = "rag"
    HYBRID_SEARCH = "hybrid"
    RETRIEVAL_RERANKING = "reranking"
    MULTI_STAGE = "multi-stage"


def create_simple_rag_pipeline(
    llm_provider: str = "openai",
    embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    document_store: str = "in-memory",
) -> Dict[str, Any]:
    """
    Create a simple RAG pipeline configuration.
    
    Args:
        llm_provider: LLM provider (openai, huggingface, etc.)
        embedder_model: Embedding model name
        document_store: Document store type (in-memory, elasticsearch, weaviate)
    
    Returns:
        Pipeline configuration dictionary
    """
    return {
        "name": "simple-rag-pipeline",
        "components": {
            "document_store": {
                "type": document_store,
                "config": {
                    "embedding_dim": 384 if "MiniLM" in embedder_model else 768,
                }
            },
            "retriever": {
                "type": "embedding-retriever",
                "config": {
                    "embedder": embedder_model,
                    "top_k": 5,
                }
            },
            "llm": {
                "type": "text-generator",
                "config": {
                    "provider": llm_provider,
                    "model": "gpt-3.5-turbo" if llm_provider == "openai" else "meta-llama/Llama-2-7b",
                    "temperature": 0.7,
                }
            },
            "prompt_builder": {
                "type": "prompt-builder",
                "config": {
                    "template": "Context: {documents}\nQuestion: {query}\nAnswer:"
                }
            }
        },
        "connections": [
            ("retriever.documents", "prompt_builder.documents"),
            ("prompt_builder.prompt", "llm.prompt"),
        ]
    }


def create_hybrid_search_pipeline(
    embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    llm_provider: str = "openai",
) -> Dict[str, Any]:
    """
    Create a hybrid search pipeline (BM25 + embedding-based).
    
    Args:
        embedder_model: Embedding model name
        llm_provider: LLM provider
    
    Returns:
        Pipeline configuration dictionary
    """
    return {
        "name": "hybrid-search-pipeline",
        "components": {
            "document_store": {
                "type": "elasticsearch",
                "config": {
                    "host": "localhost",
                    "port": 9200,
                    "embedding_dim": 384,
                }
            },
            "bm25_retriever": {
                "type": "bm25-retriever",
                "config": {
                    "top_k": 5,
                }
            },
            "embedding_retriever": {
                "type": "embedding-retriever",
                "config": {
                    "embedder": embedder_model,
                    "top_k": 5,
                }
            },
            "document_joiner": {
                "type": "document-joiner",
                "config": {
                    "mode": "concatenate",
                }
            },
            "llm": {
                "type": "text-generator",
                "config": {
                    "provider": llm_provider,
                    "model": "gpt-3.5-turbo",
                }
            }
        },
        "connections": [
            ("bm25_retriever.documents", "document_joiner.documents_left"),
            ("embedding_retriever.documents", "document_joiner.documents_right"),
        ]
    }


def create_multi_stage_reranking_pipeline(
    embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
    llm_provider: str = "openai",
) -> Dict[str, Any]:
    """
    Create a multi-stage pipeline with reranking.
    
    Args:
        embedder_model: Embedding model
        reranker_model: Cross-encoder reranker model
        llm_provider: LLM provider
    
    Returns:
        Pipeline configuration dictionary
    """
    return {
        "name": "multi-stage-reranking-pipeline",
        "components": {
            "document_store": {
                "type": "weaviate",
                "config": {
                    "url": "http://localhost:8080",
                }
            },
            "dense_retriever": {
                "type": "embedding-retriever",
                "config": {
                    "embedder": embedder_model,
                    "top_k": 10,
                }
            },
            "reranker": {
                "type": "cross-encoder-ranker",
                "config": {
                    "model": reranker_model,
                    "top_k": 3,
                }
            },
            "llm": {
                "type": "text-generator",
                "config": {
                    "provider": llm_provider,
                    "model": "gpt-4",
                }
            }
        },
        "connections": [
            ("dense_retriever.documents", "reranker.documents"),
        ]
    }


def save_pipeline_config(config: Dict[str, Any], output_path: str) -> None:
    """Save pipeline configuration to file."""
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Pipeline configuration saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Haystack Pipeline Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline_builder.py --type rag --output rag_pipeline.json
  python pipeline_builder.py --type hybrid --embedder paraphrase-MiniLM-L6-v2 --output hybrid_pipeline.json
  python pipeline_builder.py --type reranking --output reranking_pipeline.json
        """
    )
    
    parser.add_argument(
        "--type",
        choices=[pt.value for pt in PipelineType],
        default="rag",
        help="Pipeline type to create"
    )
    parser.add_argument(
        "--llm",
        default="openai",
        help="LLM provider (openai, huggingface, local)"
    )
    parser.add_argument(
        "--embedder",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Embedding model name"
    )
    parser.add_argument(
        "--output",
        default="pipeline.json",
        help="Output file path for pipeline config"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print configuration to console"
    )
    
    args = parser.parse_args()
    
    # Create appropriate pipeline
    if args.type == PipelineType.SIMPLE_RAG.value:
        config = create_simple_rag_pipeline(
            llm_provider=args.llm,
            embedder_model=args.embedder
        )
    elif args.type == PipelineType.HYBRID_SEARCH.value:
        config = create_hybrid_search_pipeline(
            embedder_model=args.embedder,
            llm_provider=args.llm
        )
    elif args.type == PipelineType.RETRIEVAL_RERANKING.value:
        config = create_multi_stage_reranking_pipeline(
            embedder_model=args.embedder,
            llm_provider=args.llm
        )
    else:
        config = create_simple_rag_pipeline()
    
    # Output
    if args.verbose:
        print("\nGenerated Pipeline Configuration:")
        print(json.dumps(config, indent=2))
    
    save_pipeline_config(config, args.output)


if __name__ == "__main__":
    main()
