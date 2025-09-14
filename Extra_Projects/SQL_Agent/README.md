# SQL Agent (LangChain, LangGraph, Gemini)

## Features
- Natural language to SQL agent using free Gemini API
- Schema discovery, agentic RAG, session memory
- FastAPI backend for API access
- Query logging, security validation, and alternative suggestions

## Setup
1. Fill in your API keys in `config.yaml` or `.env`.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `python -m uvicorn app.api.main:app --reload`

## API Endpoints
- `GET /schema` — Get current DB schema
- `POST /session/create` — Create a new session
- `GET /session/{session_id}/history` — Get session history
- `POST /query` — Ask a question (JSON: `{ "question": "...", "session_id": "..." }`)

## Example Query
```json
POST /query
{
	"question": "How many users are in the users table?",
	"session_id": "..."
}
```

## Security
- Only safe, read-only SELECT queries are allowed.
- All queries are validated and logged.

## Testing
- Run `pytest tests/` to execute automated tests.

## Project Structure
- `app/agent/` — Agent logic & suggestions
- `app/db/` — Database connection
- `app/schema/` — Schema discovery
- `app/memory/` — Session/context memory
- `app/api/` — FastAPI endpoints
- `app/utils/` — Utilities (prompt, RAG, validation, logging)
- `tests/` — Automated tests

## License
MIT
