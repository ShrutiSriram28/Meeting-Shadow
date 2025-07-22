import React, { useState } from "react";
import VideoCall from "./components/VideoCall";
import AiPanel from "./components/AiPanel";

function App() {
  const [aiData, setAiData] = useState(null);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        height: "100vh",
        background: "#f9f9f9",
      }}
    >
      {/* Video Section */}
      <div
        style={{
          flex: "2", 
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "20px",
        }}
      >
        <div
          style={{
            width: "100%",
            maxWidth: "1000px",
            background: "#fff",
            borderRadius: "8px",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
          }}
        >
          <h1 style={{ textAlign: "center", marginBottom: "10px" }}>
            Cognitive Shadow
          </h1>
          <VideoCall onAiUpdate={setAiData} />
        </div>
      </div>

      {/* AI Panel */}
      <div
        style={{
          flex: "1", 
          borderLeft: "1px solid #ddd",
          padding: "20px",
          overflowY: "auto",
          background: "#fff",
        }}
      >
        <h2 style={{ textAlign: "center" }}>AI Insights</h2>
        <AiPanel data={aiData} />
      </div>
    </div>
  );
}

export default App;