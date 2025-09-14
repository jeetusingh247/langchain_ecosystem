from typing import List

def suggest_alternatives(question: str, schema: dict) -> List[str]:
    # Simple heuristic: suggest queries for each table if question is ambiguous
    suggestions = []
    if len(schema) > 1:
        for table in schema:
            suggestions.append(f"Show all records from {table}")
    return suggestions
