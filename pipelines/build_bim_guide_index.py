from pathlib import Path
import re, pickle, faiss, pdfplumber, pytesseract
from sentence_transformers import SentenceTransformer
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT_DIR   = Path(__file__).resolve().parents[1]
DATA_DIR   = ROOT_DIR / "data"
RAW_DIR    = DATA_DIR / "raw"
INDEX_DIR  = DATA_DIR / "indexes"

PDF_PATH   = RAW_DIR / "BIM-Guide-07-v1.pdf"
EMBED_PATH = INDEX_DIR / "index1.faiss"
META_PATH  = INDEX_DIR / "meta1.pkl"

EMBED_MODEL = "all-MiniLM-L6-v2"       # light, fast
CHUNK_SIZE  = 1500
CHUNK_OVERL = 200

def main():
    pages = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            if not text.strip():
                img = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(img)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                pages.append(Document(
                    page_content=text,
                    metadata={"page_num": page_num}
                ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERL
    )
    chunks = splitter.split_documents(pages)

    embedder = SentenceTransformer(EMBED_MODEL)
    vecs = embedder.encode([c.page_content for c in chunks],
                           show_progress_bar=False)

    index = faiss.IndexFlatL2(vecs.shape[1])
    index.add(vecs)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(EMBED_PATH))
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("Index complete:", len(chunks), "chunks")

if __name__ == "__main__":
    main()
