# Python Services

The backend is divided into three independently developed services:

- [Ingestion + RAG](rag/README.md): owns ingestion and the retrieval index.
- [MCP](mcp/README.md): exposes tools and owns Jira access.
- [Agent](agent/README.md): owns the model orchestration and conversation API.

The request flow is frontend → Agent → MCP → RAG or Jira. Services communicate through agreed APIs rather than importing each other's implementation or reading each other's database tables.

Each service will have its own `pyproject.toml`, `Dockerfile`, configuration, and service-level checks. Agree on [contracts](../contracts/README.md) and mock responses before integration.

Status: directory scaffolds only; no services are runnable yet.
