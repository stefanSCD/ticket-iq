# Model and Agent Service

**Owner:** Model and Agent workstream.

## Responsibilities

- Integrate the model, initially evaluating `Qwen3.5-4B`, and orchestrate MCP tools.
- Assess readiness, retrieve evidence, identify open decisions, and ask focused questions.
- Draft improved requirements and acceptance criteria with traceable sources.
- Preserve exact author clarification, revision, and decision messages as provenance for added or changed requirements; these messages never authorize saving. Retain RAG-issued citations from both searches and document reads before referencing them in proposals.
- Maintain conversation state, proposals, and approval records.
- Follow the [assessment rubric](../../../docs/assessment-rubric.md) for verdicts, evidence on assessments/questions, and proposal eligibility. Own bounded retrieval-run refresh; never relax scope or snapshot policy to recover evidence.
- Expose the conversation API used by the frontend.
- Request approved updates through MCP and confirm success only after a successful tool result.

## Fine-Tuning and Evaluation

- Run a functional baseline against golden references and save predictions and metrics.
- Fine-tune using only the training partition.
- Evaluate the fine-tuned model on the same evaluation examples with retrieval, prompts, and tool configuration held fixed.
- Use validation for adjustments and a held-out test partition for the final comparison.
- Report readiness, citations, clarification coverage, unnecessary questions, and latency by dataset.

Training and evaluation run as separate jobs, outside interactive conversations. Golden answers must never be included in evaluation inputs or retrieval context. Define missing dataset partitions before using those records.

## Interfaces

Expose the application API in the [Frontend ↔ Agent contract](../../contracts/frontend-agent/README.md), including authenticated session ownership, command deduplication, immutable proposals, and durable event polling in v1. Implement the client side of the [Agent ↔ MCP contract](../../contracts/agent-mcp/README.md), including trusted per-run context, output validation, and retrieval-generation pinning. Expose the four read tools to the model; invoke `update_ticket` deterministically from the stored approved proposal.

Implement the internal approval store and endpoints defined in the [MCP ↔ Agent Approval Records contract](../../contracts/mcp-agent-approvals/README.md). These handlers must remain available while the agent awaits an MCP tool call.

Implement Agent-owned administrative recovery transitions from the [reconciliation runbook](../../../docs/save-reconciliation.md). Preserve original results, keep the target guard during recovery synchronization, and publish final state only after MCP acknowledgement. Use the [integration scenarios](../../../docs/integration-scenarios.md) for cross-service acceptance.

See the [work allocation](../../../docs/work.md) and [normalized dataset documentation](../../../datasets/normalized/README.md).

Status: scaffold only. Add the agent, conversation API, training/evaluation jobs, dependency configuration, and Dockerfile here.
