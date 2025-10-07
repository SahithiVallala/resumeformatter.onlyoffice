import React from 'react';
import './DownloadPhase.css';

const DownloadPhase = ({ results, onStartOver }) => {
  const handleDownload = (filename) => {
    window.open(`http://localhost:5000/api/download/${filename}`, '_blank');
  };

  const handleDownloadAll = () => {
    results.forEach((result, index) => {
      setTimeout(() => {
        handleDownload(result.filename);
      }, index * 500); // Stagger downloads by 500ms
    });
  };

  return (
    <div className="download-phase">
      <div className="success-animation">
        <div className="success-checkmark">
          <div className="check-icon">
            <span className="icon-line line-tip"></span>
            <span className="icon-line line-long"></span>
            <div className="icon-circle"></div>
            <div className="icon-fix"></div>
          </div>
        </div>
      </div>

      <div className="phase-header">
        <h2>🎉 Formatting Complete!</h2>
        <p>Your professionally formatted resumes are ready to download</p>
      </div>

      <div className="results-summary">
        <div className="summary-card">
          <div className="summary-icon">📄</div>
          <div className="summary-text">
            <span className="summary-number">{results.length}</span>
            <span className="summary-label">Resume{results.length !== 1 ? 's' : ''} Formatted</span>
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-icon">✨</div>
          <div className="summary-text">
            <span className="summary-number">100%</span>
            <span className="summary-label">Success Rate</span>
          </div>
        </div>
      </div>

      <div className="results-container">
        <div className="results-header">
          <h3>📥 Download Your Files</h3>
          {results.length > 1 && (
            <button className="download-all-btn" onClick={handleDownloadAll}>
              ⬇️ Download All ({results.length})
            </button>
          )}
        </div>

        <div className="results-grid">
          {results.map((result, index) => (
            <div key={index} className="result-card" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="result-icon">
                {result.filename.endsWith('.pdf') ? '📄' : '📝'}
              </div>
              <div className="result-info">
                <h4>{result.name || 'Resume'}</h4>
                <p className="original-name">{result.original}</p>
                <div className="file-meta">
                  <span className="file-type">
                    {result.filename.endsWith('.pdf') ? 'PDF' : 'DOCX'}
                  </span>
                  <span className="formatted-badge">✓ Formatted</span>
                </div>
              </div>
              <button
                className="download-btn"
                onClick={() => handleDownload(result.filename)}
              >
                <span className="download-icon">⬇️</span>
                <span className="download-text">Download</span>
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="action-buttons">
        <button className="btn-start-over" onClick={onStartOver}>
          🔄 Format More Resumes
        </button>
      </div>
    </div>
  );
};

export default DownloadPhase;
