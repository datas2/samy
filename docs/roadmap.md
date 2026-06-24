# Roadmap

Samy is an evolving project. This document outlines the short-term and medium-term roadmap for features, architecture and integrations.

## Short-term (0–3 months)

- **VS Code Extension**
  - Implement a basic VS Code extension that connects to Samy’s `/explain`, `/review` and `/optimize` endpoints.
  - Support per-file operations (explain this code, review this file, optimize this query).

- **RAG improvements**
  - Add better chunking strategies (e.g., code-aware chunking, headings-based chunking).
  - Introduce per-domain collections (e.g., `cloud`, `sql`, `python`) in the vector store.
  - Add relevance thresholds and ranking improvements.

- **Telemetry and Observability**
  - Expand telemetry events to include per-operation latency and error counts.
  - Provide a simple dashboard or script to summarize telemetry data (e.g., top operations, error types).

- **LLM configuration**
  - Expose configuration for multiple models (e.g., “fast” vs “quality” modes).
  - Improve fallback behavior and error messages when the LLM is unavailable.

## Medium-term (3–9 months)

- **User Profiles and Preferences**
  - Add user-level configuration (preferred model, languages, frameworks).
  - Persist user settings in the SQLite database (or an external store for production).

- **Advanced RAG**
  - Add support for external knowledge sources (e.g., Git repos, cloud documentation).
  - Implement per-project knowledge collections and dynamic routing between them.
  - Introduce confidence/uncertainty indicators in responses when knowledge is sparse.

- **Deeper Integrations**
  - Integrate with CI pipelines (e.g., GitHub Actions) for automated code review using Samy.
  - Provide a CLI that wraps the main API operations for terminal-based workflows.
  - Explore integration with other editors (e.g., JetBrains) and web UIs.

- **Scalability and Multi-tenant setups**
  - Add configuration and documentation for running Samy in multi-tenant environments.
  - Introduce quotas and rate limits per user or token.
  - Optionally integrate with managed vector stores and databases.

## Long-term (9+ months)

- **Domain-specific Skills**
  - Dedicated skills for:
    - BigQuery optimization,
    - Dataflow / Beam pipeline design,
    - Cloud Run / GKE deployments,
    - PostgreSQL performance tuning,
    - Observability and incident analysis.
  - Each skill with its own prompts, knowledge and evaluation criteria.

- **Evaluation and Benchmarks**
  - Build an evaluation harness to measure Samy’s effectiveness on real-world tasks.
  - Track improvements across versions and models (e.g., CodeGemma vs Qwen vs CodeLlama).
  - Collect anonymized metrics (opt-in) to improve prompts and retrieval.

- **Plugin / Skill System**
  - Design a plugin system that allows external contributors to add new skills:
    - custom prompts,
    - custom knowledge sources,
    - specialized pipelines per domain.
  - Ensure plugins remain isolated and safe to run.

## Additional documentation ideas

Beyond the architecture, deployment and roadmap docs, additional documentation that would be valuable includes:

- **API Reference**
  - Detailed description of each endpoint (`/health`, `/explain`, `/review`, `/optimize`), including request/response schemas.
  - Examples of payloads and responses.

- **VS Code Integration Guide**
  - How to configure the extension to point to a local or remote Samy instance.
  - Common workflows (explain selection, review file, optimize query).

- **Model Selection Guide**
  - Tradeoffs between different models (e.g., `qwen2.5-coder:3b` vs `codegemma:7b` vs `codellama:13b`).
  - Recommendations for local vs Cloud Run vs dedicated LLM servers.

These documents can be added incrementally as features land, ensuring the documentation stays aligned with the implementation.