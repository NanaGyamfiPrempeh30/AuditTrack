import React from "react";

function App() {
  return (
    <div style={{fontFamily: "Arial, sans-serif", padding: 24}}>
      <h1>AuditTrack Dashboard</h1>
      <p>Welcome — this is a minimal dashboard. Integrate charts and API calls here.</p>
      <ul>
        <li>Health: /healthz</li>
        <li>Events: /events (integration with API)</li>
      </ul>
    </div>
  );
}

export default App;
