# Skills Table Fix - Implementation Guide

## Current Problem

**What it's doing now:**
```
Skill: "OPGW & ADSS"
Years: "3+"
Last Used: "2025"
```

**What you want:**
```
Skill: "Considerable knowledge of fiber optic systems and hands-on working experience with fiber installation, splicing, and testing equipment"
Years: "3+"
Last Used: "2025"
```

## Root Cause

The current code extracts individual skill KEYWORDS from the resume instead of extracting full SKILL STATEMENTS/DESCRIPTIONS from experience bullets.

**Location**: `Backend/utils/word_formatter.py` around line 900-1100 (skills table filling logic)

## Correct Logic

### 1. Extract Full Skill Statements from Experience

**Current approach** (Wrong):
- Parses skills section
- Extracts keywords: "OPGW", "ADSS", "Fiber Splicing", etc.
- Each keyword becomes a row

**Correct approach**:
- Parse experience bullets (not skills section!)
- Extract full sentences that describe capabilities
- Look for patterns like:
  - "Managed..."
  - "Designed and implemented..."
  - "Considerable knowledge of..."
  - "Experience with..."
- Keep the FULL statement as the skill description

### 2. Group Related Skills

Don't create separate rows for "OPGW", "ADSS", "Fiber Splicing". Instead, combine them:

```
"Considerable knowledge of fiber optic systems and hands-on working experience with fiber installation, splicing, and testing equipment including OPGW, ADSS, Fiber Splicing, OTDR"
```

### 3. Calculate Years Correctly

**Current (Wrong)**: Shows "3+" for everything

**Correct Logic**:
1. For each skill statement, find ALL jobs that mention related technologies
2. Find the EARLIEST start date across all jobs using this skill
3. Find the LATEST end date across all jobs using this skill
4. Calculate total years = (latest_year - earliest_year)
5. If skill is used in multiple non-overlapping jobs, sum the durations
6. Use "8+" format only if explicitly mentioned or if >8 years

**Example**:
```python
def calculate_skill_years(skill_statement, all_jobs):
    related_jobs = []
    
    # Extract technologies from skill statement
    techs = extract_technologies(skill_statement)
    
    # Find all jobs that used these technologies
    for job in all_jobs:
        for detail in job['details']:
            if any(tech.lower() in detail.lower() for tech in techs):
                related_jobs.append(job)
                break
    
    if not related_jobs:
        return "–"
    
    # Find earliest start and latest end
    years = []
    for job in related_jobs:
        start_year = extract_year(job['start_date'])
        end_year = extract_year(job['end_date'])
        if start_year and end_year:
            years.append((start_year, end_year))
    
    if not years:
        return "–"
    
    earliest_start = min(y[0] for y in years)
    latest_end = max(y[1] for y in years)
    
    total_years = latest_end - earliest_start
    
    if total_years >= 8:
        return f"{total_years}+"
    else:
        return str(total_years)
```

### 4. Calculate Last Used Correctly

**Current (Wrong)**: Shows "2025" for everything

**Correct Logic**:
```python
def calculate_last_used(skill_statement, all_jobs):
    # Find most recent job that used this skill
    latest_year = None
    
    techs = extract_technologies(skill_statement)
    
    for job in sorted(all_jobs, key=lambda x: extract_year(x['end_date']), reverse=True):
        for detail in job['details']:
            if any(tech.lower() in detail.lower() for tech in techs):
                latest_year = extract_year(job['end_date'])
                break
        if latest_year:
            break
    
    return latest_year or "–"
```

## Implementation Steps

### Step 1: Modify Skill Extraction

File: `Backend/utils/word_formatter.py`

Find the function that fills the skills table (search for "Filling skills table" or "_fill_skills_table"):

**Replace this**:
```python
# Current code extracts keywords
skills = self.resume_data.get('skills', [])
for skill in skills:
    add_skill_row(skill, "3+", "2025")
```

**With this**:
```python
# Extract full skill statements from experience
experience = self.resume_data.get('experience', [])
skill_statements = extract_skill_statements_from_experience(experience)

for statement in skill_statements:
    description = statement['description']
    years = calculate_years_for_skill(statement, experience)
    last_used = calculate_last_used_for_skill(statement, experience)
    add_skill_row(description, years, last_used)
```

### Step 2: Create Helper Functions

Add these helper functions:

```python
def extract_skill_statements_from_experience(self, experience_entries):
    """Extract full skill statements from experience bullets"""
    statements = []
    
    # Action verb patterns that indicate skill statements
    action_patterns = [
        r'^Managed\s+',
        r'^Designed\s+and\s+implemented\s+',
        r'^Implemented\s+',
        r'^Deployed\s+',
        r'^Oversaw\s+',
        r'^Monitored\s+',
        r'^Performed\s+',
        r'^Installed\s+',
        r'^Configured\s+',
        r'^Maintained\s+',
        r'Considerable knowledge of',
        r'Experience\s+(with|in|designing|implementing)',
        r'In-depth experience'
    ]
    
    for job in experience_entries:
        for detail in job.get('details', []):
            detail_clean = detail.strip()
            
            # Check if this detail matches skill statement patterns
            for pattern in action_patterns:
                if re.search(pattern, detail_clean, re.IGNORECASE):
                    # Extract the statement and technologies
                    statement = extract_full_statement(detail_clean)
                    technologies = extract_technologies(detail_clean)
                    
                    statements.append({
                        'description': statement,
                        'technologies': technologies,
                        'job_start': job.get('start_date'),
                        'job_end': job.get('end_date')
                    })
                    break
    
    # Group similar statements and remove duplicates
    grouped = group_similar_statements(statements)
    
    # Limit to top 8-15 statements
    return grouped[:12]

def extract_full_statement(self, detail_text):
    """Extract the main capability statement from a bullet"""
    # Remove trailing technology lists in parentheses
    statement = re.sub(r'\s*\([^)]+\)\s*$', '', detail_text)
    
    # Keep the full sentence up to the first period or technology list
    statement = statement.split('.')[0]
    
    return statement.strip()

def extract_technologies(self, text):
    """Extract specific technologies/tools mentioned in text"""
    # Common technology patterns
    tech_patterns = [
        r'\b[A-Z][a-z]+(?:/[A-Z][a-z]+)+\b',  # Cisco/Meraki, AWS/Azure
        r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})*\b',     # OTDR, OPGW, ADSS
        r'\b(?:Cisco|Meraki|Azure|AWS|OTDR|Fiber|VPN)\b'  # Specific tools
    ]
    
    technologies = []
    for pattern in tech_patterns:
        matches = re.findall(pattern, text)
        technologies.extend(matches)
    
    return list(set(technologies))

def group_similar_statements(self, statements):
    """Group similar skill statements to avoid duplication"""
    grouped = {}
    
    for stmt in statements:
        # Create a key based on main keywords
        key_words = extract_key_words(stmt['description'])
        key = ' '.join(sorted(key_words[:3]))  # Use first 3 key words as grouping key
        
        if key not in grouped:
            grouped[key] = stmt
        else:
            # Merge technologies
            grouped[key]['technologies'].extend(stmt['technologies'])
            grouped[key]['technologies'] = list(set(grouped[key]['technologies']))
    
    return list(grouped.values())
```

### Step 3: Update Row Addition Logic

When adding rows to the table:

```python
def add_skill_row_to_table(self, table, description, years, last_used):
    """Add a single skill row with proper formatting"""
    row = table.add_row()
    
    # Skill description (full statement)
    skill_cell = row.cells[0]
    skill_cell.text = description
    
    # Years used
    years_cell = row.cells[1]
    years_cell.text = str(years)
    
    # Last used
    last_used_cell = row.cells[2]
    last_used_cell.text = str(last_used)
```

## Testing

### Test Case 1: Full Statement Extraction

**Input**: Experience bullet
```
"Managed fiber installation, termination, and maintenance, ensuring accurate fiber records using OTDR and AutoCAD"
```

**Expected Output**:
```
Skill: "Managed fiber installation, termination, and maintenance, ensuring accurate fiber records"
Technologies: ["OTDR", "AutoCAD", "Fiber"]
```

### Test Case 2: Years Calculation

**Input**: 
- Job 1 (2023-2025): Uses Fiber, OTDR
- Job 2 (2021-2023): Uses Fiber, Network
- Job 3 (2018-2021): Uses Network, Cisco

**For "Fiber" skill**:
- Jobs using Fiber: Job 1, Job 2
- Earliest: 2021, Latest: 2025
- Years: 4

**For "Network" skill**:
- Jobs using Network: Job 2, Job 3
- Earliest: 2018, Latest: 2023
- Years: 5

### Test Case 3: Last Used

**Input**: Same as above

**For "Fiber" skill**:
- Latest job using Fiber: Job 1 (ends 2025)
- Last Used: 2025

**For "Network" skill**:
- Latest job using Network: Job 2 (ends 2023)
- Last Used: 2023

## Quick Fix (Temporary)

If you need a quick improvement NOW without full rewrite:

1. Instead of using skills list, use experience details
2. Take first 10-15 experience bullets as-is
3. Calculate years from job dates
4. Use most recent job's end year

```python
# Quick fix in skills table filling section
experience = self.resume_data.get('experience', [])
skill_rows = []

for job in experience[:3]:  # Top 3 jobs only
    for detail in job.get('details', [])[:5]:  # Top 5 details per job
        skill_rows.append({
            'description': detail,
            'years': calculate_job_years(job),
            'last_used': extract_year(job['end_date'])
        })

# Add to table
for row_data in skill_rows[:10]:  # Limit to 10 rows
    add_row_to_skills_table(row_data)
```

## Summary

✅ Extract FULL statements from experience (not keywords)  
✅ Calculate years from actual job history (not "3+" for everything)  
✅ Use correct last used year (not "2025" for everything)  
✅ Group similar skills to avoid duplication  
✅ Limit to 8-15 high-level skills  

**This is a significant rewrite** (2-3 hours) but necessary for quality output.

Would you like me to implement this fix now?
