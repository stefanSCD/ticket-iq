# Ingestion + RAG Service

**Owner:** Data Ingestion and RAG workstream.

## Responsibilities

- Ingest documentation and completed historical tickets using the existing normalized datasets.
- Chunk content, generate embeddings, and maintain PostgreSQL + pgvector storage.
- Handle duplicate sources, updates, and deletions.
- Provide dense and hybrid search with project isolation and snapshot filtering where supported.
- Issue and validate source identifiers, exact excerpts, and deterministic citations for both search hits and nonempty document-read pages under the shared MCP ↔ RAG citation rules.
- Run ingestion and embedding in a background worker separate from search requests.

## Interfaces

Implement the internal HTTP endpoints in the [MCP ↔ RAG contract](../../contracts/mcp-rag/README.md) for document search, historical-ticket search, and paginated reads of cited documents. Enforce authorized corpus/dataset/project scope, explicit temporal policies, and stable source/version provenance.

Ingestion job operations are a separate interface to be specified in [contracts](../../contracts/README.md).

This service alone owns the retrieval index. Index documentation and completed history only; review targets and golden answers must remain outside the retrieval corpus.

## Starting Point

- [Normalized dataset documentation](../../../datasets/normalized/README.md)
- [Existing normalization script](../../../scripts/normalize_datasets.py)
- Initial embedding candidate: `Qwen3-Embedding-0.6B`.

Status: scaffold only. Add service code, dependency configuration, worker entry point, and Dockerfile here.
