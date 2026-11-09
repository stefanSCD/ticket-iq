# TicketIQ Source

This directory contains the implementation workspaces for TicketIQ. These are documentation-only scaffolds; runnable services and build configuration will be added by each workstream.

```text
src/
  services/
    rag/
    mcp/
    agent/
  frontend/
  contracts/
```

| Directory | Responsibility |
|---|---|
| [services/rag](services/rag/README.md) | Data ingestion, embeddings, index maintenance, and retrieval |
| [services/mcp](services/mcp/README.md) | MCP tools, Jira adapter, and approved ticket updates |
| [services/agent](services/agent/README.md) | Model integration, conversation API, agent logic, fine-tuning, and evaluation |
| [frontend](frontend/README.md) | Ticket selection, clarification, proposal review, and approval UI |
| [contracts](contracts/README.md) | Shared interface schemas and example payloads |

Each Python service will manage its own dependencies and Docker image. A repository-root `compose.yaml` is planned for local integration. Existing datasets, scripts, tests, and project documentation remain at the repository root.

See the [architecture](../docs/high-level-architecture.md), [work allocation](../docs/work.md), and [workflow example](../docs/workflow-example.md).

Behavior and integration references: [assessment rubric](../docs/assessment-rubric.md), [save reconciliation](../docs/save-reconciliation.md), and [integration scenarios and contract checks](../docs/integration-scenarios.md).
