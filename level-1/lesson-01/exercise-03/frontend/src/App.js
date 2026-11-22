import { useState } from "react";

function App() {
  const [goal, setGoal] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!goal.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const res = await fetch("/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Request failed");
      } else {
        setAnswer(data.answer);
      }
    } catch (err) {
      setError("Unable to reach the backend. Make sure the FastAPI server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Mini AI Agent</h1>
      <p>Ask about employee hours, name, email, or department.</p>

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          placeholder="e.g. Find employee hours"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          disabled={loading}
          style={styles.input}
        />
        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {error && <div style={styles.error}>{error}</div>}

      {answer && (
        <div style={styles.card}>
          <strong>Answer:</strong> {answer}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "system-ui, sans-serif",
    maxWidth: 560,
    margin: "40px auto",
    padding: 0 20,
    lineHeight: 1.5,
  },
  h1: { marginBottom: 8 },
  form: { display: "flex", gap: 10, marginBottom: 24 },
  input: {
    flex: 1,
    padding: 10,
    fontSize: 16,
    border: "1px solid #ccc",
    borderRadius: 6,
  },
  button: {
    padding: "10 20",
    fontSize: 16,
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
  },
  error: {
    color: "#dc2626",
    marginBottom: 16,
    padding: 10,
    background: "#fee2e2",
    borderRadius: 6,
  },
  card: {
    padding: 16,
    background: "#f0f9ff",
    border: "1px solid #bae6fd",
    borderRadius: 6,
  },
};

export default App;
