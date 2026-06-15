# Samy

Samy is an AI Engineering Assistant designed for data professionals who work with cloud platforms, analytics, databases, software engineering, and modern data architectures.

The project was created to help engineers review code, optimize SQL queries, understand cloud architectures, improve data pipelines, and accelerate technical decision-making without depending entirely on general-purpose AI assistants.

Samy combines large language models, retrieval-augmented generation (RAG), and a curated knowledge base focused on Data Engineering, Data Analytics, Data Science, Database Administration, Python, SQL, Go, and Google Cloud Platform.

The goal is not to replace engineers. The goal is to help engineers make better technical decisions faster.

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

## Local Development

Samy is developed using Python and managed through UV.

The recommended workflow consists of cloning the repository, installing dependencies through UV, configuring Ollama locally, and starting the FastAPI service.

The project is designed to run locally with minimal infrastructure requirements.

## Deployment

Samy can be deployed as a standalone container and executed on platforms such as Google Cloud Run.

The deployment architecture was intentionally designed to remain simple, allowing individual developers and small teams to operate the platform without requiring complex infrastructure.

## CI/CD Workflows

Samy uses three GitHub Actions workflows to ensure quality and automate releases: `test.yml`, `build.yml`, and `deploy.yml`. The `test.yml` workflow runs unit, integration, and end-to-end tests on every push and pull request targeting `main`, using `uv` to install dependencies and `pytest` to execute tests in `tests/unit`, `tests/integration`, and `tests/e2e` (when those folders exist).

After tests, the `build.yml` workflow runs on every push to `main` and automatically generates a new semantic version tag based on conventional commits, using `mathieudutour/github-tag-action`. Whenever a tag matching `v*.*.*` is created, the `deploy.yml` workflow is triggered: it checks out the code, installs dependencies with `uv sync`, and runs `uv build` to generate distributable artifacts for the tagged release. In summary, the logic order is: **test in each push/PR → automatic tag in the main → build/deploy triggered by tag**.


## Open Source

Samy is an open-source project maintained by Data S2.

Contributions, ideas, experiments, bug reports, architectural discussions, and improvements are welcome.

The project evolves through practical engineering challenges, research, and continuous experimentation.

## Why Samy?

Samy was named in honor of Samuel Silvio Vieira Amancio, father of Data S2 founder.

Beyond technology, this project represents curiosity, learning, craftsmanship, and the belief that engineering is ultimately about helping people solve meaningful problems.

Every line of code, every review, every optimization, and every improvement is part of that journey.