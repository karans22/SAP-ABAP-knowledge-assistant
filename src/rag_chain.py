"""
Builds the retrieval-augmented generation chain: given a user question,
retrieve the most relevant chunks from the vector store and use them as
grounding context for the LLM's answer.
"""
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", ".chroma_store")

SYSTEM_PROMPT = """You are an assistant that answers questions about SAP \
ABAP development, grounded strictly in the provided context.

Rules:
- Answer using ONLY the information in the context below.
- If the context does not contain the answer, say so explicitly rather \
than guessing.
- When relevant, mention the specific ABAP concept, statement, or error \
code by name.
- Keep answers concise and technically precise.

Context:
{context}
"""


def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def get_retriever(k: int = 4):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )
    return vector_store.as_retriever(search_kwargs={"k": k})


def build_rag_chain():
    retriever = get_retriever()

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


def answer_question(question: str):
    """Convenience function: returns (answer, source_documents)."""
    chain, retriever = build_rag_chain()
    source_docs = retriever.invoke(question)
    answer = chain.invoke(question)
    return answer, source_docs
