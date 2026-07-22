# app.py
# A simple web UI for the SE Copilot, built with Streamlit.
# Run it:  streamlit run app.py

import streamlit as st
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

# --- setup (same as rag.py) ---
load_dotenv()
claude = Anthropic()

SYSTEM_PROMPT = (
    "You are a documentation assistant for a SaaS product. "
    "Answer the user's question using ONLY the documentation context provided in their message. "
    'If the answer is not in that context, say: "I don\'t have that information in the docs." '
    "Do not use outside knowledge and do not make anything up. "
    "Be concise, precise, and confident. "
    "If the user's question is ambiguous, ask one brief clarifying question before answering."
)

client = chromadb.PersistentClient(path=".chroma")
collection = client.get_collection("docs")

# --- the web page ---
st.title("🛠️ SE Copilot")
st.write("Ask a question and I'll answer using only the product docs.")

question = st.text_input("Your question:")

# run the RAG steps only when the button is clicked AND there's a question
if st.button("Ask") and question:
    with st.spinner("Searching the docs..."):
        # retrieve
        results = collection.query(query_texts=[question], n_results=2)
        chunks = results["documents"][0]
        context = "\n\n".join(chunks)

        # generate
        user_message = f"Context:\n{context}\n\nQuestion: {question}"
        message = claude.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        answer = message.content[0].text

    st.markdown("### Answer")
    st.write(answer)
