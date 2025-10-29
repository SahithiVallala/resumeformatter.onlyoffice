@echo off
echo ========================================
echo Installing Performance Optimizations
echo ========================================
echo.

echo [1/2] Installing Backend Dependencies...
cd Backend
pip install PyMuPDF==1.23.8 mammoth==1.6.0 beautifulsoup4==4.12.2
echo.

echo [2/2] Installing Frontend Dependencies...
cd ..\frontend
npm install tinymce @tinymce/tinymce-react
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart the backend server
echo 2. Reload the frontend
echo 3. Star button should now be clickable
echo 4. Thumbnails will load faster with caching
echo 5. Check EDITOR_IMPLEMENTATION_GUIDE.md for editing feature
echo.
pause
