# Resume Formatter - Template Preservation Guide

## Overview
The Resume Formatter now **preserves exact template formatting** including:
- ✅ Letterheads and logos
- ✅ Headers and footers
- ✅ Background images and watermarks
- ✅ Exact fonts, colors, and styling
- ✅ Page layout and margins
- ✅ All visual elements (borders, lines, shapes)

## How It Works

### PDF Templates
For PDF templates, the system:
1. **Clones the template** - Keeps all visual elements intact
2. **Creates an overlay** - Adds resume content on top
3. **Merges layers** - Combines template background with new content
4. **Preserves everything** - Letterheads, logos, and styling remain unchanged

### Word Templates (.docx)
For Word templates, the system:
1. **Opens the template** - Loads the .docx file
2. **Finds placeholders** - Looks for [NAME], [Email], etc.
3. **Replaces content** - Fills in actual resume data
4. **Maintains formatting** - Keeps all fonts, colors, and layout

## Template Requirements

### PDF Templates
- Should have clear section headings (Experience, Education, Skills, etc.)
- Can include any visual elements (logos, letterheads, borders)
- All graphics and formatting will be preserved

### Word Templates
- Use placeholders like:
  - `[NAME]` or `Your Name` for the candidate's name
  - `[Email]` or `your.email@example.com` for email
  - `[Phone]` or `(123) 456-7890` for phone number
  - `[LinkedIn]` for LinkedIn profile
- Include section headings: EXPERIENCE, EDUCATION, SKILLS, etc.
- All formatting (fonts, colors, tables, images) will be preserved

## Usage

1. **Upload Template**
   - Go to the web interface
   - Click "Upload Template"
   - Select your PDF or Word template
   - The system will analyze and store it

2. **Format Resumes**
   - Select your template
   - Upload one or more resumes (PDF or Word)
   - Click "Format Resumes"
   - Download the formatted results

## Technical Details

### PDF Processing
- Uses `PyPDF2` for PDF manipulation
- Uses `reportlab` for content overlay
- Merges template background with resume content
- Preserves all embedded images and graphics

### Word Processing
- Uses `python-docx` for Word manipulation
- Finds and replaces placeholders
- Maintains all formatting properties
- Preserves tables, images, and styles

## Supported Formats

### Input (Templates)
- PDF (.pdf)
- Word (.docx, .doc)

### Input (Resumes)
- PDF (.pdf)
- Word (.docx, .doc)

### Output
- PDF (.pdf) - for PDF templates
- Word (.docx) - for Word templates

## Best Practices

1. **Template Design**
   - Use clear section headings
   - Leave adequate space for content
   - Test with sample resumes first

2. **Resume Content**
   - Ensure resumes have clear sections
   - Use standard section names (Experience, Education, Skills)
   - Keep content concise and well-formatted

3. **Quality Control**
   - Always preview formatted resumes
   - Check that all content is visible
   - Verify letterheads and logos are intact

## Troubleshooting

### Issue: Content overlaps with letterhead
**Solution**: The system automatically leaves space at the top. If overlap occurs, adjust the template's top margin.

### Issue: Text is cut off
**Solution**: The system wraps long lines. Ensure your template has adequate width for content.

### Issue: Sections not matching
**Solution**: Use standard section names in both template and resume (Experience, Education, Skills, etc.)

## Example Templates

### PDF Template Structure
```
[Letterhead/Logo at top]
[Company branding]

NAME
Contact Info

EXPERIENCE
[Content will be inserted here]

EDUCATION
[Content will be inserted here]

SKILLS
[Content will be inserted here]
```

### Word Template Structure
```
[Header with logo]

[NAME]
[Email] | [Phone] | [LinkedIn]

WORK EXPERIENCE
• [Experience items will be inserted]

EDUCATION
• [Education items will be inserted]

SKILLS
• [Skills will be inserted]

[Footer with company info]
```

## API Endpoints

### Upload Template
```
POST /api/templates
Body: multipart/form-data
  - template_file: File
  - template_name: String
```

### Format Resumes
```
POST /api/format
Body: multipart/form-data
  - template_id: String
  - resume_files: File[]
```

### Download Formatted Resume
```
GET /api/download/<filename>
```

## Future Enhancements

- [ ] Support for multi-page templates
- [ ] Advanced placeholder syntax
- [ ] Batch processing optimization
- [ ] Template preview before formatting
- [ ] Custom section mapping
