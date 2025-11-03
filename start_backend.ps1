# Start Flask Backend with Virtual Environment
Write-Host "`n======================================================================"
Write-Host "🚀 Starting Flask Backend"
Write-Host "======================================================================`n"

# Activate virtual environment
Write-Host "1️⃣ Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Navigate to backend
Write-Host "2️⃣ Starting Flask server..."
cd Backend
python app.py
