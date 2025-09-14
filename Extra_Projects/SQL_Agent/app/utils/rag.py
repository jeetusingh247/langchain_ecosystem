from typing import Dict, List
import re

def extract_relevant_tables(question: str, schema: Dict) -> List[str]:
    """
    Naive keyword-based retrieval: returns table names that appear in the question.
    """
    tables = list(schema.keys())
    found = []
    for table in tables:
        if re.search(rf"\b{re.escape(table)}\b", question, re.IGNORECASE):
            found.append(table)
    return found

def get_relevant_schema(question: str, schema: Dict) -> Dict:
    """
    Returns a subset of the schema containing only relevant tables.
    """
    relevant_tables = extract_relevant_tables(question, schema)
    if not relevant_tables:
        # fallback: return all tables (or top N)
        return dict(list(schema.items())[:3])
    return {t: schema[t] for t in relevant_tables}
