# Resume Editor Implementation Guide

## Overview
This guide outlines how to add in-browser editing functionality to allow users to edit formatted resumes before downloading.

## Architecture

### Workflow
1. **Format Resume** → DOCX generated
2. **Convert to HTML** → Use `mammoth.js` to convert DOCX to HTML
3. **Display in Editor** → Show HTML in TinyMCE/CKEditor
4. **User Edits** → Real-time editing in browser
5. **Convert Back** → Use `html-docx-js` to convert edited HTML back to DOCX
6. **Download** → User downloads the edited DOCX/PDF

## Backend Changes

### 1. Add New Dependencies
Add to `Backend/requirements.txt`:
```
mammoth==1.6.0
```

### 2. Create DOCX to HTML Conversion Endpoint
Add to `Backend/app.py`:

```python
@app.route('/api/convert-to-html/<filename>', methods=['GET'])
def convert_to_html(filename):
    """Convert DOCX to HTML for editing"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        import mammoth
        
        # Convert DOCX to HTML
        with open(file_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
            messages = result.messages
        
        return jsonify({
            'success': True,
            'html': html,
            'messages': [str(m) for m in messages]
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/save-edited-resume', methods=['POST'])
def save_edited_resume():
    """Save edited HTML back to DOCX"""
    try:
        data = request.get_json()
        html_content = data.get('html')
        original_filename = data.get('filename')
        
        if not html_content or not original_filename:
            return jsonify({'success': False, 'message': 'Missing data'}), 400
        
        # Generate new filename for edited version
        edited_filename = original_filename.replace('.docx', '_edited.docx')
        output_path = os.path.join(Config.OUTPUT_FOLDER, edited_filename)
        
        # Convert HTML back to DOCX using python-docx
        from docx import Document
        from docx.shared import Pt, Inches
        from bs4 import BeautifulSoup
        
        doc = Document()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Parse HTML and add to document
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol']):
            if element.name in ['h1', 'h2', 'h3']:
                para = doc.add_heading(element.get_text(), level=int(element.name[1]))
            elif element.name == 'p':
                para = doc.add_paragraph(element.get_text())
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    doc.add_paragraph(li.get_text(), style='List Bullet')
        
        doc.save(output_path)
        
        return jsonify({
            'success': True,
            'filename': edited_filename,
            'message': 'Resume saved successfully'
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
```

## Frontend Changes

### 1. Install Dependencies
```bash
cd frontend
npm install tinymce @tinymce/tinymce-react
# OR for CKEditor
npm install @ckeditor/ckeditor5-react @ckeditor/ckeditor5-build-classic
```

### 2. Create ResumeEditor Component

Create `frontend/src/components/ResumeEditor.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { Editor } from '@tinymce/tinymce-react';
import './ResumeEditor.css';

const ResumeEditor = ({ filename, onSave, onCancel }) => {
  const [htmlContent, setHtmlContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadHtmlContent();
  }, [filename]);

  const loadHtmlContent = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/convert-to-html/${filename}`);
      const data = await response.json();
      
      if (data.success) {
        setHtmlContent(data.html);
      } else {
        alert('Failed to load resume for editing');
      }
    } catch (error) {
      console.error('Error loading HTML:', error);
      alert('Error loading resume');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const response = await fetch('http://localhost:5000/api/save-edited-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          html: htmlContent,
          filename: filename
        })
      });

      const data = await response.json();
      
      if (data.success) {
        onSave(data.filename);
      } else {
        alert('Failed to save resume');
      }
    } catch (error) {
      console.error('Error saving:', error);
      alert('Error saving resume');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="editor-loading">
        <div className="spinner"></div>
        <p>Loading editor...</p>
      </div>
    );
  }

  return (
    <div className="resume-editor">
      <div className="editor-header">
        <h2>✏️ Edit Your Resume</h2>
        <div className="editor-actions">
          <button className="btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button className="btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving...' : '💾 Save & Download'}
          </button>
        </div>
      </div>
      
      <div className="editor-container">
        <Editor
          apiKey="your-tinymce-api-key-here"  // Get free key from tinymce.com
          value={htmlContent}
          onEditorChange={(content) => setHtmlContent(content)}
          init={{
            height: 600,
            menubar: true,
            plugins: [
              'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
              'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
              'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
            ],
            toolbar: 'undo redo | blocks | ' +
              'bold italic forecolor | alignleft aligncenter ' +
              'alignright alignjustify | bullist numlist outdent indent | ' +
              'removeformat | help',
            content_style: 'body { font-family:Arial,sans-serif; font-size:11pt; line-height:1.6; }',
            branding: false
          }}
        />
      </div>
    </div>
  );
};

export default ResumeEditor;
```

### 3. Create ResumeEditor CSS

Create `frontend/src/components/ResumeEditor.css`:

```css
.resume-editor {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.editor-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
}

.editor-actions {
  display: flex;
  gap: 12px;
}

.editor-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.editor-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### 4. Integrate Editor into DownloadPhase

Modify `DownloadPhase.js` to add an "Edit" button:

```javascript
// Add state for editor
const [editingFile, setEditingFile] = useState(null);

// Add edit handler
const handleEdit = (filename) => {
  setEditingFile(filename);
};

// Add in the file list rendering
<button 
  className="btn-edit"
  onClick={() => handleEdit(file.filename)}
>
  ✏️ Edit
</button>

// Add conditional rendering for editor
{editingFile && (
  <ResumeEditor
    filename={editingFile}
    onSave={(newFilename) => {
      setEditingFile(null);
      // Refresh file list or trigger download
    }}
    onCancel={() => setEditingFile(null)}
  />
)}
```

## Performance Optimizations

### 1. Lazy Loading
Only load the editor when user clicks "Edit" button

### 2. Caching
Cache converted HTML on backend to avoid repeated conversions

### 3. Compression
Use gzip compression for HTML content transfer

### 4. Async Operations
Make all conversions asynchronous to prevent blocking

## Testing Steps

1. **Install backend dependencies**: `pip install mammoth beautifulsoup4`
2. **Install frontend dependencies**: `npm install tinymce @tinymce/tinymce-react`
3. **Test DOCX to HTML conversion**: Format a resume and check `/api/convert-to-html`
4. **Test editor loading**: Click "Edit" button and verify HTML loads
5. **Test editing**: Make changes in editor
6. **Test saving**: Save changes and verify DOCX is generated
7. **Test download**: Download edited DOCX and verify changes

## Alternative: CKEditor Implementation

If you prefer CKEditor over TinyMCE:

```javascript
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

<CKEditor
  editor={ClassicEditor}
  data={htmlContent}
  onChange={(event, editor) => {
    const data = editor.getData();
    setHtmlContent(data);
  }}
  config={{
    toolbar: ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', '|', 'undo', 'redo']
  }}
/>
```

## Next Steps

1. Install PyMuPDF: `pip install PyMuPDF==1.23.8`
2. Install mammoth: `pip install mammoth beautifulsoup4`
3. Install TinyMCE: `npm install tinymce @tinymce/tinymce-react`
4. Implement the backend endpoints
5. Create the ResumeEditor component
6. Integrate into DownloadPhase
7. Test thoroughly

## Notes

- TinyMCE requires a free API key (get from tinymce.com)
- CKEditor is open-source and doesn't require an API key
- HTML to DOCX conversion may lose some formatting - consider using `python-docx-template` for better preservation
- Consider adding a "Preview" mode before saving
