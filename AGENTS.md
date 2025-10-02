# Repository Guidelines

## Project Structure & Module Organization
- `apps/streamlit/` contains the active Streamlit entry points (e.g., `bid_set_app.py`, `bim_guide_app.py`).
- `pipelines/` houses indexing jobs that transform PDFs under `data/raw/` into FAISS stores in `data/indexes/`.
- `src/` is reserved for shared ingestion, retrieval, and configuration utilities; create modules here instead of copying logic between scripts.
- `archive/simple_rag/` preserves the original flat demo for quick reference. Keep it untouched unless you need to backport fixes.

## Build, Test, and Development Commands
- `python pipelines/build_bid_set_index.py` rebuilds the Holabird bid-set index; rerun after changing the PDF or chunking parameters.
- `python pipelines/build_bim_guide_index.py` does the same for the BIM Guide document.
- `streamlit run apps/streamlit/bid_set_app.py` (or `bim_guide_app.py`) launches the respective UI; confirm Ollama is serving before running.
- `ollama pull mistral:7b-instruct-q4_K_M` fetches the local fallback LLM. Swap the tag if using a different model.
- `python scripts/build_clip_image_embeddings.py` renders golden-set PDFs to images and stores CLIP page embeddings in `data/clip_embeddings/` for vision experiments.
- `python scripts/embedding_benchmark.py --models …` compares embedding providers (text-only, Gemini, CLIP, or fusion). Use `fusion:text=<provider/model>,clip=<clip model>` with `--fusion-alpha` to weight text vs image similarity.

## Coding Style & Naming Conventions
- Use 4-space indentation, `snake_case` for functions/variables, and PascalCase for classes.
- Define configuration constants in uppercase near the top of each module; prefer `pathlib.Path` for filesystem work.
- Factor reusable routines into `src/` modules with clear docstrings rather than duplicating code across apps and pipelines.

## Testing Guidelines
- Add smoke checks or notebooks alongside new ingestion features; document how you validated OCR, chunking, and retrieval changes.
- Before opening a PR, rebuild the relevant index and run at least one representative question in the Streamlit UI, noting results in the PR description.
- When automated tests are introduced, place them under `tests/` with file names mirroring the module under test (e.g., `test_retrieval.py`).

## Commit & Pull Request Guidelines
- Write concise, imperative commit messages (`Refactor ingestion paths`, `Add diagram selector UI`).
- Pull requests should outline the motivation, summarize the solution, list verification steps, and include screenshots or terminal captures for UI/CLI changes.
- Reference any related tickets and request review from teammates responsible for ingestion when touching shared pipelines or `src/` utilities.

## Security & Configuration Tips
- Keep client PDFs local; do not commit them or generated FAISS artifacts. Add placeholders or sample data instead.
- Store environment-specific settings (Ollama host, API keys) in `.env` files ignored by git and load them via configuration helpers.
