# 🔍 Troubleshooting: Editor Stuck on "Loading editor..."

## Quick Checks

### 1. Check OnlyOffice is Running
```powershell
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                        STATUS
xxxxx          onlyoffice/documentserver    Up X minutes
```

**If not running:**
```powershell
.\start_onlyoffice.ps1
```

---

### 2. Check OnlyOffice API is Accessible
Open in browser: http://localhost:8080/web-apps/apps/api/documents/api.js

**Expected:** JavaScript code should appear

**If 404 or error:**
- OnlyOffice is not running
- Port 8080 is blocked
- Docker container has issues

---

### 3. Check Browser Console (F12)
Look for these messages:

**Good:**
```
🔄 Loading editor for: filename.docx
✅ DocsAPI already loaded
📡 Fetching editor config...
📦 Config received: {...}
✅ Config valid, initializing editor...
🚀 Creating editor instance with ID: onlyoffice-editor-1234567890
✅ Editor loaded successfully!
```

**Bad - API Not Loading:**
```
⏳ Waiting for DocsAPI to load...
❌ DocsAPI failed to load after 10 seconds
```
**Solution:** Check OnlyOffice is running and accessible

**Bad - Config Error:**
```
❌ Failed to fetch config: 404
```
**Solution:** File not found in output folder

**Bad - Editor Creation Error:**
```
❌ Error creating editor: [error message]
```
**Solution:** Check the specific error message

---

### 4. Check Backend Logs
Look for:

**Good:**
```
✅ Using hardcoded local IP: 192.168.0.104
📡 OnlyOffice will use: http://192.168.0.104:5000
📡 Download URL: http://192.168.0.104:5000/api/onlyoffice/download/filename.docx
```

**Bad:**
```
⚠️  WARNING: Output directory does not exist
```
**Solution:** Create output directory

---

## Common Issues & Solutions

### Issue 1: "DocsAPI failed to load after 10 seconds"

**Cause:** OnlyOffice API script not loading

**Solutions:**
1. Check OnlyOffice is running: `docker ps`
2. Restart OnlyOffice: `docker restart [container-id]`
3. Check port 8080 is not blocked
4. Try accessing: http://localhost:8080

---

### Issue 2: "Failed to fetch editor config: 404"

**Cause:** File not found in output directory

**Solutions:**
1. Check file exists: `ls Backend/output/`
2. Verify filename matches
3. Re-format the resume

---

### Issue 3: Editor loads but shows error inside

**Cause:** OnlyOffice can't reach backend

**Solutions:**
1. Check backend is running on port 5000
2. Verify IP address in `onlyoffice_routes.py`:
   ```python
   backend_url = "http://192.168.0.104:5000"
   ```
3. Update IP to your machine's local IP:
   ```powershell
   ipconfig
   # Look for IPv4 Address under your network adapter
   ```

---

### Issue 4: "Container ref is null"

**Cause:** React component not mounted properly

**Solutions:**
1. Refresh the page (F5)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Restart frontend: `npm start`

---

## Step-by-Step Debug Process

### Step 1: Verify OnlyOffice
```powershell
# Check if running
docker ps

# If not, start it
.\start_onlyoffice.ps1

# Wait 30 seconds for it to fully start

# Test API
curl http://localhost:8080/web-apps/apps/api/documents/api.js
```

### Step 2: Verify Backend
```powershell
# Check backend is running
# Should see: "Running on http://127.0.0.1:5000"

# Test config endpoint
curl http://localhost:5000/api/onlyoffice/config/[your-filename].docx
```

### Step 3: Verify Frontend
```powershell
# Restart frontend
cd frontend
npm start

# Open browser console (F12)
# Click resume tab
# Watch console logs
```

### Step 4: Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Click resume tab
4. Look for:
   - `api.js` - Should be 200 OK
   - `config/filename.docx` - Should be 200 OK
   - `download/filename.docx` - Should be 200 OK

---

## Manual Test Commands

### Test OnlyOffice API
```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:8080/web-apps/apps/api/documents/api.js"
```

### Test Backend Config
```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/onlyoffice/config/formatted_xxx.docx"
```

### Test File Download
```powershell
# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/onlyoffice/download/formatted_xxx.docx" -OutFile "test.docx"
```

---

## Nuclear Option: Complete Reset

If nothing works:

```powershell
# 1. Stop everything
docker stop $(docker ps -q)
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# 2. Clear output folder
Remove-Item Backend\output\* -Force

# 3. Restart OnlyOffice
.\start_onlyoffice.ps1

# 4. Wait 30 seconds

# 5. Start backend
.\.venv\Scripts\Activate.ps1
cd Backend
python app.py

# 6. Start frontend (new terminal)
cd frontend
npm start

# 7. Format a fresh resume

# 8. Try preview
```

---

## Expected Console Output (Success)

```
🔄 Loading editor for: formatted_abc123.docx
🗑️ Destroying previous editor...
✅ DocsAPI already loaded
📡 Fetching editor config...
📦 Config received: {success: true, config: {...}}
✅ Config valid, initializing editor...
🚀 Creating editor instance with ID: onlyoffice-editor-1730483456789
📝 Editor config: {document: {...}, editorConfig: {...}}
✅ Editor loaded successfully!
```

---

## Get Help

If still stuck, provide:
1. Browser console output (F12)
2. Backend terminal output
3. `docker ps` output
4. `ipconfig` output
5. Screenshot of error

---

**Most common fix: Restart OnlyOffice Docker container!** 🔄
