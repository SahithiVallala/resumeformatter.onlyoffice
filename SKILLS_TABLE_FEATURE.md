# 📊 Skills Table Auto-Fill Feature

## Overview

The Resume Formatter now **automatically detects and fills skills tables** in Word templates! If your template contains a table with columns like "Skill", "Years Used", and "Last Used", the system will:

1. ✅ Detect the skills table automatically
2. ✅ Extract skills from the candidate's resume
3. ✅ Calculate years of experience for each skill
4. ✅ Determine when each skill was last used
5. ✅ Fill the table rows dynamically

## 🎯 How It Works

### Template Requirements

Your template should have a table with headers like:

```
| Skill | Years Used | Last Used |
|-------|------------|-----------|
|       |            |           |
|       |            |           |
```

**Supported Column Names:**
- **Skill Column**: "Skill", "Skills", "Technology", "Competency"
- **Years Column**: "Years", "Experience", "Years Used", "Years of Experience"
- **Last Used Column**: "Last Used", "Last", "Recent", "Most Recent"

### What Gets Filled

For each skill found in the candidate's resume:

**Skill Name**: Python, JavaScript, React, AWS, etc.
**Years Used**: Calculated from work experience dates (e.g., "3+ years")
**Last Used**: Most recent year used or "Present" if currently using

## 📝 Example

### Your Template Table

```
Skills
Please use this table to list the skills noted in the Required/Desired section 
of the VectorVMS requirement. In addition, please respond with the years of 
experience for each skill and the last time each skill was used.

| Skill      | Years Used | Last Used |
|------------|------------|-----------|
|            |            |           |
|            |            |           |
|            |            |           |
```

### After Formatting

```
| Skill          | Years Used | Last Used |
|----------------|------------|-----------|
| Python         | 5+ years   | Present   |
| JavaScript     | 4+ years   | Present   |
| React          | 3+ years   | 2024      |
| AWS            | 3+ years   | Present   |
| Docker         | 2+ years   | 2024      |
| Node.js        | 4+ years   | Present   |
| PostgreSQL     | 3+ years   | 2023      |
| Git            | 5+ years   | Present   |
| REST APIs      | 4+ years   | Present   |
| Kubernetes     | 2+ years   | 2024      |
```

## 🔍 How Skills Are Extracted

### 1. Skills Detection
The system extracts skills from the resume's:
- Skills section
- Technical skills section
- Experience descriptions
- Project descriptions

### 2. Years Calculation
For each skill, the system:
- Searches through work experience
- Finds where the skill was mentioned
- Extracts date ranges (e.g., "2020-2023")
- Calculates total years of experience

### 3. Last Used Detection
The system determines:
- If skill is in current/recent job → "Present"
- If skill is in past job → Year (e.g., "2023")
- If no dates found → "Recent"

## 🎨 Features

### Automatic Detection
- ✅ No configuration needed
- ✅ Works with any table that has skill-related headers
- ✅ Detects variations in column names

### Smart Filling
- ✅ Removes empty template rows
- ✅ Adds exactly the right number of rows
- ✅ Limits to 15 skills (prevents overly long tables)
- ✅ Preserves table formatting and styling

### Intelligent Parsing
- ✅ Matches skills to experience dates
- ✅ Handles "Present", "Current", ongoing roles
- ✅ Calculates years from date ranges
- ✅ Provides sensible defaults when data is missing

## 📊 Console Output

When processing, you'll see:

```
🔍 Scanning 2 tables...
  📊 Found skills table at index 1
  ✅ Filled 10 skill rows
✓ Replaced 10 placeholders in tables
```

## 🛠️ Technical Details

### Table Detection Logic

The system identifies a skills table if:
1. Table has at least 2 rows (header + data)
2. Header contains "skill" or similar keyword
3. Header contains "years" or "last used" keyword

### Column Mapping

```python
# System automatically maps columns:
skill_col = header with "skill"/"technology"
years_col = header with "years"/"experience"
last_used_col = header with "last"/"recent"
```

### Data Extraction

```python
# For each skill:
1. Find skill in resume
2. Search experience for skill mentions
3. Extract date ranges (2020-2023, 2022-Present)
4. Calculate: end_year - start_year
5. Format: "3+ years"
6. Determine last used: year or "Present"
```

## 💡 Tips for Best Results

### 1. Resume Format
Ensure candidate resumes have:
- ✅ Clear skills section
- ✅ Work experience with dates
- ✅ Skills mentioned in job descriptions

### 2. Template Design
For best results:
- ✅ Use clear column headers ("Skill", "Years Used", "Last Used")
- ✅ Include at least 2-3 empty rows in template
- ✅ Place table after any instructions

### 3. Date Formats
The system recognizes:
- ✅ "2020-2023"
- ✅ "Jan 2020 - Dec 2023"
- ✅ "2022-Present"
- ✅ "2021-Current"

## 🎯 Use Cases

### 1. VectorVMS Requirements
Perfect for templates requiring:
- Skills matrix
- Technology proficiency tables
- Experience breakdown by skill

### 2. Client Submissions
Ideal for:
- Vendor management systems
- Client-specific formats
- Compliance requirements

### 3. Standardized Formats
Great for:
- Company standard templates
- Recruiter submissions
- Proposal responses

## 🔄 Workflow

```
1. Upload template with skills table
   ↓
2. Upload candidate resume(s)
   ↓
3. System detects skills table
   ↓
4. Extracts skills from resume
   ↓
5. Calculates years & last used
   ↓
6. Fills table rows automatically
   ↓
7. Download formatted resume
```

## ✨ Benefits

- **Time Saving**: No manual table filling
- **Accuracy**: Calculated from actual experience
- **Consistency**: Same format for all candidates
- **Scalability**: Works for bulk formatting
- **Flexibility**: Adapts to different table structures

## 🚀 Example Templates

### Template 1: Basic Skills Table
```
| Skill | Years | Last Used |
```

### Template 2: Detailed Skills Table
```
| Technology | Years of Experience | Most Recent Use |
```

### Template 3: Competency Matrix
```
| Competency | Experience Level | Last Applied |
```

All variations are automatically detected and filled!

## 📝 Notes

- Maximum 15 skills per table (prevents overly long tables)
- Empty rows in template are removed
- Table formatting (borders, colors) is preserved
- Works only with Word (.docx) templates
- Skills without dates get default values ("1+ years", "Recent")

## 🎉 Result

Your skills tables are now **automatically populated** with accurate, calculated data from candidate resumes!

**No more manual data entry for skills tables!** 🚀
