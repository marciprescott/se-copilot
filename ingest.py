# ingest.py
# Reads your docs, chops them into chunks, and stores them in a searchable vector database.
# Run once (and again whenever your docs change):  python3 ingest.py

import glob  # finds files matching a pattern, like docs/*.md
import chromadb  # the local vector database that makes our chunks searchable

# --- Step 1: find all the doc files ---
# glob.glob returns a LIST of file paths, e.g. ["docs/stripe-payments.md", "docs/stripe-keys.md"]
paths = glob.glob("docs/*.md")


# --- Step 2: read each file and chop it into chunks ---
# all_chunks is created OUTSIDE the loop so it survives every lap and keeps growing.
all_chunks = []

for path in paths:  # each lap, `path` = one file path from the list
    # open the file and read all of its text into `text`
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()  # split the text into a list of individual words

    # walk through the words 200 at a time: 0, 200, 400, ...
    for i in range(0, len(words), 200):
        chunk = " ".join(
            words[i : i + 200]
        )  # grab a 200-word slice, join back into one string
        all_chunks.append(
            {"text": chunk, "source": path}
        )  # store text + which file it came from

# this runs ONCE, after the loop finishes, so it shows the final total
print(f"Collected {len(all_chunks)} chunks")


# --- Step 3: set up the vector database (once, after collecting) ---
# PersistentClient saves the database to a ".chroma" folder on disk so it survives between runs
client = chromadb.PersistentClient(path=".chroma")
# a "collection" is like a table; ours is named "docs" and holds our chunk-vectors
collection = client.get_or_create_collection("docs")


# --- Step 4: load every chunk into the database ---
for i, chunk in enumerate(
    all_chunks
):  # enumerate gives a counter `i` AND the chunk each lap
    collection.upsert(
        ids=[str(i)],  # a unique label per chunk: "0", "1", "2"...
        documents=[
            chunk["text"]
        ],  # the text Chroma turns into numbers (embeds) for search
        metadatas=[
            {"source": chunk["source"]}
        ],  # keep the source so the bot can cite it later
    )

print("Stored all chunks in the vector database.")
# --- Quick test: search the database ---
results = collection.query(
    query_texts=["how do I keep my API keys safe?"],
    n_results=2,
)
for doc in results["documents"][0]:
    print(doc)
    print("----")
