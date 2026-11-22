def build_sql_prompt(schema: str, question: str) -> str:
    return f"""
You are a MySQL expert. Write a single MySQL query to answer the user's question.

Rules:
- Use only the tables and columns defined in the schema below.
- Never use SELECT *. Always list explicit columns.
- Do not reference any table or column not present in the schema.
- Return only the SQL query, no markdown fences, no explanation.

Schema:
{schema}

Question:
{question}

SQL:
""".strip()


if __name__ == "__main__":
    schema = """
users(id, name, email, created_at)
"""

    question = "Find users created this week"

    print(build_sql_prompt(schema, question))