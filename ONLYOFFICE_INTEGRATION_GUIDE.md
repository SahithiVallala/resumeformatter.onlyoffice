# 🚀 OnlyOffice Document Server Integration Guide

## 📋 **Overview**

This guide shows how to integrate **OnlyOffice Document Server** into your Resume Formatter application to enable **in-browser .docx editing** without converting to HTML.

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                            │
│                  (localhost:3000)                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OnlyOfficeEditor Component                          │  │
│  │  - Loads editor iframe                               │  │
│  │  - Fetches config from Flask                         │  │
│  │  - Displays .docx in MS Word-like interface          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
                    API Calls (config, download)
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend                             │
│                  (localhost:5000)                            │
│                                                              │
│  Routes:                                                     │
│  • /api/onlyoffice/config/<filename>  → Config JSON         │
│  • /api/onlyoffice/download/<filename> → Serve .docx        │
│  • /api/onlyoffice/callback/<filename> → Save edited doc    │
└─────────────────────────────────────────────────────────────┘
                            ↓ ↑
                    Document Server API
                            ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│              OnlyOffice Document Server                      │
│                  (localhost:8080)                            │
│                                                              │
│  • Renders .docx in browser                                 │
│  • Provides editing interface                               │
│  • Handles save callbacks                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 **Step 1: Install OnlyOffice Document Server**

### **Option A: Docker (Recommended)**

```bash
# Pull and run OnlyOffice Document Server
docker run -i -t -d -p 8080:80 \
  -e JWT_ENABLED=false \
  --name onlyoffice-documentserver \
  onlyoffice/documentserver
```

**Verify it's running:**
```
http://localhost:8080/welcome/
```

You should see the OnlyOffice welcome page!

### **Option B: Windows Installer**

Download from: https://www.onlyoffice.com/download-docs.aspx

---

## 🔧 **Step 2: Backend Integration (Flask)**

### **2.1: Create OnlyOffice Routes**

**File**: `Backend/routes/onlyoffice_routes.py` (Already created!)

This file provides:
- **Config endpoint**: Returns OnlyOffice editor configuration
- **Download endpoint**: Serves .docx files to OnlyOffice
- **Callback endpoint**: Receives edited documents from OnlyOffice

### **2.2: Register Routes in Flask**

**Edit**: `Backend/app.py`

Add these lines after the existing imports:

```python
# Import OnlyOffice routes
from routes.onlyoffice_routes import onlyoffice_bp

# Register blueprint
app.register_blueprint(onlyoffice_bp)
```

**Full example**:

```python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import os
import traceback
import json

from config import Config
from models.database import TemplateDB
from utils.advanced_template_analyzer import analyze_template
from utils.advanced_resume_parser import parse_resume

# Import OnlyOffice routes
from routes.onlyoffice_routes import onlyoffice_bp

# Try to import enhanced formatter
try:
    from utils.enhanced_formatter_integration import format_resume_intelligent
    print("✅ Enhanced intelligent formatter loaded")
except ImportError:
    from utils.intelligent_formatter import format_resume_intelligent
    print("⚠️  Using standard formatter")

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

# Register OnlyOffice blueprint
app.register_blueprint(onlyoffice_bp)

# ... rest of your app.py code ...
```

---

## ⚛️ **Step 3: Frontend Integration (React)**

### **3.1: Create OnlyOffice Editor Component**

**File**: `src/components/OnlyOfficeEditor.jsx`

```jsx
import React, { useEffect, useRef, useState } from 'react';

const OnlyOfficeEditor = ({ filename, onClose }) => {
  const editorRef = useRef(null);
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch OnlyOffice configuration from Flask backend
    const fetchConfig = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/onlyoffice/config/${filename}`);
        
        if (!response.ok) {
          throw new Error('Failed to load editor configuration');
        }
        
        const configData = await response.json();
        setConfig(configData);
        setLoading(false);
      } catch (err) {
        console.error('Error loading OnlyOffice config:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchConfig();
  }, [filename]);

  useEffect(() => {
    if (config && editorRef.current) {
      // Load OnlyOffice Document Editor
      const script = document.createElement('script');
      script.src = 'http://localhost:8080/web-apps/apps/api/documents/api.js';
      script.async = true;
      
      script.onload = () => {
        // Initialize OnlyOffice editor
        new window.DocsAPI.DocEditor(editorRef.current.id, config);
      };
      
      document.body.appendChild(script);
      
      return () => {
        document.body.removeChild(script);
      };
    }
  }, [config]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading editor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <p className="text-red-600 font-semibold">Error: {error}</p>
          <button 
            onClick={onClose}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 bg-white">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-100 border-b">
        <h2 className="text-lg font-semibold">{filename}</h2>
        <button
          onClick={onClose}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Close Editor
        </button>
      </div>
      
      {/* OnlyOffice Editor Container */}
      <div 
        id="onlyoffice-editor" 
        ref={editorRef}
        style={{ width: '100%', height: 'calc(100vh - 60px)' }}
      />
    </div>
  );
};

export default OnlyOfficeEditor;
```

### **3.2: Add "Edit in Browser" Button**

**Edit**: Your existing results/download page component

```jsx
import React, { useState } from 'react';
import OnlyOfficeEditor from './OnlyOfficeEditor';

const ResultsPage = ({ formattedFile }) => {
  const [showEditor, setShowEditor] = useState(false);

  if (showEditor) {
    return (
      <OnlyOfficeEditor 
        filename={formattedFile}
        onClose={() => setShowEditor(false)}
      />
    );
  }

  return (
    <div className="results-container">
      <h2>Resume Formatted Successfully!</h2>
      
      <div className="action-buttons">
        {/* Existing download button */}
        <a 
          href={`http://localhost:5000/api/download/${formattedFile}`}
          download
          className="btn btn-primary"
        >
          Download Resume
        </a>
        
        {/* NEW: Edit in Browser button */}
        <button
          onClick={() => setShowEditor(true)}
          className="btn btn-secondary"
        >
          ✏️ Edit in Browser
        </button>
      </div>
    </div>
  );
};

export default ResultsPage;
```

---

## 🧪 **Step 4: Testing**

### **4.1: Start All Services**

**Terminal 1 - OnlyOffice:**
```bash
docker start onlyoffice-documentserver
# Or if not started yet:
docker run -i -t -d -p 8080:80 -e JWT_ENABLED=false --name onlyoffice-documentserver onlyoffice/documentserver
```

**Terminal 2 - Flask Backend:**
```bash
cd Backend
python app.py
```

**Terminal 3 - React Frontend:**
```bash
cd frontend  # or wherever your React app is
npm start
```

### **4.2: Test the Flow**

1. **Format a resume** using your existing flow
2. Click **"Edit in Browser"** button
3. **OnlyOffice editor should open** with the formatted resume
4. **Make edits** (change text, formatting, etc.)
5. **Save** (Ctrl+S or File → Save)
6. **Close editor** - file is automatically saved to `Backend/output/`

---

## 🔍 **Troubleshooting**

### **Issue 1: OnlyOffice not loading**

**Check:**
```bash
# Verify OnlyOffice is running
curl http://localhost:8080/welcome/

# Check if API script is accessible
curl http://localhost:8080/web-apps/apps/api/documents/api.js
```

**Fix**: Restart Docker container
```bash
docker restart onlyoffice-documentserver
```

### **Issue 2: CORS errors**

**Symptom**: Console shows CORS policy errors

**Fix**: Add OnlyOffice URL to Flask CORS config:

```python
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://localhost:3000",
        "http://localhost:8080"  # Add OnlyOffice
    ]
}})
```

### **Issue 3: Document not saving**

**Check callback endpoint**: Add logging to `onlyoffice_routes.py`:

```python
@onlyoffice_bp.route('/api/onlyoffice/callback/<filename>', methods=['POST'])
def save_callback(filename):
    data = request.json
    print(f"📥 Callback received: {data}")  # DEBUG
    
    status = data.get('status')
    print(f"📊 Status: {status}")  # DEBUG
    
    # ... rest of code ...
```

---

## 🎨 **Customization Options**

### **Disable Features**

Edit `onlyoffice_routes.py` config:

```python
"customization": {
    "autosave": True,
    "forcesave": True,
    "comments": False,      # Disable comments
    "chat": False,          # Disable chat
    "compactHeader": True,  # Compact UI
    "compactToolbar": True, # Compact toolbar
    "hideRightMenu": True,  # Hide right sidebar
    "plugins": False        # Disable plugins
}
```

### **Read-Only Mode**

```python
"editorConfig": {
    "mode": "view",  # Change from "edit" to "view"
    # ...
}
```

---

## 📊 **Comparison: OnlyOffice vs Alternatives**

| Feature | OnlyOffice | Mammoth.js | HTML Editor |
|---------|-----------|------------|-------------|
| Native .docx editing | ✅ Yes | ❌ Converts to HTML | ❌ Converts to HTML |
| Preserves formatting | ✅ 100% | ⚠️ ~70% | ⚠️ ~50% |
| Tables support | ✅ Full | ⚠️ Basic | ⚠️ Basic |
| Fonts preserved | ✅ Yes | ❌ No | ❌ No |
| Self-hosted | ✅ Yes | ✅ Yes | ✅ Yes |
| Free | ✅ Yes (Community) | ✅ Yes | ✅ Yes |
| Setup complexity | ⚠️ Medium | ✅ Easy | ✅ Easy |

**Winner**: OnlyOffice for your use case! 🏆

---

## 🚀 **Next Steps**

1. ✅ **Install OnlyOffice** using Docker
2. ✅ **Add routes** to Flask backend (already created!)
3. ✅ **Create React component** (code provided above)
4. ✅ **Test the integration**
5. 🎯 **Deploy** (optional: use cloud OnlyOffice or self-host)

---

## 📚 **Resources**

- **OnlyOffice API Docs**: https://api.onlyoffice.com/editors/basic
- **Docker Hub**: https://hub.docker.com/r/onlyoffice/documentserver
- **GitHub**: https://github.com/ONLYOFFICE/DocumentServer
- **Community Forum**: https://forum.onlyoffice.com/

---

## 💡 **Pro Tips**

1. **JWT Security**: For production, enable JWT authentication:
   ```bash
   docker run -e JWT_ENABLED=true -e JWT_SECRET=your-secret-key ...
   ```

2. **Cloud Hosting**: Use OnlyOffice Cloud if you don't want to self-host:
   - https://www.onlyoffice.com/cloud-service.aspx

3. **Mobile Support**: OnlyOffice works on mobile browsers too!

4. **Collaboration**: Enable real-time collaboration by setting unique user IDs

---

**You're all set!** 🎉 OnlyOffice will give you a **professional MS Word-like editing experience** directly in your browser, with **zero formatting loss**!
