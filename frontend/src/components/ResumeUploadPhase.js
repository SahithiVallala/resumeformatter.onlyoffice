import React, { useState } from 'react';
import './ResumeUploadPhase.css';

const ResumeUploadPhase = ({ selectedTemplate, templates, onFormatSuccess, onBack, isFormatting, setIsFormatting }) => {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);

  const selectedTemplateData = templates.find(t => t.id === selectedTemplate);

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(prev => [...prev, ...selectedFiles]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(prev => [...prev, ...droppedFiles]);
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleFormat = async () => {
    if (files.length === 0) {
      alert('Please upload at least one resume');
      return;
    }

    setIsFormatting(true);
    const formData = new FormData();
    formData.append('template_id', selectedTemplate);
    files.forEach(file => {
      formData.append('resume_files', file);
    });

    try {
      const response = await fetch('http://localhost:5000/api/format', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (data.success) {
        onFormatSuccess(data.files);
      } else {
        alert(data.message || 'Formatting failed');
        setIsFormatting(false);
      }
    } catch (error) {
      alert('Error formatting resumes');
      setIsFormatting(false);
    }
  };

  return (
    <div className="resume-upload-phase">
      <div className="phase-header">
        <h2>📤 Upload Candidate Resumes</h2>
        <p>Drop your resume files here or click to browse</p>
      </div>

      <div className="selected-template-info">
        <div className="template-badge">
          <span className="badge-label">Selected Template:</span>
          <span className="badge-name">{selectedTemplateData?.name}</span>
        </div>
        <button className="change-template-btn" onClick={onBack}>
          Change Template
        </button>
      </div>

      <div
        className={`dropzone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <div className="dropzone-content">
          <div className="upload-icon">📁</div>
          <h3>Drag & Drop Resume Files Here</h3>
          <p>or click to browse your computer</p>
          <div className="supported-formats">
            <span>Supports: PDF, DOCX</span>
          </div>
        </div>
        <input
          id="file-upload"
          type="file"
          multiple
          accept=".pdf,.docx,.doc"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
      </div>

      {files.length > 0 && (
        <div className="uploaded-files">
          <div className="files-header">
            <h3>📋 Uploaded Files ({files.length})</h3>
            <button className="clear-all-btn" onClick={() => setFiles([])}>
              Clear All
            </button>
          </div>
          <div className="files-list">
            {files.map((file, index) => (
              <div key={index} className="file-item">
                <div className="file-icon">
                  {file.name.endsWith('.pdf') ? '📄' : '📝'}
                </div>
                <div className="file-details">
                  <div className="file-name">{file.name}</div>
                  <div className="file-size">{(file.size / 1024).toFixed(2)} KB</div>
                </div>
                <button className="remove-file-btn" onClick={() => removeFile(index)}>
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="action-buttons">
        <button className="btn-back" onClick={onBack}>
          ← Back to Templates
        </button>
        <button
          className="btn-format"
          onClick={handleFormat}
          disabled={isFormatting || files.length === 0}
        >
          {isFormatting ? (
            <>
              <span className="spinner"></span>
              Formatting {files.length} resume(s)...
            </>
          ) : (
            <>
              ✨ Format {files.length} Resume{files.length !== 1 ? 's' : ''}
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ResumeUploadPhase;
