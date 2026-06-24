# Samy

Samy is an AI Engineering Assistant designed for data professionals who work with cloud platforms, analytics, databases, software engineering, and modern data architectures.

The project was created to help engineers review code, optimize SQL queries, understand cloud architectures, improve data pipelines, and accelerate technical decision-making without depending entirely on general-purpose AI assistants.

Samy combines large language models, retrieval-augmented generation (RAG), and a curated knowledge base focused on Data Engineering, Data Analytics, Data Science, Database Administration, Python, SQL, Go, and Google Cloud Platform.

The goal is not to replace engineers. The goal is to help engineers make better technical decisions faster.

## Why Samy?

Samy was named in honor of Samuel Silvio Vieira Amancio, father of Data S2 founder.

Beyond technology, this project represents curiosity, learning, craftsmanship, and the belief that engineering is ultimately about helping people solve meaningful problems.

Every line of code, every review, every optimization, and every improvement is part of that journey.

## Vision

Modern AI assistants know a little about everything. Samy follows a different path.

Instead of becoming another general-purpose assistant, Samy is being built as a specialized engineering companion that understands real-world data systems, cloud architectures, operational constraints, software quality, and platform-specific best practices.

The long-term vision is to create an engineering assistant capable of reasoning like an experienced data professional while remaining transparent, extensible, and open.

## What Samy Can Do

Samy can review Python code, analyze SQL statements, explain complex architectures, suggest improvements for cloud-native solutions, identify performance bottlenecks, and assist with common engineering tasks.

As the project evolves, Samy will expand its capabilities through specialized skills and knowledge domains, allowing deeper expertise in topics such as BigQuery optimization, Dataflow design, Cloud Run deployments, PostgreSQL administration, observability, and distributed systems.

## Architecture

Samy is built around a modular architecture composed of a user interface layer, a backend service layer, a retrieval layer, a knowledge layer, and a language model layer.

The backend is powered by FastAPI and exposes APIs used by clients such as the VS Code extension and future web interfaces.

The retrieval layer indexes technical documentation, engineering playbooks, and domain-specific knowledge stored within the project repository.

The language model layer can operate with local models through Ollama or connect to external providers when required.

This architecture allows Samy to remain lightweight, portable, and extensible.

## Knowledge Base

A core principle of Samy is that knowledge matters more than model size.

The project maintains a growing collection of engineering references, architectural patterns, operational playbooks, technical notes, and implementation guides.

This knowledge base becomes part of the assistant's reasoning process and allows responses to reflect practical engineering experience rather than generic internet knowledge.

## Utility Scripts

Samy provides a small set of utility scripts to help manage the local database, knowledge base and embeddings. All scripts live under the `scripts/` directory and can be executed with `uv run` or plain `python` from the project root.

### Database backup

The `backup_db.py` script creates a timestamped backup of the SQLite database:

```bash
uv run python scripts/backup_db.py
# or
python scripts/backup_db.py
```

By default, it copies `backend/database/sqlite.db` into a `backups/` directory with a name such as `sqlite_20250101_120000.db`.

### Building embeddings
The `build_embeddings.py` script walks through the `knowledge/` directory, chunks its contents and generates embeddings using the configured Ollama model, storing them in the vector store:

```bash
uv run python scripts/build_embeddings.py
# or
python scripts/build_embeddings.py
```

This is a convenient way to (re)build embeddings after adding or updating knowledge files.

### Importing playbooks
The `import_playbooks.py` script copies playbook files into the knowledge base under `knowledge/playbooks`:

```bash
uv run python scripts/import_playbooks.py /path/to/your/playbooks
# or
python scripts/import_playbooks.py /path/to/your/playbooks
```

This helps keep operational/engineering playbooks versioned within the Samy repository and available for RAG.

### Synchronizing knowledge
The `sync_knowledge.py` script re-ingests all files under the `knowledge/` directory into the vector store:

```bash
uv run python scripts/sync_knowledge.py
# or
python scripts/sync_knowledge.py
```

Use this when the knowledge base changes and you want the vector store to reflect the current state (for example, after importing new playbooks or updating documentation).



## CI/CD Workflows

Samy uses three GitHub Actions workflows to ensure quality and automate releases: `test.yml`, `build.yml`, and `deploy.yml`. The `test.yml` workflow runs unit, integration, and end-to-end tests on every push and pull request targeting `main`, using `uv` to install dependencies and `pytest` to execute tests in `tests/unit`, `tests/integration`, and `tests/e2e` (when those folders exist).

After tests, the `build.yml` workflow runs on every push to `main` and automatically generates a new semantic version tag based on conventional commits, using `mathieudutour/github-tag-action`. Whenever a tag matching `v*.*.*` is created, the `deploy.yml` workflow is triggered: it checks out the code, installs dependencies with `uv sync`, and runs `uv build` to generate distributable artifacts for the tagged release. In summary, the logic order is: **test in each push/PR → automatic tag in the main → build/deploy triggered by tag**.


## Open Source

Samy is an open-source project maintained by Data S2.

Contributions, ideas, experiments, bug reports, architectural discussions, and improvements are welcome.

The project evolves through practical engineering challenges, research, and continuous experimentation.

## Contributing

Contributions are welcome. If you find a bug, have an idea, or want to improve the code, you can:

1. Open an issue describing the problem or proposal.
2. Fork the repository and create a feature branch.
3. Install dependencies with `uv sync` and run tests with `uv run pytest`.
4. Open a pull request against the `master` branch.

Please keep commits focused and include context in the PR description.