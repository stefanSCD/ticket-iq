# TicketIQ — Work Allocation

The project is divided into four workstreams, with one person responsible for each. The shared reference is [Milestone 2](milestone-2.md) and the [workflow example](workflow-example.md).

## 1. Data Ingestion and RAG

**Goal:** Provide relevant, traceable project context to the agent.

- Build on the existing normalized datasets and implement fixture ingestion/replay.
- Implement chunking and embedding generation, initially using `Qwen3-Embedding-0.6B`.
- Set up PostgreSQL + pgvector to store chunks, embeddings, and source metadata.
- Handle duplicate sources, updates, and deletions.
- Implement documentation and historical-ticket retrieval, starting with dense search and adding hybrid vector + full-text search.
- Enforce project isolation and source availability at the ticket snapshot where timestamps support it.
- Return relevant excerpts with document/ticket identifiers and citation metadata.

**Deliverable:** An ingestion pipeline and retrieval functions that the MCP workstream can expose as tools.

**Data boundary:** Index normalized documentation and completed historical tickets only. Review targets and golden answers must not enter the retrieval corpus.

## 2. Frontend

**Goal:** Let a ticket author complete the refinement workflow through a simple interface.

- Provide ticket selection and display the current description and acceptance criteria.
- Show the agent's assessment, supporting sources, and clarification questions.
- Allow the author to answer questions and request revisions.
- Display the proposed ticket changes for review.
- Provide explicit approval of the final proposal, separate from clarification answers.
- Show update success or failure based on the backend result.
- Integrate with the agent's conversation API; use mock responses while that API is being implemented.

**Deliverable:** A frontend covering ticket selection, clarification, proposal review, approval, and update confirmation.

## 3. MCP Server and Jira Integration

**Goal:** Give the agent controlled access to project context and ticket operations.

- Implement the MCP server and these tools:
  - `get_ticket(ticket_id)`
  - `search_docs(project_id, query, top_k)`
  - `get_document(project_id, doc_id)`
  - `search_tickets(project_id, query, top_k)`
  - `update_ticket(ticket_id, changes, approval_id, expected_version)`
- Connect search tools to the retrieval functions from workstream 1.
- Implement a mock Jira adapter for the initial working demo, with a clear adapter boundary for real Jira integration.
- Validate tool inputs, project scope, and result limits.
- Require recorded approval of the exact proposed changes and a matching ticket version before saving.
- Return clear read/update results and errors to the agent.

**Deliverable:** A working MCP tool layer and ticket adapter supporting reads and approved updates.

## 4. Model, Agent Logic, and Baseline vs Fine-Tuned Evaluation

**Goal:** Implement the reasoning and conversation flow, then measure whether fine-tuning improves it.

- Integrate the initial model candidate, `Qwen3.5-4B`, and connect it to the MCP tools.
- Implement the agent loop: read the ticket, retrieve context, distinguish documented facts from open decisions, ask focused questions, and draft improved requirements and acceptance criteria.
- Return `Ready`, `Needs clarification`, or `Insufficient evidence` as appropriate.
- Implement the shared [assessment rubric](assessment-rubric.md), including evidence on assessments/questions, no approvable partial proposals, and bounded evidence refresh owned by Agent.
- Track conversation state and the source of each added requirement: retrieved evidence or an author's answer.
- Expose the conversation API consumed by the frontend.
- Present proposals for review, pass recorded approval to the update tool, and confirm success only after the tool reports a successful save.
- Run the functional baseline model before fine-tuning and save its outputs and scores against the golden references.
- Prepare training examples from the training partition and fine-tune the model.
- Run the fine-tuned model on the same evaluation examples and compare it with the baseline.
- Report readiness F1, citation correctness, clarification-topic coverage, unnecessary questions, and latency. Include retrieval Recall@k when assessing the full RAG pipeline, and report results by dataset.

**Deliverable:** A functional agent and conversation API, a fine-tuned model, and a baseline-versus-fine-tuned results report.

**Evaluation boundary:** Golden records are evaluation references, not agent inputs. Use only the training partition for fine-tuning, validation for adjustments, and a held-out test partition for the final comparison. Define the missing PCON and TeamFlow splits before using those records in training or evaluation. Keep retrieval, prompts, tool configuration, and evaluation examples fixed when comparing model versions.

## Shared Integration Agreements

- Agree early on retrieval result schemas, MCP tool inputs/outputs, and the frontend-to-agent conversation API so all four workstreams can progress using mocks.
- Workstream 1 owns retrieval implementation; workstream 3 exposes it through MCP.
- Workstream 4 owns the conversation API; workstream 2 consumes it.
- Workstreams 2, 3, and 4 agree on how a proposal and its explicit approval are identified and recorded.
- Evaluation implementation can follow the first functional baseline, but dataset partitions and leakage boundaries must be established before fine-tuning.
- Use the [integration scenarios](integration-scenarios.md) as the common acceptance plan. MCP/Jira owns uncertain-write investigation; Agent owns approval/session recovery; a deployment operator coordinates the [reconciliation workflow](save-reconciliation.md). The recovery guard is released only after both services acknowledge the same outcome.
- The shared demo follows the documented workflow: ticket → evidence → clarification → proposal → explicit approval → update confirmation.
