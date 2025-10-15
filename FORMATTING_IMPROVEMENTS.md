# Resume Formatting Improvements

## Overview
Updated the resume parser and formatter to produce clean, single-line formatted output for Employment History and Education sections.

## Desired Format

### Employment History
```
INFOSYS - DEVELOPER                                    2021-2025
  • Led development of enterprise applications
  • Managed team of 5 developers
  • Implemented microservices architecture

TECH SOLUTIONS INC - SOFTWARE ENGINEER                 2018-2021
  • Developed web applications
  • Integrated third-party APIs
```

### Education
```
MASTER OF SCIENCE IN DATA SCIENCE  PS UNIVERSITY       2020-2022
  • Specialized in Machine Learning
  • GPA: 3.8/4.0

BACHELOR OF TECHNOLOGY  STATE TECHNICAL UNIVERSITY     2014-2018
  • Graduated with Honors
```

## Changes Made

### 1. Parser Improvements (`advanced_resume_parser.py`)

#### Experience Extraction
- **Pattern Recognition**: Detects "Role + Dates" on first line, "Company Name" on second line
- **Example Input**:
  ```
  • Information Technology Technician I Aug 2007 to Current
  • Company Name – City, State
  ```
- **Extracted Fields**:
  - `company`: "Company Name" (location removed)
  - `role`: "Information Technology Technician I"
  - `duration`: "2007-2025"
  - `details`: Following bullet points

#### Education Extraction
- **Pattern Recognition**: Detects degree + institution, extracts year
- **Example Input**:
  ```
  • Bachelor of Science, Information Technology 2005
  Florida International University – City, State
  ```
- **Extracted Fields**:
  - `degree`: "Bachelor of Science, Information Technology"
  - `institution`: "Florida International University"
  - `year`: "2005"
  - `details`: Coursework, etc.

#### Unicode Normalization
- Removes garbage characters: `ï¼`, `â€"`, `–`, `—`
- Normalizes to clean ASCII dashes and quotes
- Strips location info: "City, State", "India", "USA", etc.

### 2. Formatter Improvements (`word_formatter.py`)

#### Structured Table Layout
- Creates borderless 2-column tables for each entry
- **Left column (70% width)**: `COMPANY - ROLE` (uppercase, bold)
- **Right column (30% width)**: `YEARS` (right-aligned)
- Details shown below in merged cells

#### Bullet Cleanup
- Removes existing raw bullet paragraphs before inserting structured tables
- Prevents duplicate content
- Only removes actual bullets/numbered lists, stops at next heading

#### Fallback Handling
- If parser returns empty data, attempts to build structure from raw bullets
- Scans document tables for headings in cells
- Multiple insertion points: placeholders, headings, table cells

### 3. Helper Functions Added

#### Parser Helpers
- `_strip_bullet(s)`: Removes leading bullets (•, -, –, *, etc.)
- `_extract_role_from_dated_line(s)`: Extracts role by removing dates
- `_normalize_text(s)`: Cleans unicode artifacts
- `_strip_location(s)`: Removes "City, State" fragments

#### Formatter Helpers
- `_delete_following_bullets(paragraph)`: Removes bullet paragraphs after heading
- `_collect_bullets_after_heading(paragraph)`: Harvests raw bullets
- `_build_experience_from_bullets(bullets)`: Fallback parser
- `_build_education_from_bullets(bullets)`: Fallback parser
- `_delete_next_table(paragraph)`: Removes old tables before inserting new

## Testing

### Run Complete Workflow Test
```bash
cd Backend
python test_complete_workflow.py
```

This will:
1. Use test data with correct structure (company, role, duration)
2. Format with your Word template
3. Create output: `Backend/output/test_formatted_output.docx`
4. Verify tables were created correctly

### Verify Output
Open `Backend/output/test_formatted_output.docx` and check:
- ✅ Employment History shows: `COMPANY - ROLE` on left, `YEARS` on right
- ✅ Education shows: `DEGREE  INSTITUTION` on left, `YEAR` on right
- ✅ Details appear as bullets below each entry
- ✅ No duplicate raw bullet lists
- ✅ Clean, professional formatting

## Data Structure

The parser now returns this structure:

```python
{
    'name': 'Candidate Name',
    'email': 'email@example.com',
    'phone': '555-1234',
    'experience': [
        {
            'company': 'Infosys',
            'role': 'Senior Developer',
            'duration': '2021-2025',
            'title': 'Senior Developer - Infosys',
            'details': ['Detail 1', 'Detail 2', ...]
        }
    ],
    'education': [
        {
            'degree': 'Master of Science in Data Science',
            'institution': 'PS University',
            'year': '2020-2022',
            'details': ['GPA: 3.8', ...]
        }
    ],
    'skills': ['Python', 'Java', ...]
}
```

## Key Files Modified

1. **`Backend/utils/advanced_resume_parser.py`**
   - `_extract_experience()`: Enhanced date-line + company-line pairing
   - `_extract_education()`: Better degree/institution parsing
   - Added unicode normalization and location stripping

2. **`Backend/utils/word_formatter.py`**
   - `_insert_experience_block()`: Creates clean 2-column table
   - `_insert_education_block()`: Creates clean 2-column table  
   - `_delete_following_bullets()`: Removes old bullets before insertion
   - Added fallback builders for when parser returns empty data

## Next Steps

1. **Test with your actual resume files**:
   - Place resume in `Backend/resumes/`
   - Run the main app or formatter
   - Check output

2. **Adjust if needed**:
   - If company/role detection is wrong, update `_parse_company_role_line()`
   - If dates aren't extracted, check `_contains_date_range()`
   - If location removal is too aggressive, adjust `_strip_location()`

3. **Fine-tune formatting**:
   - Column widths in `_insert_experience_block()` (currently 70/30)
   - Font sizes (currently 11pt for title, 10pt for date)
   - Spacing and alignment

## Debugging

If output is still showing raw bullets:
1. Check parser logs for "Parsed exp" / "Parsed edu" messages
2. Verify data structure has `company`, `role`, `duration` fields (not just `title`)
3. Ensure `_delete_following_bullets()` is being called before table insertion
4. Check if template has nested tables that aren't being detected

If parsing fails:
1. Add more logging to `_extract_experience()` and `_extract_education()`
2. Check if section headers match keywords (Experience, Employment History, etc.)
3. Verify `_contains_date_range()` detects your date formats
4. Test `_normalize_text()` is cleaning unicode properly
