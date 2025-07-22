import React from "react"

export default function AiPanel({ data }) {
    if (!data) return <p>No AI data yet.</p>;

    return (
        <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "10px" }}>
            <h3>Live Cognitive Shadow</h3>
            <p><strong>Transcript:</strong> {data.transcript}</p>
            <p><strong>Summary:</strong> {data.summary}</p>
            <p><strong>Contradictions:</strong> {data.decision_auditor}</p>
            <p><strong>Gaps:</strong> {data.cognitive_gaps}</p>
            <p><strong>Clarifications:</strong> {data.clarification_questions}</p>
        </div>
    );
}