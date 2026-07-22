# rag.py
# Ask a question, retrieve matching chunks, and have Claude answer using ONLY those chunks.
# Run it:  python3 rag.py

import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

# load the API key from .env and create the Claude client
load_dotenv()
claude = (
    Anthropic()
)  # named 'claude' so it doesn't clash with the Chroma 'client' below

# grounding rule: Claude answers ONLY from the provided context
SYSTEM_PROMPT = (
    "You are a documentation assistant for a SaaS product. "
    "Answer the user's question using ONLY the documentation context provided in their message. "
    'If the answer is not in that context, say: "I don\'t have that information in the docs." '
    "Do not use outside knowledge and do not make anything up. "
    "Be concise, precise, and confident. "
    "If the user's question is ambiguous, ask one brief clarifying question before answering."
)

# connect to the SAME database ingest.py built
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_collection("docs")

# get the question from the user
question = input("What is your question?  ")

# search the store for the most relevant chunks
results = collection.query(
    query_texts=[question],
    n_results=2,
)

# bundle the retrieved chunks into one context block
chunks = results["documents"][0]
context = "\n\n".join(chunks)

# build one message that gives Claude the context AND the question
user_message = f"Context:\n{context}\n\nQuestion: {question}"

# ask Claude, grounded by the system prompt
message = claude.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": user_message}],
)

# print Claude's grounded answer
print(message.content[0].text)
