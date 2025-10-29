@echo off
echo ========================================
echo Installing ML Dependencies for Smart Section Mapping
echo ========================================
echo.

echo Step 1: Installing sentence-transformers...
pip install sentence-transformers==2.2.2
echo.

echo Step 2: Installing fuzzywuzzy...
pip install fuzzywuzzy==0.18.0 python-Levenshtein==0.21.1
echo.

echo Step 3: Installing spaCy...
pip install spacy==3.7.2
echo.

echo Step 4: Downloading spaCy English model...
python -m spacy download en_core_web_sm
echo.

echo ========================================
echo ✅ Installation Complete!
echo ========================================
echo.
echo The smart section mapper is now ready to use.
echo It will automatically handle:
echo   - Section name variations (Work Experience → Employment History)
echo   - Typos and misspellings
echo   - Missing section headings
echo   - Synonym matching (Summary → Professional Profile)
echo.
pause
