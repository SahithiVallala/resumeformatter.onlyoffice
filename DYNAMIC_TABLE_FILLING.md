# Dynamic Table Filling System ✨

## Overview

The system now **AUTOMATICALLY detects and fills ANY table structure** in your templates - no hardcoding required!

---

## How It Works

### Step 1: Detect Table Type

The system analyzes table headers to determine what kind of data table it is:

```python
# Reads first few rows to find headers
header_text = "skill years used last used"

# Counts indicator keywords
skills_score = 3     # Found: skill, years, used
experience_score = 0
education_score = 0

# Result: This is a SKILLS table!
```

**Supported Table Types**:
- **Skills** - Technical skills, competencies, proficiencies
- **Experience** - Employment history, work history
- **Education** - Academic qualifications

---

### Step 2: Read Column Headers Dynamically

```python
# Example: Skills table
headers = ['SKILL', 'YEARS USED', 'LAST USED']

# System reads these at runtime - NO hardcoding!
```

---

### Step 3: Intelligent Column Mapping

The system **semantically understands** what each column means:

#### Skills Table Example

**Template columns**: `['Technical Competency', 'Years of Exp', 'Currently Using']`

**System maps**:
```
Column 0 ('Technical Competency') → skill
   (contains "competency" keyword)

Column 1 ('Years of Exp') → years  
   (contains "years" and "exp" keywords)

Column 2 ('Currently Using') → last_used
   (contains "current" keyword)
```

#### Experience Table Example

**Template columns**: `['Company Name', 'Position', 'Dates', 'Location']`

**System maps**:
```
Column 0 ('Company Name') → company
   (contains "company" keyword)

Column 1 ('Position') → role
   (contains "position" keyword)

Column 2 ('Dates') → duration
   (contains "date" keyword)

Column 3 ('Location') → location
   (contains "location" keyword)
```

#### Education Table Example

**Template columns**: `['Degree/Certificate', 'Institution', 'Year of Graduation']`

**System maps**:
```
Column 0 ('Degree/Certificate') → degree
   (contains "degree" keyword)

Column 1 ('Institution') → institution
   (contains "institution" keyword)

Column 2 ('Year of Graduation') → year
   (contains "year" and "graduation" keywords)
```

---

### Step 4: Fill Table Dynamically

```python
# Clear old rows (keep header)
# For each resume item:
#   Create new row
#   Fill each column with mapped data
```

---

## Keyword Patterns Recognized

### Skills Table Columns

| Data Field | Recognized Keywords |
|------------|---------------------|
| **skill** | skill, technology, competency, expertise, tool, name |
| **years** | year, experience, exp, yrs, duration, used |
| **last_used** | last, recent, current, latest, when |

### Experience Table Columns

| Data Field | Recognized Keywords |
|------------|---------------------|
| **company** | company, employer, organization, firm |
| **role** | role, position, title, job |
| **duration** | date, year, period, duration, from, to, when |
| **location** | location, city, state, place |
| **responsibilities** | responsibilit, duties, description, summary |

### Education Table Columns

| Data Field | Recognized Keywords |
|------------|---------------------|
| **degree** | degree, qualification, certificate, program |
| **institution** | institution, university, college, school |
| **year** | year, date, graduation, completion |
| **field** | field, major, specialization, subject |
| **gpa** | gpa, grade, marks, score |

---

## Example Console Output

```
🔍 Scanning 3 tables...

  📋 Table 0: 8 rows x 3 cols
     Headers: ['SKILL', 'YEARS USED', 'LAST USED']
  ✅ Detected as SKILLS TABLE
     🔍 Analyzing table structure...
     📋 Column headers: ['skill', 'years used', 'last used']
     🗺️  Column mapping: {0: 'skill', 1: 'years', 2: 'last_used'}
        Column 0 ('skill') → skill
        Column 1 ('years used') → years
        Column 2 ('last used') → last_used
     📊 Found 8 skills items to fill
     🔄 Adding 8 rows...
        ✓ Row 1: ['Python', '2+ years', 'Recent']
        ✓ Row 2: ['JavaScript', '2+ years', 'Recent']
        ✓ Row 3: ['SQL', '2+ years', 'Recent']
  ✅ Filled 8 rows

  📋 Table 1: 5 rows x 4 cols
     Headers: ['Company', 'Role', 'Dates', 'Location']
  ✅ Detected as EXPERIENCE/EMPLOYMENT TABLE
     🔍 Analyzing table structure...
     📋 Column headers: ['company', 'role', 'dates', 'location']
     🗺️  Column mapping: {0: 'company', 1: 'role', 2: 'duration', 3: 'location'}
        Column 0 ('company') → company
        Column 1 ('role') → role
        Column 2 ('dates') → duration
        Column 3 ('location') → location
     📊 Found 3 experience items to fill
     🔄 Adding 3 rows...
        ✓ Row 1: ['Infosys', 'Senior Developer', '2021-2025']
        ✓ Row 2: ['Tech Solutions', 'Software Engineer', '2018-2021']
  ✅ Filled 3 rows

  📋 Table 2: 3 rows x 3 cols
     Headers: ['Degree', 'University', 'Year']
  ✅ Detected as EDUCATION TABLE
     🔍 Analyzing table structure...
     📋 Column headers: ['degree', 'university', 'year']
     🗺️  Column mapping: {0: 'degree', 1: 'institution', 2: 'year'}
        Column 0 ('degree') → degree
        Column 1 ('university') → institution
        Column 2 ('year') → year
     📊 Found 2 education items to fill
     🔄 Adding 2 rows...
        ✓ Row 1: ['Master of Science', 'PS University', '2020-2022']
        ✓ Row 2: ['Bachelor of Technology', 'State University', '2014-2018']
  ✅ Filled 2 rows
```

---

## Works with ANY Template!

### Example 1: Different Skills Column Names

**Template A**: `SKILL | YEARS USED | LAST USED`  
**Template B**: `Technical Competency | Years of Experience | Currently Using`  
**Template C**: `Tool/Technology | Exp (Yrs) | Most Recent Use`

✅ **All three work!** System recognizes variations automatically.

---

### Example 2: Different Experience Column Names

**Template A**: `Company | Position | Dates`  
**Template B**: `Employer Name | Job Title | Employment Period`  
**Template C**: `Organization | Role | Duration | Location`

✅ **All work!** Dynamic mapping handles any structure.

---

### Example 3: Partial Column Matches

**Template**: `Skill Name | When Last Used`  
(Missing "Years" column)

**System maps**:
- Column 0 → skill ✅
- Column 1 → last_used ✅
- (No years column - skipped)

**Result**: Fills skill names and last used dates, leaves years column empty if it exists elsewhere

---

## Benefits

✅ **No hardcoding** - Works with any template structure  
✅ **Intelligent mapping** - Understands column meaning semantically  
✅ **Flexible keywords** - Recognizes many variations  
✅ **Handles missing columns** - Gracefully skips unmapped columns  
✅ **Clear debugging** - Shows exactly what's mapped and filled  
✅ **Multiple table types** - Skills, Experience, Education  

---

## Adding New Column Types

Want to add support for new column types? Just add keywords:

```python
# In _map_columns_to_fields(), add to patterns:

patterns = {
    'new_field': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing fields
}
```

Then provide data in standardized format:

```python
# In _get_XXX_data(), add field to returned dict:
{
    'new_field': 'value',
    # ... existing fields
}
```

---

## Test It Now!

Upload **ANY template** with tables for:
- Skills
- Employment history
- Education

The system will:
1. ✅ Detect table type automatically
2. ✅ Read column headers dynamically
3. ✅ Map columns intelligently
4. ✅ Fill with candidate data
5. ✅ Show detailed console output

**Watch the console to see the intelligent mapping in action!** 🎯✨
