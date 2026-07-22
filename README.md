# 🛠️ SE Copilot

An AI documentation assistant that answers questions about a product using **only its official docs** — and honestly says *"I don't have that information in the docs"* instead of making things up.

Built as a hands-on learning project on the path to solutions engineering. It's a **Retrieval-Augmented Generation (RAG)** app: product documentation is split into chunks and embedded into a vector database, the most relevant pieces are retrieved for each question, and Claude answers using only that context.

## Why it's different

Ask a general chatbot about a product and it might confidently invent an answer. SE Copilot is **grounded**: it only answers from the documentation it's given, notes that it's drawing from the docs, and refuses to guess when the answer isn't there. For anything customer-facing, that trustworthiness is the entire point.

## Demo

<!-- Add a screenshot named demo.png to the repo, then this will show it: -->
![SE Copilot demo](demo.png)

## How it works

1. **Ingest** (`ingest.py`) — reads the docs and splits them into overlapping chunks.
2. **Embed & store** — each chunk is turned into an embedding (a numeric representation of its *meaning*) and saved in a local ChromaDB vector store for semantic search.
3. **Retrieve** (`rag.py` / `app.py`) — for a given question, the most semantically similar chunks are pulled from the store.
4. **Generate** — those chunks are handed to Claude with a strict grounding instruction, and Claude returns a concise, cited answer (or admits it doesn't know).

## Tech stack

- **Python**
- **Anthropic Claude API** — answer generation
- **ChromaDB** — local vector database + embeddings (semantic search)
- **Streamlit** — web UI

## Getting started

### Prerequisites
- Python 3.10+
- An Anthropic API key

### Setup

```bash
# clone and enter the project
git clone https://github.com/marciprescott/se-copilot.git
cd se-copilot

# create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# install dependencies
pip install anthropic chromadb python-dotenv streamlit

# add your API key (creates a .env file that is gitignored)
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Run it

```bash
# build the vector store from the docs
python3 ingest.py

# launch the web app
streamlit run app.py
```

Then open the local URL Streamlit prints, type a question, and ask. Prefer the terminal? Run `python3 rag.py` for a command-line version.

## Using your own docs

Drop `.md` or `.txt` files into the `docs/` folder and re-run `python3 ingest.py`. The included samples are a few pages of Stripe's documentation.

## Project structure

- `app.py` — Streamlit web UI
- `rag.py` — command-line version of the assistant
- `ingest.py` — builds the vector store from the docs
- `docs/` — source documentation
- `hello.py` — an early experiment from learning the Claude API

## What's next

- Show source citations inline with each answer
- Support switching between multiple document sets
- Add conversation memory for follow-up questions

---

*Built in public while learning. Feedback and suggestions welcome.*
