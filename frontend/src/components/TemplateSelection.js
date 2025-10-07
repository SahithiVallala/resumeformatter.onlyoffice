import React, { useState } from 'react';
import './TemplateSelection.css';

const TemplateSelection = ({ templates, selectedTemplate, onSelect, onDelete, onUpload }) => {
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [templateName, setTemplateName] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!templateName || !file) {
      alert('Please provide template name and file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('template_name', templateName);
    formData.append('template_file', file);

    try {
      const response = await fetch('http://localhost:5000/api/templates', {
        method: 'POST',
        body: formData
      });

      // Handle non-JSON or error responses gracefully
      const contentType = response.headers.get('content-type') || '';
      if (!response.ok) {
        const errText = contentType.includes('application/json')
          ? JSON.stringify(await response.json())
          : await response.text();
        alert(`Upload failed (HTTP ${response.status}).\n${errText || 'No error body'}`);
        return;
      }

      const data = contentType.includes('application/json') ? await response.json() : { success: false, message: 'Unexpected response format' };
      if (data.success) {
        alert('Template uploaded successfully!');
        setShowUploadModal(false);
        setTemplateName('');
        setFile(null);
        // Refresh template list
        onUpload();
        // Auto-select the newly uploaded template and move to next step
        if (data.id) {
          onSelect(data.id);
        }
      } else {
        alert(data.message || 'Upload failed');
      }
    } catch (error) {
      console.error('Upload error', error);
      alert(`Error uploading template.\n${error?.message || ''}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="template-selection">
      <div className="phase-header">
        <h2>🎨 Choose Your Template</h2>
        <p>Select a template to format your resumes or add a new one</p>
      </div>

      <div className="templates-grid">
        {templates.map((template) => (
          <div
            key={template.id}
            className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
            onClick={() => onSelect(template.id)}
          >
            <div className="template-preview">
              <div className="template-icon">📄</div>
            </div>
            <div className="template-info">
              <h3>{template.name}</h3>
              <div className="template-meta">
                <span className="template-type">{(template.file_type || '').toUpperCase()}</span>
                <span className="template-date">
                  {(() => {
                    try {
                      const d = template.upload_date ? new Date(template.upload_date) : null;
                      return d && !isNaN(d.getTime()) ? d.toLocaleDateString() : 'Just now';
                    } catch (e) {
                      return 'Just now';
                    }
                  })()}
                </span>
              </div>
            </div>
            <button
              className="delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(template.id);
              }}
            >
              🗑️
            </button>
            {selectedTemplate === template.id && (
              <div className="selected-badge">
                <span>✓ Selected</span>
              </div>
            )}
          </div>
        ))}

        <div className="template-card add-template" onClick={() => setShowUploadModal(true)}>
          <div className="add-template-content">
            <div className="add-icon">+</div>
            <h3>Add New Template</h3>
            <p>Upload a custom template</p>
          </div>
        </div>
      </div>

      {templates.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No Templates Yet</h3>
          <p>Click the + button to upload your first template</p>
        </div>
      )}

      {showUploadModal && (
        <div className="modal-overlay" onClick={() => setShowUploadModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📤 Upload New Template</h3>
              <button className="close-btn" onClick={() => setShowUploadModal(false)}>×</button>
            </div>
            <form onSubmit={handleUpload} className="upload-form">
              <div className="form-group">
                <label>Template Name</label>
                <input
                  type="text"
                  placeholder="e.g., Company Standard Format"
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Template File (.pdf, .docx, .doc)</label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={(e) => setFile(e.target.files[0])}
                    required
                    id="file-input"
                  />
                  <label htmlFor="file-input" className="file-input-label">
                    {file ? file.name : 'Choose file...'}
                  </label>
                </div>
              </div>
              <div className="form-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowUploadModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={uploading}>
                  {uploading ? 'Uploading...' : 'Upload Template'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TemplateSelection;
