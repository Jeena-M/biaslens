import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  // Send text to backend Node API
  const analyze = async () => {
    if (!text.trim()) return; // prevent empty submission
    setLoading(true);
    setAnalysis(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error("Error fetching analysis:", err);
      alert("Failed to fetch analysis. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  // Highlight masculine/feminine words
  const highlightWords = () => {
    if (!analysis) return text;

    const suggestions = analysis.tailored_suggestions || {};
    const masculineWords = Object.keys(suggestions);
    const femWords = []; // optional: add feminine-coded words here

    return text.split(" ").map((word, idx) => {
      const cleanWord = word.toLowerCase().replace(/[.,!?]/g, "");

      if (masculineWords.includes(cleanWord)) {
        return (
          <span key={idx} className="masc-word">
            {word}{" "}
          </span>
        );
      }

      if (femWords.includes(cleanWord)) {
        return (
          <span key={idx} className="fem-word">
            {word}{" "}
          </span>
        );
      }

      return <span key={idx}>{word} </span>;
    });
  };

  return (
    <div className="container">
      <h2 class="title">BiasLens</h2>

      <textarea
        rows="6"
        placeholder="Enter text to analyze..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing…" : "Analyze"}
      </button>

      {loading && <p className="loading">Analyzing…</p>}

      {analysis && (
        <>
          {/* ---- HIGHLIGHTED TEXT ---- */}
          <h3>Highlighted Text</h3>
          <div className="highlight-box">{highlightWords()}</div>

          {/* ---- SUGGESTIONS ---- */}
          <div className="suggestion-box">
            <h4>Suggested Neutral Alternatives</h4>
            {Object.entries(analysis.tailored_suggestions).map(
              ([word, alternatives]) => (
                <div key={word} className="suggestion-item">
                  <strong>{word}</strong> → {alternatives.join(", ")}
                </div>
              )
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
