# Exercise 3 – Mini AI Agent

Combines a React frontend, Python FastAPI backend, mock LLM, dummy employee tool, and a 3-turn agent loop.

## Architecture

```
React frontend
  User enters: "Find employee hours"
      │
      ▼
Python FastAPI backend
  Receives the user's goal
      │
      ▼
Agent loop
  Decides → calls tool → observes result → responds
      │
      ▼
Dummy employee tool
  Returns sample employee information
```

## Files

- `backend/main.py` — FastAPI server with the agent loop and mock LLM.
- `frontend/src/App.js` — React UI with a text input and answer display.
- `frontend/src/index.js` — React entry point.
- `frontend/public/index.html` — HTML shell.

## How it works

1. The user submits a goal (e.g., "Find employee hours").
2. The backend runs `agent_solve(goal)`:
   - Turn 1: mock LLM receives the goal and decides to call `dummy_employee_tool`.
   - Turn 2: `dummy_employee_tool` runs and returns sample employee data; the result is fed back as a `tool` message.
   - Turn 3: mock LLM observes the tool result and produces the final answer.
3. The answer is returned to the frontend and displayed.

## Running

### Backend

```powershell
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload --port 5000
```

The server runs on `http://127.0.0.1:5000`.

### Frontend

```powershell
cd frontend
npm install
npm start
```

The app opens on `http://localhost:3000` and proxies API calls to the FastAPI backend.

## Example goals to try

- "Find employee hours" → returns Mon-Fri 9:00 AM - 5:00 PM
- "What is the employee name?" → returns Vijay Kumar
- "What is the employee email?" → returns vijay@example.com
- "What department?" → returns Engineering
- "Hello" → no tool match → direct answer
