import React, { useState } from "react";

function App() {
  const [number, setNumber] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCall = async () => {
    setLoading(true);
    setStatus("");

    try {
      const response = await fetch("https://your-render-backend.onrender.com/make_call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ number }), // 👈 only send number
      });

      const result = await response.json();
      if (response.ok) {
        setStatus(result.message);
      } else {
        setStatus(`Error: ${result.error}`);
      }
    } catch (err) {
      setStatus(`Network error: ${err.message}`);
    }

    setLoading(false);
  };

  return (
    <div style={{ fontFamily: "sans-serif", textAlign: "center", marginTop: "100px" }}>
      <h2>AI Call Interface</h2>
      <input
        type="text"
        placeholder="Enter phone number (+972...)"
        value={number}
        onChange={(e) => setNumber(e.target.value)}
        style={{
          padding: "10px",
          width: "250px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          marginRight: "10px",
        }}
      />
      <button
        onClick={handleCall}
        disabled={loading}
        style={{
          padding: "10px 20px",
          backgroundColor: "#007BFF",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
        }}
      >
        {loading ? "Calling..." : "Call"}
      </button>

      {status && <p style={{ marginTop: "20px" }}>{status}</p>}
    </div>
  );
}

export default App;
