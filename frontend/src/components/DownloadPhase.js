import React, { useState, useRef, useEffect } from 'react';
import { renderAsync } from 'docx-preview';
import './DownloadPhase.css';

const DownloadPhase = ({ results, onStartOver }) => {
  const [selectedPreview, setSelectedPreview] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const previewContainerRef = useRef(null);
  
  const handleDownload = (filename) => {
    window.open(`http://localhost:5000/api/download/${filename}`, '_blank');
  };
  
  const handlePreviewClick = async (result) => {
    setSelectedPreview(result);
    setPreviewLoading(true);
  };
  
  // Render DOCX preview when selected
  useEffect(() => {
    if (selectedPreview && previewContainerRef.current) {
      const loadPreview = async () => {
        try {
          // Fetch DOCX file as blob
          const response = await fetch(`http://localhost:5000/api/download/${selectedPreview.filename}`);
          const blob = await response.blob();
          
          // Clear previous preview
          previewContainerRef.current.innerHTML = '';
          
          // Render DOCX instantly in browser (no server conversion!)
          await renderAsync(blob, previewContainerRef.current);
          
          setPreviewLoading(false);
          console.log('✅ DOCX rendered instantly in browser!');
        } catch (error) {
          console.error('Preview error:', error);
          setPreviewLoading(false);
        }
      };
      
      loadPreview();
    }
  }, [selectedPreview]);


  const handleDownloadAll = () => {
    results.forEach((result, index) => {
      setTimeout(() => {
        handleDownload(result.filename);
      }, index * 500); // Stagger downloads by 500ms
    });
  };

  return (
    <div className="download-phase">
      <div className="download-layout">
        <div className="results-panel">
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
            <div 
              key={index} 
              className={`result-card ${selectedPreview?.filename === result.filename ? 'active' : ''}`}
              style={{ animationDelay: `${index * 0.1}s` }}
              onClick={() => handlePreviewClick(result)}
            >
              <div className="result-icon">
                📝
              </div>
              <div className="result-info">
                <h4>{result.name || 'Resume'}</h4>
                <p className="original-name">{result.original}</p>
                <div className="file-meta">
                  <span className="file-type">
                    DOCX
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

        {selectedPreview && (
          <div className="preview-panel">
            <div className="preview-header">
              <h3>📄 Preview</h3>
              <button 
                className="close-preview-btn"
                onClick={() => {
                  setSelectedPreview(null);
                  setPreviewLoading(false);
                }}
              >
                ✕
              </button>
            </div>
            <div className="preview-content">
              <div className="preview-file-info">
                <h4>{selectedPreview.name || 'Resume'}</h4>
                <p className="preview-original">{selectedPreview.original}</p>
              </div>
              <div className="preview-iframe-container">
                {previewLoading && (
                  <div className="preview-loading">
                    <div className="loading-spinner"></div>
                    <p>Loading preview...</p>
                  </div>
                )}
                {/* DOCX Preview Container - renders instantly in browser */}
                <div 
                  ref={previewContainerRef}
                  className="docx-preview-container"
                  style={{ display: previewLoading ? 'none' : 'block' }}
                />
              </div>
              <div className="preview-actions">
                <button
                  className="btn-download-preview"
                  onClick={() => handleDownload(selectedPreview.filename)}
                >
                  ⬇️ Download DOCX
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DownloadPhase;
