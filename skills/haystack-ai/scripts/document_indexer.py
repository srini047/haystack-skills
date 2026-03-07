"""
Haystack Document Indexer

Utility for preparing, chunking, and indexing documents for Haystack pipelines.

Usage:
    python document_indexer.py --input docs.json --output indexed_docs.json --chunk-size 500
    python document_indexer.py --input documents/ --format pdf --store elasticsearch
"""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Document:
    """Haystack Document representation"""
    content: str
    meta: Dict[str, Any]
    id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create Document from dictionary"""
        return cls(
            content=data.get("content", ""),
            meta=data.get("meta", {}),
            id=data.get("id")
        )


class DocumentChunker:
    """Utility for chunking documents into smaller segments"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size in tokens (approximate)
            overlap: Number of overlapping tokens between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, chunk_id: str) -> List[Document]:
        """
        Chunk text into smaller documents.
        
        Args:
            text: Text to chunk
            chunk_id: Base ID for chunks
        
        Returns:
            List of chunked documents
        """
        # Simple word-based chunking (approximate token counting)
        words = text.split()
        chunks = []
        chunk_num = 0
        
        i = 0
        while i < len(words):
            # Get chunk of words
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Create document
            doc = Document(
                content=chunk_text,
                meta={
                    "chunk_id": f"{chunk_id}_chunk_{chunk_num}",
                    "chunk_num": chunk_num,
                },
                id=f"{chunk_id}_chunk_{chunk_num}"
            )
            chunks.append(doc)
            
            # Move forward with overlap
            i += self.chunk_size - self.overlap
            chunk_num += 1
        
        return chunks
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk a list of documents"""
        chunked = []
        for doc in documents:
            chunked.extend(self.chunk_text(doc.content, doc.id or "doc"))
        return chunked


def load_json_documents(file_path: str) -> List[Document]:
    """Load documents from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return [Document.from_dict(item) for item in data]
    else:
        return [Document.from_dict(data)]


def load_text_file(file_path: str, metadata: Dict[str, Any] = None) -> Document:
    """Load a single text document"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    return Document(
        content=content,
        meta=metadata or {
            "source": str(file_path),
            "filename": Path(file_path).name,
        },
        id=Path(file_path).stem
    )


def load_documents_from_directory(
    directory: str,
    file_extensions: List[str] = None
) -> List[Document]:
    """Load documents from directory"""
    if file_extensions is None:
        file_extensions = [".txt", ".md"]
    
    documents = []
    for file_path in Path(directory).rglob("*"):
        if file_path.suffix in file_extensions:
            doc = load_text_file(str(file_path))
            documents.append(doc)
    
    return documents


def save_documents(documents: List[Document], output_path: str) -> None:
    """Save documents to JSON file"""
    doc_dicts = [
        {
            "id": doc.id,
            "content": doc.content,
            "meta": doc.meta
        }
        for doc in documents
    ]
    
    with open(output_path, 'w') as f:
        json.dump(doc_dicts, f, indent=2)
    
    print(f"Saved {len(documents)} documents to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Haystack Document Indexer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python document_indexer.py --input docs.json --output indexed.json
  python document_indexer.py --input ./documents --chunk-size 500 --output chunked.json
  python document_indexer.py --input multi_files.json --chunk-size 300 --overlap 50
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input file or directory"
    )
    parser.add_argument(
        "--output", "-o",
        default="indexed_documents.json",
        help="Output JSON file for indexed documents"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Target chunk size in tokens"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Token overlap between chunks"
    )
    parser.add_argument(
        "--no-chunk",
        action="store_true",
        help="Skip chunking step"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print processing details"
    )
    
    args = parser.parse_args()
    
    # Load documents
    input_path = Path(args.input)
    if input_path.is_dir():
        if args.verbose:
            print(f"Loading documents from directory: {args.input}")
        documents = load_documents_from_directory(str(args.input))
    else:
        if args.verbose:
            print(f"Loading documents from file: {args.input}")
        documents = load_json_documents(str(args.input))
    
    print(f"Loaded {len(documents)} documents")
    
    # Chunk documents if requested
    if not args.no_chunk:
        if args.verbose:
            print(f"Chunking documents (size={args.chunk_size}, overlap={args.overlap})")
        chunker = DocumentChunker(chunk_size=args.chunk_size, overlap=args.overlap)
        documents = chunker.chunk_documents(documents)
        print(f"Created {len(documents)} chunks")
    
    # Save
    save_documents(documents, args.output)
    
    if args.verbose:
        print("\nSample document:")
        if documents:
            doc = documents[0]
            print(f"  ID: {doc.id}")
            print(f"  Content: {doc.content[:100]}...")
            print(f"  Meta: {doc.meta}")


if __name__ == "__main__":
    main()
