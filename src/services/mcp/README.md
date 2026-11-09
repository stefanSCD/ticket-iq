# MCP Service and Jira Integration

**Owner:** MCP Server and Jira Integration workstream.

## Responsibilities

- Expose `get_ticket`, `search_docs`, `get_document`, `search_tickets`, and `update_ticket` as MCP tools.
- Delegate retrieval to the RAG HTTP API.
- Read and update tickets through a Jira adapter, starting with a mock implementation.
- Validate tool inputs, project scope, and result limits.
- Validate recorded approval of the exact proposed changes and the expected ticket version before saving.
- Return clear results and errors to the Agent service.

## Interfaces

Implement the server side of the [Agent ↔ MCP contract](../../contracts/agent-mcp/README.md) over Streamable HTTP, including the five tool schemas, trusted invocation context, and structured results. This service calls the RAG API and Jira adapter. A frontend approval flag alone is insufficient for writes.

Only this service writes to Jira. Retrieval algorithms belong to RAG, and conversation orchestration belongs to Agent.

Use the [MCP ↔ RAG contract](../../contracts/mcp-rag/README.md) for context tools. Resolve trusted corpus/dataset/project scope, propagate the ticket snapshot policy, and forward exact excerpts and citation metadata without rewriting them.

Validate and register RAG-issued citations from search hits and document-read pages in the run context. Forward them to Agent for session evidence storage; MCP does not mint citation IDs or attach new text to an existing citation.

Propagate unavailable-generation/source errors without clearing the run pin or issuing a replacement search. Agent owns refresh under the [Agent ↔ MCP policy](../../contracts/agent-mcp/README.md#6-timeouts-cancellation-and-evaluation).

See the [MCP ↔ Jira Adapter contract](../../contracts/mcp-jira-adapter/README.md), [shared contracts](../../contracts/README.md), and [architecture](../../../docs/high-level-architecture.md).

Use the [MCP ↔ Agent Approval Records contract](../../contracts/mcp-agent-approvals/README.md) to reserve author approval before writing and report the adapter result afterward. MCP owns durable operation/attempt tracking so retries cannot dispatch duplicate updates.

Own uncertain-write investigation, durable dispatch fencing, and MCP's administrative recovery operations under the [reconciliation runbook](../../../docs/save-reconciliation.md). Coordinate with Agent without directly editing its database. Recovered operations can never dispatch again; all recovery acknowledgements must survive restart.

Status: scaffold only. Add the MCP server, adapters, dependency configuration, and Dockerfile here.
