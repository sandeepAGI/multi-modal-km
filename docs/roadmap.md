# Project Roadmap

This roadmap tracks the evolution of the multi-modal knowledge management demo. Each phase concludes only after automated checks and hands-on validation (including user walkthroughs) are documented. Update status fields as work progresses.

## Phase 0 – Baseline Audit (Complete)
- **Objectives**: Capture current RAG behavior, document repository layout, list known gaps.
- **Key Tasks**: Restructure repo, refresh contributor guide, push baseline to GitHub.
- **Exit Criteria**:
  - [x] Repo structure documented (`README`, `AGENTS`).
  - [x] Streamlit apps run end-to-end with existing indexes.
  - [x] Notes on missing functionality logged here.

## Phase 1 – Streamlit Experience Upgrade (Target: 2025-10-01)
- **Objectives**: Deliver multi-diagram UI with diagram selection, context previews, and richer evidence display.
- **Tasks**:
  - Design component layout (`apps/streamlit/` scaffolding, session state schema).
  - Implement diagram picker, chat-style responses, and citation cards.
  - Persist session transcripts for export or review.
- **Testing & Validation**:
  - Automated smoke: load app, submit scripted question set, assert response codes.
  - User session: demo with stakeholder, capture feedback and screenshots.
  - Exit when both automated checks pass and user sign-off recorded in this file (link to notes).

## Phase 2 – Enhanced Ingestion Pipeline (Target: 2025-10-01)
- **Objectives**: Extract layout-aware text and visual cues from diagrams and store enriched metadata.
- **Tasks**:
  - Evaluate PDF parsers/OCR combos (layout-aware extraction, vision models).
  - Implement pipeline that outputs chunk text + bounding boxes + entity tags.
  - Store derived metadata in structured format (`data/processed/` or vector DB).
- **Testing & Validation**:
  - Automated regression: compare extracted entities vs. golden set for sample pages.
  - Manual QA: review generated overlays/highlights on at least two diagrams with domain user.
  - Exit upon hitting accuracy thresholds agreed with stakeholders (document metrics here).

## Phase 3 – Retrieval & LLM Orchestration (Target: 2025-10-02)
- **Objectives**: Support hybrid retrieval and pluggable hosted LLMs with observability and fallbacks.
- **Tasks**:
  - Abstract retrieval interface to allow vector + keyword search and filters.
  - Integrate hosted LLM APIs (Anthropic/OpenAI) with configurable prompts.
  - Add logging/telemetry for latency, failures, and prompt/response storage.
- **Testing & Validation**:
  - Automated: unit tests for retrieval routing; integration test hitting mock/real API with retries.
  - User test: run scripted Q&A session verifying fallback behavior when primary model unavailable.
  - Exit when SLA targets met and monitoring dashboards set up (note links).

## Phase 4 – Scale & Evaluation Framework (Target: 2025-10-03)
- **Objectives**: Prepare for 1000+ diagrams with automated evaluation harnesses and deployment-ready packaging.
- **Tasks**:
  - Batch ingestion workflow (cloud job definitions, queueing).
  - Evaluation suite: question bank, scoring rubric, periodic reports.
  - Deployment artifacts (Docker, infra templates, security review).
- **Testing & Validation**:
  - Automated load test on representative dataset slice; capture resource metrics.
  - Stakeholder acceptance test covering end-to-end scenario on fresh data.
  - Exit when evaluation harness is repeatable and deployment checklist complete.

## Tracking & Updates
- Update this file after each planning session or phase review.
- Record blockers, decisions, and links to issues/PRs under the relevant phase.
- Always document the automated test results and user-testing feedback before marking a phase done.
- Start a **new** assistant session at the end of each phase, seeding the conversation with a short summary and links to prior context.
