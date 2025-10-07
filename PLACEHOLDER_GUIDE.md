# 📝 Template Placeholder Guide

## Understanding Your Template

Your template has **instruction placeholders** that need to be replaced with actual candidate data. The system now recognizes and replaces ALL common placeholder formats!

## ✅ Supported Placeholder Formats

### Name Placeholders
```
[NAME]                          → John Doe
[CANDIDATE NAME]                → John Doe
<CANDIDATE NAME>                → John Doe
<Candidate's full name>         → John Doe
<Candidate Name>                → John Doe
<Name>                          → John Doe
Your Name                       → John Doe
Insert name                     → John Doe
```

### Contact Information
```
[EMAIL] or <EMAIL>              → john.doe@email.com
[PHONE] or <PHONE>              → (555) 123-4567
[ADDRESS] or <ADDRESS>          → 123 Main St, City
[LINKEDIN] or <LINKEDIN>        → linkedin.com/in/johndoe
[DOB] or <DOB>                  → 01/15/1990
```

### Section Content Placeholders
```
<List candidate's relevant employment history>
    → Replaced with actual work experience

<List candidate's education background>
    → Replaced with actual education details

<List skills>
    → Replaced with actual skills list

<Professional Summary>
    → Replaced with actual summary
```

## 📋 Your Template Example

### Before (Template):
```
CAI Contact
Insert name and contact information for the CAI Contract Manager

Tim Brodrick
Phone: 678-427-3660
Email: Timothy.Brodrick@cai.io

<Candidate's full name>

Employment History
<List candidate's relevant employment history>

Education
<List candidate's education background>
```

### After (Formatted):
```
CAI Contact
Insert name and contact information for the CAI Contract Manager

Tim Brodrick
Phone: 678-427-3660
Email: Timothy.Brodrick@cai.io

John Doe

Employment History
• Senior Software Engineer at Tech Corp (2020-2023)
  - Led development of cloud-based applications
  - Managed team of 5 developers
• Software Developer at StartupXYZ (2018-2020)
  - Developed mobile applications
  - Implemented CI/CD pipelines

Education
• Master of Science in Computer Science
  University of Technology, 2018
• Bachelor of Science in Software Engineering
  State University, 2016
```

## 🎯 How It Works

### Step 1: Template Analysis
```
System scans template and finds:
✓ <Candidate's full name>
✓ <List candidate's relevant employment history>
✓ <List candidate's education background>
```

### Step 2: Resume Parsing
```
System extracts from candidate resume:
✓ Name: John Doe
✓ Experience: 2 jobs with details
✓ Education: 2 degrees
✓ Skills: 15 technical skills
```

### Step 3: Intelligent Replacement
```
System replaces:
<Candidate's full name> → John Doe
<List candidate's relevant employment history> → Actual work history
<List candidate's education background> → Actual education
```

## 📊 All Recognized Patterns

### Angle Bracket Format `<...>`
```
<Candidate's full name>
<Candidate Name>
<Name>
<EMAIL>
<PHONE>
<ADDRESS>
<LINKEDIN>
<DOB>
<List candidate's relevant employment history>
<List employment history>
<Employment History>
<Work Experience>
<List candidate's education background>
<List education background>
<Education Background>
<List skills>
<Skills>
<Professional Summary>
```

### Square Bracket Format `[...]`
```
[NAME]
[CANDIDATE NAME]
[EMAIL]
[PHONE]
[ADDRESS]
[LINKEDIN]
[DOB]
```

### Plain Text Instructions
```
Insert name
Your Name
List relevant employment history
List education background
Professional summary
```

## 🔧 Template Best Practices

### ✅ DO Use These Formats:
```
1. <Candidate's full name>
2. <List candidate's relevant employment history>
3. <List candidate's education background>
4. [NAME], [EMAIL], [PHONE]
```

### ❌ AVOID These:
```
1. Vague instructions without brackets
2. Non-standard placeholder formats
3. Mixed formats in same field
```

## 💡 Tips for Your Templates

### 1. Keep CAI Contact Information
```
✓ System will NOT replace this section
✓ It stays exactly as-is in the template
✓ Only candidate placeholders are replaced
```

### 2. Use Clear Section Headings
```
Employment History  ← System recognizes this
Education          ← System recognizes this
Skills             ← System recognizes this
```

### 3. Use Consistent Placeholders
```
✓ <Candidate's full name>
✓ <List candidate's relevant employment history>
✓ <List candidate's education background>
```

## 🚀 Testing Your Template

### 1. Upload Template
```
- Upload your Word template with placeholders
- System analyzes and detects all placeholders
- Check console output for detected fields
```

### 2. Format Test Resume
```
- Upload a sample candidate resume
- System extracts all information
- Replaces all placeholders
- Downloads formatted result
```

### 3. Verify Output
```
✓ Candidate name replaced
✓ Contact info replaced
✓ Employment history filled in
✓ Education filled in
✓ CAI contact info preserved
✓ All formatting maintained
```

## 📝 Example Output

### Your Template Structure:
```
┌─────────────────────────────────────────┐
│  CAI Contact Information                │  ← Preserved
│  (Tim Brodrick details)                 │  ← Preserved
│                                         │
│  <Candidate's full name>                │  ← Replaced
│                                         │
│  Employment History                     │  ← Heading preserved
│  <List candidate's relevant...>         │  ← Replaced with actual data
│                                         │
│  Education                              │  ← Heading preserved
│  <List candidate's education...>        │  ← Replaced with actual data
└─────────────────────────────────────────┘
```

### After Formatting:
```
┌─────────────────────────────────────────┐
│  CAI Contact Information                │  ← Preserved
│  Tim Brodrick                           │  ← Preserved
│  Phone: 678-427-3660                    │  ← Preserved
│  Email: Timothy.Brodrick@cai.io         │  ← Preserved
│                                         │
│  John Doe                               │  ← ✅ Replaced!
│                                         │
│  Employment History                     │  ← Preserved
│  • Senior Software Engineer...          │  ← ✅ Actual data!
│  • Software Developer...                │  ← ✅ Actual data!
│                                         │
│  Education                              │  ← Preserved
│  • Master of Science...                 │  ← ✅ Actual data!
│  • Bachelor of Science...               │  ← ✅ Actual data!
└─────────────────────────────────────────┘
```

## ✅ Ready to Use!

The system now understands your template format and will:
1. ✅ Keep CAI contact information unchanged
2. ✅ Replace `<Candidate's full name>` with actual name
3. ✅ Replace `<List candidate's relevant employment history>` with actual experience
4. ✅ Replace `<List candidate's education background>` with actual education
5. ✅ Preserve all formatting and structure

**Upload your template and test it now! 🎉**
