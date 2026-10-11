"""
Streamlit UI for the SAP ABAP Knowledge Assistant.

Run with:
    streamlit run app.py
"""
import streamlit as st

from src.rag_chain import answer_question

st.set_page_config(page_title="SAP ABAP Knowledge Assistant", page_icon="🧠")

st.title("🧠 SAP ABAP Knowledge Assistant")
st.caption(
    "A RAG-based assistant for SAP ABAP questions — paste code or ask about "
    "CDS views, error codes, or best practices."
)

with st.expander("ℹ️ About this project"):
    st.markdown(
        """
        This assistant retrieves relevant chunks from a local knowledge
        base (SAP ABAP docs, error codes, best practices) and uses them to
        ground the LLM's answer, reducing hallucination compared to asking
        an LLM directly.

        **Before first use:** run `python -m src.ingest` once to build the
        vector store from the sample documents in `data/sample_abap_docs/`.
        """
    )

question = st.text_area(
    "Ask a question or paste an ABAP snippet:",
    height=150,
    placeholder="e.g. Why would SY-SUBRC = 4 occur after a SELECT SINGLE?",
)

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Retrieving context and generating answer..."):
        try:
            answer, sources = answer_question(question)
            st.markdown("### Answer")
            st.write(answer)

            with st.expander(f"📚 Sources ({len(sources)} chunk(s) retrieved)"):
                for i, doc in enumerate(sources, start=1):
                    st.markdown(f"**Source {i}:** `{doc.metadata.get('source', 'unknown')}`")
                    st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
        except Exception as e:
            st.error(
                "Something went wrong. Make sure you've run `python -m "
                "src.ingest` and set GOOGLE_API_KEY in your .env file."
            )
            st.exception(e)
