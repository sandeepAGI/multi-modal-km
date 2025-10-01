from pathlib import Path
import pickle, faiss, requests, streamlit as st
from sentence_transformers import SentenceTransformer

ROOT_DIR     = Path(__file__).resolve().parents[2]
INDEX_DIR    = ROOT_DIR / "data" / "indexes"
EMBED_PATH   = INDEX_DIR / "index1.faiss"
META_PATH    = INDEX_DIR / "meta1.pkl"
EMBED_MODEL  = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "mistral:7b-instruct-q4_K_M"
K            = 5

@st.cache_resource
def load_stack():
    index  = faiss.read_index(str(EMBED_PATH))
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    embedder = SentenceTransformer(EMBED_MODEL)
    return index, chunks, embedder

index, chunks, embedder = load_stack()

def retrieve(q):
    qv = embedder.encode([q], convert_to_numpy=True, return_norm=True)
    _, I = index.search(qv, K)
    return [chunks[i] for i in I[0]]

def ollama(system, prompt):
    r = requests.post("http://localhost:11434/api/generate",
                      json={"model": OLLAMA_MODEL,
                            "system": system,
                            "prompt": prompt,
                            "stream": False})
    return r.json()["response"]

system_msg = (
    "Answer using only the context. "
    "If answer not present, say 'NOT FOUND'. "
    "Cite page numbers like (page 7)."
)

st.title("Simple BIM‑Guide Q&A")

q = st.text_input("Ask:")
if q:
    ctx_docs = retrieve(q)
    context  = "\n\n".join(f"[page {d.metadata['page_num']}] {d.page_content}"
                           for d in ctx_docs)
    ans = ollama(system_msg, f"Context:\n{context}\n\nQ: {q}\nA:")
    st.markdown(ans)
    with st.expander("context"):
        st.code(context[:3000] + ("..." if len(context) > 3000 else ""))
