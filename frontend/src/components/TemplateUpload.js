import React, { useState } from 'react';
import { FiUpload } from 'react-icons/fi';

const TemplateUpload = ({ onUploadSuccess }) => {
  const [templateName, setTemplateName] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!templateName || !file) {
      alert('Please provide template name and file');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('template_name', templateName);
    formData.append('template_file', file);

    try {
      const response = await fetch('http://localhost:5000/api/templates', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      
      if (data.success) {
        alert('Template uploaded successfully!');
        setTemplateName('');
        setFile(null);
        onUploadSuccess();
      } else {
        alert(data.message || 'Upload failed');
      }
    } catch (error) {
      alert('Error uploading template');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2><FiUpload /> Upload Resume Template</h2>
      <p className="info-text" style={{fontSize: '0.9em', color: '#666', marginBottom: '10px'}}>
        ⚠️ <strong>Note:</strong> For best results, use <strong>.pdf</strong> or <strong>.docx</strong> templates. 
        Old .doc format has limited support.
      </p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Template Name (e.g., Company Standard Format)"
          value={templateName}
          onChange={(e) => setTemplateName(e.target.value)}
          required
        />
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Uploading...' : 'Upload Template'}
        </button>
      </form>
    </div>
  );
};

export default TemplateUpload;
