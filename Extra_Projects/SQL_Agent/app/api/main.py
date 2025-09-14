from app.agent.suggestion import suggest_alternatives

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
class QueryRequest(BaseModel):
    question: str
    session_id: str = None
class SessionCreateResponse(BaseModel):
    session_id: str
class SessionHistoryResponse(BaseModel):
    history: list
from app.schema.discover import get_schema
from app.agent.langchain_agent import generate_sql
from app.db.connection import get_db
from sqlalchemy import text
from app.config import config
from app.memory.session import session_memory
from app.utils.rag import get_relevant_schema
from app.utils.prompt import build_prompt
from app.utils.logger import log_query
from app.utils.sql_validation import is_safe_sql

app = FastAPI()

@app.get("/schema")
def schema():
    return get_schema()

@app.post("/query")
async def query(request: QueryRequest):
    question = request.question
    session_id = request.session_id
    schema = get_schema()
    relevant_schema = get_relevant_schema(question, schema)
    history = session_memory.get_history(session_id) if session_id else None
    prompt = build_prompt(relevant_schema, question, history=history)
    sql = generate_sql(prompt)
    # Suggest alternatives if LLM output is empty or not a string
    if not sql or not isinstance(sql, str):
        suggestions = suggest_alternatives(question, relevant_schema)
        log_query(None, question, error=f"LLM did not return a string. Got: {type(sql)}")
        raise HTTPException(status_code=400, detail={"error": f"LLM did not return a string. Got: {type(sql)}", "suggestions": suggestions})
    if not isinstance(sql, str):
        log_query(None, question, error=f"LLM did not return a string. Got: {type(sql)}")
        raise HTTPException(status_code=400, detail=f"LLM did not return a string. Got: {type(sql)}")
    if not is_safe_sql(sql):
        suggestions = suggest_alternatives(question, relevant_schema)
        log_query(sql, question, error="Unsafe or non-SELECT SQL detected.")
        raise HTTPException(status_code=400, detail={"error": "Unsafe or non-SELECT SQL detected.", "suggestions": suggestions})
    db = next(get_db())
    try:
        result = db.execute(text(sql)).fetchall()
        columns = result[0].keys() if result else []
        rows = [dict(row) for row in result]
        response = {"query": sql, "result": rows, "explanation": f"Generated SQL for: {question}"}
        log_query(sql, question, result=rows)
        if session_id:
            session_memory.add_interaction(session_id, question, response)
        return response
    except Exception as e:
        suggestions = suggest_alternatives(question, relevant_schema)
        error_response = {"error": str(e), "query": sql, "suggestions": suggestions}
        log_query(sql, question, error=str(e))
        if session_id:
            session_memory.add_interaction(session_id, question, error_response)
        raise HTTPException(status_code=400, detail=error_response)

@app.post("/session/create", response_model=SessionCreateResponse)
async def create_session():
    session_id = session_memory.create_session()
    return {"session_id": session_id}

@app.get("/session/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str):
    return {"history": session_memory.get_history(session_id)}

