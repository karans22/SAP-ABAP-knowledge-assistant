"""
Ingests markdown documents from data/sample_abap_docs/ into a local
Chroma vector store, using Google Gemini embeddings.

Run with:
    python -m src.ingest
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_abap_docs"
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", ".chroma_store")


def load_documents():
    """Load all markdown files from the knowledge base directory."""
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def chunk_documents(documents, chunk_size=800, chunk_overlap=100):
    """Split documents into overlapping chunks for better retrieval granularity."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vector_store(chunks):
    """Embed chunks and persist them to a local Chroma store."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    vector_store.persist()
    return vector_store


def main():
    print(f"Loading documents from {DATA_DIR} ...")
    documents = load_documents()
    print(f"Loaded {len(documents)} document(s).")

    chunks = chunk_documents(documents)
    print(f"Split into {len(chunks)} chunk(s).")

    print(f"Embedding and persisting to {PERSIST_DIR} ...")
    build_vector_store(chunks)
    print("Done. Vector store is ready for querying.")


if __name__ == "__main__":
    main()
