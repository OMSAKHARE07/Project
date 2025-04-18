import React, { useEffect, useState } from 'react';
import './SummaryResult.css'; // Styles moved here for clarity
import { getSummaryResult } from '../services/apiService';

const SummaryResult = () => {
  const [summaryLines, setSummaryLines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getSummaryResult();
        const summaryText = data.text || 'No summary found.';
        const lines = summaryText
          .split(/[\n.]+/)
          .filter(line => line.trim().length > 30);
        
        for (let i = 0; i < lines.length; i++) {
          await new Promise(resolve => setTimeout(resolve, 250));
          setSummaryLines(prev => [...prev, '• ' + lines[i].trim()]);
        }
      } catch (err) {
        setSummaryLines(['Failed to load summary: ' + err.message]);
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  const goBack = () => {
    window.location.href = '/';
  };

  return (
    <div className="result-box">
      <h2>📝 Summarized Text</h2>
      <div className="progress-bar">
        <div className="progress" />
      </div>
      <div id="summaryText" className="summary-content">
        {loading && 'Preparing summary...'}
        {summaryLines.map((line, idx) => (
          <p key={idx}>{line}</p>
        ))}
      </div>
      <button onClick={goBack}>⬅️ Back to Upload</button>
    </div>
  );
};

export default SummaryResult;
