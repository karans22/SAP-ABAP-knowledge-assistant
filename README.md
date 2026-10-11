# SAP ABAP Knowledge Assistant (RAG)

A Retrieval-Augmented Generation (RAG) assistant that answers questions about
SAP ABAP code, error codes, and best practices — grounded in a local
knowledge base instead of relying purely on an LLM's memory.

Paste an ABAP snippet or ask a question (e.g. *"What does this CDS view
do?"* or *"Why would SY-SUBRC = 4 occur here?"*) and the assistant retrieves
the most relevant documentation chunks and uses them to generate a grounded
answer, reducing hallucination.

## Why this project

Enterprise AI/ML roles increasingly need engineers who can bridge deep
domain knowledge (here: SAP ABAP / S/4HANA) with modern GenAI tooling
(LLMs, RAG, vector search, prompt engineering). This project demonstrates
that combination directly, rather than as two separate skills on a resume.

## Architecture

```
User Question / ABAP Snippet
        │
        ▼
  Streamlit UI (app.py)
        │
        ▼
  Retrieval Chain (src/rag_chain.py)
        │
        ├── Embed query  ──────► Google Gemini Embeddings
        │
        ▼
  Chroma Vector Store  ◄──────  Ingested docs (src/ingest.py)
        │                       (data/sample_abap_docs/*.md)
        ▼
  Top-k relevant chunks
        │
        ▼
  LLM (Gemini) + Prompt Template ──► Grounded Answer
```

## Tech stack

- **LangChain** — orchestration of the retrieval + generation pipeline
- **ChromaDB** — local, free vector store for embeddings
- **Google Gemini API** (`langchain-google-genai`) — free-tier LLM + embeddings
- **Streamlit** — lightweight UI for demoing the assistant
- **Python 3.10+**

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   and copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   # then edit .env and add your GOOGLE_API_KEY
   ```

3. Ingest the sample documents into the vector store:
   ```bash
   python -m src.ingest
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project structure

```
sap-abap-knowledge-assistant/
├── app.py                     # Streamlit UI
├── src/
│   ├── ingest.py               # Loads, chunks, and embeds documents
│   └── rag_chain.py            # Retrieval + LLM chain
├── data/
│   └── sample_abap_docs/       # Sample ABAP knowledge base (replace with your own)
├── tests/
│   └── test_ingest.py
├── requirements.txt
└── .env.example
```

## Extending this project

- Swap the sample docs for real (sanitized) internal ABAP documentation,
  RICEFW specs, or SAP Notes.
- Add a feedback loop where the assistant logs unanswered/low-confidence
  questions for the knowledge base to be expanded.
- Add source citations in the UI so users can see which document chunk
  informed the answer.
- Containerize with Docker and deploy on a free-tier host (Render/Railway)
  for a live demo link.

## Status

Actively developed as a personal project to explore applied GenAI/RAG
patterns for enterprise use cases. Contributions and feedback welcome.
