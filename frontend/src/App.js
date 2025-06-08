import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Krypto Analyzer</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleAnalyze} style={{ marginLeft: '10px' }}>Analizuj</button>
      {result && (
        <div style={{ marginTop: '20px' }}>
          <h2>Decyzja: {result.decision}</h2>
          <p>Trend: {result.trend} (nachylenie: {result.slope.toFixed(4)})</p>
          <p>OCR: {result.text}</p>
          <p>Uzasadnienie: {result.reason}</p>
        </div>
      )}
    </div>
  );
}

export default App;
