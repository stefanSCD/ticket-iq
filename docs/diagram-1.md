flowchart LR
    Jira["Jira<br/>New or updated tickets"]
    Docs["Project documentation<br/>Added or changed"]
    Webhook["Webhook receiver"]
    Queue["Event queue"]
    Ingest["Ingestion worker<br/>Normalize, deduplicate, chunk"]
    Embed["Qwen3-Embedding-0.6B"]
    DB[("PostgreSQL + pgvector<br/>Chunks, metadata, vectors")]

    Jira --> Webhook
    Docs --> Webhook
    Webhook --> Queue --> Ingest --> Embed --> DB

    User["Ticket author"]
    Agent["Ticket quality agent"]
    Model["Qwen3.5-4B"]
    MCP["MCP server<br/>Read-only tools"]
    JiraAPI["Jira API"]
    DocStore["Project docs"]
    Retrieval["Hybrid retrieval<br/>Vector + full-text search"]

    User -->|"New ticket / assessment request"| Agent
    Agent <--> Model
    Agent <--> MCP
    MCP -->|"get_ticket"| JiraAPI
    MCP -->|"get_document"| DocStore
    MCP -->|"search_docs / search_tickets"| Retrieval
    Retrieval <--> DB
    Agent -->|"Readiness, evidence, questions"| User
