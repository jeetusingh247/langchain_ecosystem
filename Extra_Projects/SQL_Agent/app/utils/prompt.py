def build_prompt(schema, question, history=None, examples=None):
    prompt = """
You are an advanced SQL Agent. Given the following database schema and user question, generate a safe, read-only SQL query.

Schema:
{schema}

"""
    if history:
        prompt += f"Session History: {history}\n\n"
    if examples:
        prompt += f"Example Queries: {examples}\n\n"
    prompt += f"User Question: {question}\nSQL:"
    return prompt
