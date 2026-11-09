# Shared Interface Contracts

This directory will hold agreed API/tool schemas and representative request, response, event, and error examples. It enables each workstream to develop against mocks before dependencies are available.

| Boundary | What to agree on |
|---|---|
| Frontend ↔ Agent | Sessions, ticket selection, clarification messages, progress, proposals, approval actions, and update results |
| Agent ↔ MCP | Tool inputs/outputs, project scope, citations, approval identifiers, ticket versions, and errors |
| MCP ↔ RAG | Queries, project/snapshot filters, result limits, document reads, and cited excerpts |
| MCP ↔ Agent approval records | Backend verification of approval for an exact proposal and ticket version |
| MCP ↔ Jira adapter | Ticket fields, versions, approved changes, and read/update results |

Each interface is agreed jointly by its producer and consumer. Coordinate breaking changes and update example payloads alongside schemas. Keep implementation code inside its owning service.

## Available Contracts

- [MCP ↔ Jira Adapter v1](mcp-jira-adapter/README.md): internal Python adapter operations, Jira Cloud REST v3 mapping, JSON Schema, example payloads, approval boundaries, and concurrency limitations.
- [MCP ↔ Agent Approval Records v1](mcp-agent-approvals/README.md): internal HTTP authorization/reservation, exact proposal binding, lifecycle, result reporting, JSON Schema, and mock examples.
- [MCP ↔ RAG v1](mcp-rag/README.md): scoped document/history search, temporal policies, exact citations, pinned document reads, JSON Schema, and mock examples.
- [Agent ↔ MCP v1](agent-mcp/README.md): five tool definitions, MCP transport/results, backend invocation context, downstream mappings, JSON Schema, and JSON-RPC examples.
- [Frontend ↔ Agent v1](frontend-agent/README.md): authenticated session API, conversation/proposals/evidence, explicit approval and revocation, durable progress polling, JSON Schema, and UI mock examples.

The five application boundaries above now have initial contracts. Ingestion/webhook operations and deployment/authentication setup remain separate implementation work. Contract examples are fixtures, not implemented services.

## Shared Behavioral Rules and Checks

The [assessment rubric](../../docs/assessment-rubric.md) defines readiness, evidence references, question handling, proposal eligibility, and evaluation. The [reconciliation runbook](../../docs/save-reconciliation.md) defines administrative recovery across Agent and MCP, separately from normal result reporting. The [integration scenarios](../../docs/integration-scenarios.md) map both documents to example payloads and acceptance checks.

These contracts are unpublished v1 drafts. Their README, schema, and examples are updated together; no deployed-client compatibility is implied. Run `python -m pip install -r requirements-dev.txt` and `python -m unittest discover -s tests` from the repository root to validate payloads, cross-contract references, and fixture invariants. These checks do not replace runtime authorization, persistence, concurrency, or semantic evidence tests.
