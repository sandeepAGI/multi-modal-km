# Multi-Modal Knowledge Management Demo

This repository is the staging ground for an upgraded multi-modal knowledge management prototype. The current implementation showcases a Retrieval-Augmented Generation (RAG) workflow over construction PDFs, while the roadmap expands toward richer diagram understanding, cloud-friendly indexing jobs, and hosted LLM integrations. The existing apps remain useful as a baseline while we layer on those capabilities.

## Repository Structure

- `apps/streamlit/` – Streamlit entry points (`bid_set_app.py`, `bim_guide_app.py`) that drive the demo UI.
- `pipelines/` – Indexing scripts (`build_bid_set_index.py`, `build_bim_guide_index.py`) that transform PDFs into FAISS stores.
- `src/` – Reserved for shared ingestion, retrieval, and UI utilities as the project grows.
- `data/raw/` – Source PDFs used to seed the demo. Keep customer documents here locally.
- `data/indexes/` – Generated FAISS indexes and pickled metadata. Treat as build artifacts.
- `archive/simple_rag/` – Snapshot of the original flat demo for reference.
- `requirements.txt` – Python dependencies for the indexing and app layers.

## End-to-End Flow

1. **Extract PDF text** – `pdfplumber` reads each page; if the page is image-only, `pytesseract` performs OCR (requires Tesseract installed on the system).
2. **Normalize content** – Whitespace is collapsed and empty pages are skipped. Each retained page is wrapped in a LangChain `Document` containing the text and a `page_num` metadata field.
3. **Chunk the document** – `RecursiveCharacterTextSplitter` breaks pages into overlapping windows (`chunk_size=1500`, `chunk_overlap=200` characters) to balance context size with recall.
4. **Embed** – `SentenceTransformer("all-MiniLM-L6-v2")` generates dense vectors for every chunk.
5. **Index** – FAISS `IndexFlatL2` stores the vectors for fast cosine-similarity (via L2 on normalized vectors) search. Chunks are persisted to `meta*.pkl` so the original text and metadata can be retrieved later.
6. **Serve QA** – The Streamlit apps load the FAISS index and chunk metadata (cached with `st.cache_resource`), transform user questions into the same embedding space, pull the top `K=5` relevant chunks, and send the aggregated context plus the user question to an Ollama model (`mistral:7b-instruct-q4_K_M`).
7. **Display answers** – Answers are rendered in the Streamlit UI with a collapsible panel that shows the exact context supplied to the model (truncated to ≈3000 characters for readability).

## Environment Setup

1. **Python** – Use Python 3.9+ and create a fresh virtual environment.
2. **System Packages** – Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) so `pytesseract` can process image-only PDF pages. FAISS wheels are included via `faiss-cpu`, so no extra system install is required on most platforms.
3. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **LLM Endpoint** – The current Streamlit apps call a local Ollama server. Install [Ollama](https://ollama.ai/) and pull the demo model, or swap in your preferred endpoint when the new configuration layer lands:
   ```bash
   ollama pull mistral:7b-instruct-q4_K_M
   ollama serve  # ensures the API is listening on http://localhost:11434
   ```

## Building an Index

Run the corresponding script depending on which PDF you want to index. The script reads `PDF_PATH`, so update that constant if you replace the sample documents.

```bash
python pipelines/build_bid_set_index.py      # bids set drawings -> data/indexes/index.faiss
python pipelines/build_bim_guide_index.py    # BIM Guide -> data/indexes/index1.faiss
```

Each script prints the number of chunks created; successful execution generates both the FAISS index and the pickled metadata file in the repository root. Rerun the script whenever you change the PDF, chunking settings, or embedding model.

### Customizing for New Documents

- **PDF source** – Adjust `PDF_PATH` to point to your document.
- **Chunking** – Modify `CHUNK_SIZE` or `CHUNK_OVERL` if you need larger or smaller context windows.
- **Embedding model** – Replace `EMBED_MODEL` with any SentenceTransformer model. Remember to delete existing index files before rebuilding to avoid loading mismatched dimensions.

## Running the Streamlit App

Launch the app associated with the index you built:

```bash
streamlit run apps/streamlit/bid_set_app.py      # Uses data/indexes/index.faiss + meta.pkl
streamlit run apps/streamlit/bim_guide_app.py    # Uses data/indexes/index1.faiss + meta1.pkl
```

When you submit a question:
- The app embeds the query, performs a nearest-neighbor search in FAISS, and retrieves the top five chunk texts with their `page_num` metadata.
- The chunks are concatenated into a structured context block (prefixed with `[page N]`).
- A system prompt instructs the model to rely exclusively on the provided context, respond with "NOT FOUND" when necessary, and include page citations like `(page 7)`.
- The LLM endpoint (Ollama by default) returns the model's answer, which Streamlit displays immediately.

If the index or metadata files are missing, the app raises an error while loading. Ensure the appropriate `build_index*.py` script has been run first.

## Roadmap & Notes

- **Caching** – `st.cache_resource` ensures the FAISS index and embeddings are loaded once per Streamlit session. Restart the app (or clear cache via the Streamlit menu) if you regenerate the index.
- **OCR Accuracy** – OCR quality depends on your Tesseract installation and PDF clarity. For noisy scans, consider preprocessing or switching to a higher-quality OCR engine.
- **Model Endpoint** – The current helper hits Ollama synchronously. Upcoming work will introduce a pluggable configuration layer for hosted APIs (Anthropic, OpenAI, etc.) with retry handling and observability.
- **Diagram Awareness** – Enhancements in progress include layout-preserving extraction, vision-language embeddings, and richer metadata (bounding boxes, relationships) to surface diagram structure.
- **Scaling** – This demo uses an in-memory FAISS index (`IndexFlatL2`). The architecture will evolve toward cloud-friendly vector stores and batch ingestion jobs capable of handling thousands of diagrams.

## Next Steps

- Solidify the upgraded Streamlit layout (diagram selector, richer evidence display).
- Prototype enhanced ingestion that fuses OCR text with detected visual elements.
- Evaluate hosted LLMs as primary reasoning engines, retaining Ollama as an offline fallback.
- Add automated smoke tests covering index regeneration and core Q&A flows.
- Track milestone details and validation gates in `docs/roadmap.md`; update it after each planning review.
