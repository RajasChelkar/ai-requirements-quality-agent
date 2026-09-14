from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE = PROJECT_ROOT / "Data" / "Knowledgebase"

CHROMA_PATH = PROJECT_ROOT / "Data" / "chroma_db"


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


collection = chroma_client.get_or_create_collection(
    name="requirements_guidance"
)


def load_knowledge_base():

    documents = []
    ids = []

    for file_path in KNOWLEDGE_BASE.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(text)
        ids.append(file_path.stem)

    return documents, ids


def index_knowledge_base():

    documents, ids = load_knowledge_base()

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    print(
        f"Indexed {len(documents)} knowledge documents."
    )

def retrieve_guidance(query, top_k=3):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results

def build_context(results):
    """Combine retrieved knowledge documents into a single context."""
    documents = results["documents"][0]

    context = "\n\n".join(
        f"GUIDANCE {i + 1}:\n{document}"
        for i, document in enumerate(documents)
    )

    return context

if __name__ == "__main__":
    index_knowledge_base()

    query = "The system should respond quickly to abnormal pressure."

    results = retrieve_guidance(query, top_k=3)

    print("\nRetrieved guidance:\n")

    for document in results["documents"][0]:
        print(document)
        print("-" * 50)