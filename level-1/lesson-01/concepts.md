# AI Fundamentals

You are an experienced full-stack developer (PHP, React, Python, MySQL). Think of AI engineering as assembling familiar building blocks in a new arrangement. Here is how the five core concepts differ, how they work together, and what they look like in your stack.

---

## 1. LLM (Large Language Model)

**What it is:** A pre-trained neural network that predicts the next token given a sequence of text. It has weights, not memory. It does not "know" your database schema, your React components, or your PHP session unless you tell it.

**Analogy for a full-stack dev:** It is like a stateless API endpoint you call over HTTP. You send a request (text), you get a response (text). It has no built-in connection to MySQL, no access to `$_SESSION`, and no idea what `useState` does unless you describe it.

**Example (Python):**
```python
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a PHP function that connects to MySQL."}
    ],
)
print(response.choices[0].message.content)
```

The LLM is just the `model` parameter above. Everything else around it is orchestration.

---

## 2. Prompt

**What it is:** The text you send to the LLM. It contains instructions, examples, and data. A prompt is not a program; it is a string that steers the model's output.

**Analogy:** It is the HTTP request body you POST to the LLM API. Bad prompt = bad response, just like bad SQL = bad result set.

**Example (React frontend sending a prompt to a backend):**
```jsx
const prompt = `
You are a senior PHP developer. Review this code for SQL injection vulnerabilities.
Return only the vulnerable lines and a fix.

Code:
<?php
$id = \$_GET['id'];
$result = mysqli_query($conn, "SELECT * FROM users WHERE id = $id");
?>
`;

const res = await fetch("/api/review", {
  method: "POST",
  body: JSON.stringify({ prompt }),
});
```

The prompt is the `prompt` string. The LLM consumes it; your code constructs it.

---

## 3. Context

**What it is:** The relevant information you inject into the prompt so the LLM can answer accurately. Context is not stored inside the model; it is placed inside the prompt at inference time.

**Analogy:** It is like passing `$_GET`, `$_POST`, or Redux state into a function so it has the data it needs. Without context, the LLM is guessing.

**Example (Python injecting MySQL schema into the prompt):**
```python
schema = """
Table: users
Columns: id INT, email VARCHAR(255), created_at DATETIME
"""

prompt = f"""
You are a MySQL expert. Use this schema:
{schema}

Write a query to find users created in the last 7 days.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)
```

The `schema` string is context. It lives in your Python variable, not in the LLM's weights.

---

## 4. Tools

**What it is:** Functions the LLM can choose to call. The LLM does not execute the tool; it returns a structured request (usually JSON) telling *your code* which function to run and with what arguments. Your code runs it and returns the result to the LLM.

**Analogy:** It is like an AJAX call from React. The frontend (LLM) decides it needs data, requests it, and your backend (your PHP/Python code) executes the actual work and returns the payload.

**Example (Python defining a tool the LLM can call):**
```python
import json

def get_user_email(user_id: int) -> str:
    conn = mysql.connector.connect(host="localhost", user="root", database="app")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "Not found"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user_email",
            "description": "Look up a user's email by ID from MySQL",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"}
                },
                "required": ["user_id"]
            }
        }
    ]
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is the email of user 42?"}],
    tools=tools,
)

# The LLM may respond with a tool call instead of plain text
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
email = get_user_email(args["user_id"])
print(email)
```

The LLM never touches MySQL directly. It asks your Python function to do it.

---

## 5. AI Agent

**What it is:** A loop that combines an LLM, prompts, context, and tools. The agent decides what to do, calls tools, observes results, and repeats until the task is complete. It has autonomy; a simple prompt-response does not.

**Analogy:** It is like a React Redux saga or a PHP job worker: it receives a goal, dispatches actions (tool calls), processes responses, and loops until the goal is met.

**Example (Python agent loop):**
```python
def agent_solve(question: str):
    messages = [{"role": "user", "content": question}]
    
    for _ in range(5):  # safety limit
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if not msg.tool_calls:
            return msg.content  # final answer
        
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = get_user_email(args["user_id"])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

answer = agent_solve("Find the email of user 42 and tell me if it contains 'example.com'")
print(answer)
```

The agent is the `for` loop plus the tool-calling logic. The LLM is just one step inside it.

---

## How They Work Together

```
User Goal
    │
    ▼
┌─────────────┐
│   Agent     │  (loop: decide → act → observe)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    LLM      │  (predicts next token; stateless)
└──────┬──────┘
       │  prompt (string)
       ▼
┌─────────────┐
│   Context   │  (schema, user data, chat history injected into prompt)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Tools    │  (PHP/MySQL/React functions the LLM can request)
└─────────────┘
```

**Concrete full-stack scenario:** A user asks, "Export all users created this week to CSV."

1. **Agent** receives the goal.
2. **LLM** decides it needs to query MySQL, so it requests the `query_database` tool.
3. **Context** (the `users` table schema) is injected into the prompt so the LLM writes valid SQL.
4. **Tool** (`query_database`) runs the SQL against MySQL and returns rows.
5. **Agent** receives the rows, asks the LLM to format them as CSV, and returns the file to the user.

---

## Exercises

Complete these before moving to the next lesson. You should be able to explain each answer out loud.

### Exercise 1: Prompt + Context (Python)
Write a Python function `build_sql_prompt(schema: str, question: str) -> str` that takes a MySQL schema string and a natural-language question, and returns a prompt instructing the LLM to write a safe MySQL query using only the provided tables. Include an instruction to never use `SELECT *`.

### Exercise 2: Tool + LLM (PHP)
Create a PHP script that defines a callable tool `get_user_by_email(email)` which queries a MySQL `users` table. Simulate an LLM tool-call response (a JSON array with `name` and `arguments`) and show your PHP code executing the function and returning the result to the "LLM."

### Exercise 3: Mini Agent (React + Python)
Build a simple React frontend with a text input. When submitted, it sends the user's goal to a Python backend. The backend runs a 3-turn agent loop: (1) ask the LLM what to do, (2) if a tool is requested, run a dummy tool (e.g., return hardcoded data), (3) return the final answer to the frontend. Display the answer in the UI.

---

**Stop here.** Do not proceed to Lesson 2 until you can:
- Explain the difference between an LLM and an Agent in one sentence.
- Describe where Context lives (inside the prompt, not inside the model).
- Write a tool definition and explain who executes it (your code, not the LLM).
