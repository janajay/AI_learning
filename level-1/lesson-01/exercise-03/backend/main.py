from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GoalRequest(BaseModel):
    goal: str


def dummy_employee_tool(query: str) -> str:
    """Dummy tool that returns sample employee information."""
    query_lower = query.lower()
    if "hours" in query_lower:
        return "Employee hours: Mon-Fri 9:00 AM - 5:00 PM, 40 hours/week."
    if "name" in query_lower:
        return "Employee name: Vijay Kumar."
    if "email" in query_lower:
        return "Employee email: vijay@example.com."
    if "department" in query_lower:
        return "Employee department: Engineering."
    return f"No specific employee data found for: {query}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "dummy_employee_tool",
            "description": "Fetch sample employee information (hours, name, email, department).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]


def mock_llm(messages: list, tools: list) -> dict:
    """Simulates an LLM that decides whether to call a tool or answer directly."""
    user_content = ""
    for msg in messages:
        if msg.get("role") == "user":
            user_content = msg.get("content", "")
        elif msg.get("role") == "tool":
            tool_result = msg.get("content", "")
            return {
                "role": "assistant",
                "content": f"Based on the employee data: {tool_result}"
            }

    user_lower = user_content.lower()
    if any(k in user_lower for k in ["hours", "name", "email", "department", "employee"]):
        return {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "dummy_employee_tool",
                        "arguments": json.dumps({"query": user_content})
                    }
                }
            ]
        }

    return {
        "role": "assistant",
        "content": "I can help with employee hours, name, email, or department. Try asking about one of those."
    }


def agent_solve(goal: str) -> str:
    """Runs a 3-turn agent loop: ask LLM -> run tool if requested -> observe -> answer."""
    messages = [{"role": "user", "content": goal}]

    for _ in range(3):
        response = mock_llm(messages, TOOLS)
        messages.append(response)

        if not response.get("tool_calls"):
            return response.get("content", "")

        for tool_call in response["tool_calls"]:
            args = json.loads(tool_call["function"]["arguments"])
            result = dummy_employee_tool(args["query"])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(result)
            })

    return messages[-1].get("content", "")


@app.post("/api/agent")
def run_agent(req: GoalRequest):
    if not req.goal.strip():
        return {"error": "Goal is required"}
    answer = agent_solve(req.goal)
    return {"answer": answer}
