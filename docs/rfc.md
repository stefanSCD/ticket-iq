# RFC: TicketIQ — Context-Aware Ticket Refinement Agent

## 1. Problem
Tickets often look clear but leave out decisions that matter for a specific project. Developers then guess or chase stakeholders for answers, which causes delays and rework.

Development teams lack a reliable way to spot what a ticket leaves undecided before implementation starts, without filling those gaps with assumptions.

## 2. Existing approaches

| Tool | What it does | Gap for our case |
|---|---|---|
| Atlassian Rovo [1] | Rewrites descriptions, generates acceptance criteria, finds related Jira/Confluence content | Focuses on content assistance and discovery; has no dedicated loop to resolve every blocking ambiguity |
| IBM RQA [2] | Flags ambiguous wording and scores requirement quality using NLP | Built for formal requirements in IBM DOORS, not for interactive clarification of everyday Jira tickets |
| ClarifyGPT [3] | Detects ambiguity, asks clarifying questions, then generates code | Aimed at code generation; doesn't refine or update the ticket |

*Takeaway:* Ambiguity analysis and interactive clarification both work on their own. No existing tool combines them in a ticket-centered, context-aware workflow.

## 3. Proposal

*Core idea:* Ask only the questions that remain open after retrieving project context, then write the answers back into the ticket.

*Flow*
1. *Read* the ticket's description and acceptance criteria.
2. *Retrieve* relevant docs and related tickets (RAG).
3. *Separate* documented facts from open decisions.
4. *Ask* focused questions about the open decisions only.
5. *Draft* clearer requirements and acceptance criteria from the answers.
6. *Update* the ticket after the author confirms.

*Integrations:* Jira through MCP first, then documentation sources where available.

## 4. Goals / Non-goals

*Goals*
- Flag the gaps that block implementation.
- Reduce clarification back-and-forth.
- Make every added requirement traceable to a document or an author's answer.

*Non-goals*
- Filling gaps with assumptions.
- Editing tickets without the author's confirmation.
- Replacing the product owner's decisions.

## References
[1] Atlassian, Rovo AI features in Jira: https://support.atlassian.com/organization-administration/docs/atlassian-intelligence-features-in-jira-software/
[2] IBM, Overview of Engineering Requirements Quality Assistant: https://www.ibm.com/docs/en/erqa?topic=assistant-overview
[3] Mu et al., ClarifyGPT, FSE 2024: https://doi.org/10.1145/3660810
