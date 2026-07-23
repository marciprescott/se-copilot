# app.py
# Web UI for the SE Copilot. Runs locally AND on Streamlit Community Cloud.
# Local:  streamlit run app.py

import os
import glob
import streamlit as st
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

# --- API key: from .env locally, or Streamlit secrets in the cloud ---
load_dotenv()
if not os.environ.get("ANTHROPIC_API_KEY"):
    try:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass

claude = Anthropic()

SYSTEM_PROMPT = (
    "You are a documentation assistant for a SaaS product. "
    "Answer the user's question using ONLY the documentation context provided in their message. "
    'If the answer is not in that context, say: "I don\'t have that information in the docs." '
    "Do not use outside knowledge and do not make anything up. "
    "Be concise, precise, and confident. "
    "If the user's question is ambiguous, ask one brief clarifying question before answering."
)


# --- build the vector store from the docs folder (once, cached) ---
@st.cache_resource
def get_collection():
    client = chromadb.EphemeralClient()  # in-memory store, rebuilt on startup
    collection = client.get_or_create_collection("docs")
    if collection.count() == 0:
        i = 0
        for path in glob.glob("docs/*.md"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            words = text.split()
            for start in range(0, len(words), 200):
                chunk = " ".join(words[start : start + 200])
                collection.add(
                    ids=[str(i)],
                    documents=[chunk],
                    metadatas=[{"source": path}],
                )
                i += 1
    return collection


collection = get_collection()

# --- the web page ---
st.title("🛠️ Ask the docs")
st.write("Ask a question and I'll answer using only the product docs.")

question = st.text_input("Your question:")

if st.button("Ask") and question:
    with st.spinner("Searching the docs..."):
        results = collection.query(query_texts=[question], n_results=2)
        context = "\n\n".join(results["documents"][0])
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
