# 🚀 Quick Setup: OnlyOffice Integration

## ⚡ **5-Minute Setup**

### **Step 1: Install Docker Desktop (if not installed)**

Download: https://www.docker.com/products/docker-desktop/

### **Step 2: Start OnlyOffice Document Server**

Open PowerShell and run:

```powershell
docker run -i -t -d -p 8080:80 -e JWT_ENABLED=false --name onlyoffice-documentserver onlyoffice/documentserver
```

**Wait 2-3 minutes** for OnlyOffice to start, then verify:

```powershell
# Check if running
docker ps

# Test in browser
start http://localhost:8080/welcome/
```

You should see the OnlyOffice welcome page!

---

### **Step 3: Update Flask Backend**

**Edit**: `Backend/app.py`

Add these two lines after the existing imports:

```python
# Import OnlyOffice routes
from routes.onlyoffice_routes import onlyoffice_bp

# ... (existing code) ...

# Register OnlyOffice blueprint (add after app initialization)
app.register_blueprint(onlyoffice_bp)
```

**Full location** (around line 20):

```python
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

# Register OnlyOffice blueprint
app.register_blueprint(onlyoffice_bp)  # ← ADD THIS LINE

db = TemplateDB()
```

**Restart Flask**:
```powershell
# Press Ctrl+C to stop
python app.py
```

---

### **Step 4: Create React Component**

**Create file**: `src/components/OnlyOfficeEditor.jsx`

Copy the code from `ONLYOFFICE_INTEGRATION_GUIDE.md` (Section 3.1)

---

### **Step 5: Add "Edit" Button**

**Edit your results page** (wherever you show the formatted resume):

```jsx
import OnlyOfficeEditor from './components/OnlyOfficeEditor';

// Add state
const [showEditor, setShowEditor] = useState(false);

// Add button
<button onClick={() => setShowEditor(true)}>
  ✏️ Edit in Browser
</button>

// Add editor
{showEditor && (
  <OnlyOfficeEditor 
    filename={formattedFilename}
    onClose={() => setShowEditor(false)}
  />
)}
```

---

### **Step 6: Test!**

1. **Format a resume** using your app
2. Click **"Edit in Browser"**
3. **Edit the document** (change text, fonts, etc.)
4. **Save** (Ctrl+S)
5. **Close** - changes are saved!

---

## 🔧 **Troubleshooting**

### **OnlyOffice not starting?**

```powershell
# Check logs
docker logs onlyoffice-documentserver

# Restart
docker restart onlyoffice-documentserver
```

### **Port 8080 already in use?**

Change the port:
```powershell
docker run -i -t -d -p 9090:80 -e JWT_ENABLED=false --name onlyoffice-documentserver onlyoffice/documentserver
```

Then update `onlyoffice_routes.py`:
```python
ONLYOFFICE_URL = "http://localhost:9090"  # Change from 8080
```

### **CORS errors?**

Add to Flask `app.py`:
```python
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://localhost:3000",
        "http://localhost:8080"  # Add OnlyOffice
    ]
}})
```

---

## ✅ **Verification Checklist**

- [ ] Docker Desktop installed and running
- [ ] OnlyOffice container running (`docker ps`)
- [ ] OnlyOffice welcome page loads (http://localhost:8080/welcome/)
- [ ] Flask backend has OnlyOffice routes registered
- [ ] React component created
- [ ] "Edit" button added to UI
- [ ] Can open and edit documents in browser
- [ ] Changes save successfully

---

## 🎯 **What You Get**

✅ **Full MS Word-like editor** in your browser
✅ **No HTML conversion** - native .docx editing
✅ **All formatting preserved** (fonts, tables, styles)
✅ **Auto-save** - changes saved automatically
✅ **Professional UI** - looks like Microsoft Word
✅ **Free & open-source** - no licensing costs

---

## 📊 **System Requirements**

- **RAM**: 4GB minimum (OnlyOffice uses ~2GB)
- **Disk**: 5GB for Docker image
- **OS**: Windows 10/11, macOS, or Linux
- **Browser**: Chrome, Firefox, Edge, Safari

---

## 🚀 **Production Deployment** (Optional)

For production, enable JWT security:

```powershell
docker run -i -t -d -p 8080:80 \
  -e JWT_ENABLED=true \
  -e JWT_SECRET=your-random-secret-key-here \
  --name onlyoffice-documentserver \
  onlyoffice/documentserver
```

Then update `onlyoffice_routes.py` to include JWT token in config.

---

**That's it!** You now have a **professional document editor** integrated into your resume formatter! 🎉
