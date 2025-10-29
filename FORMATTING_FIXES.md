# Resume Formatting Issues - Fix Plan

## Issues Identified

### 1. ✅ Unwanted gap before SKILLS section
**Problem:** Extra spacing/paragraphs before SKILLS section
**Solution:** 
- Remove empty paragraphs between sections
- Adjust `space_before` and `space_after` for section headings
- Clean up orphaned content more aggressively

### 2. ✅ Education details appearing in CAI CONTACT
**Problem:** Education data bleeding into CAI CONTACT section
**Solution:**
- Strengthen CAI CONTACT boundary detection
- Skip first 5-10 paragraphs when searching for education placeholders
- Add stricter section boundary checks

### 3. ✅ Use existing EDUCATION section in template
**Problem:** Creating duplicate education sections instead of using existing one
**Solution:**
- Check for existing EDUCATION heading first
- Clear and reuse existing section
- Only create new section if not present

### 4. ✅ Add EDUCATION after Employment History if missing
**Problem:** Education not added in correct position
**Solution:**
- Track Employment History tail paragraph
- Insert EDUCATION immediately after Employment
- Maintain proper section order

### 5. ✅ Add missing sections (Skills, Certificates) dynamically
**Problem:** Missing sections from candidate resume not added
**Solution:**
- Check candidate resume for all sections
- Add missing sections in order: Employment → Education → Skills → Certificates
- Use structured insertion logic

### 6. ✅ Follow template alignment rules
**Problem:** Name not centered when template has center alignment
**Solution:**
- Detect paragraph alignment from template
- Preserve alignment when replacing content
- Apply template formatting rules

## Implementation Plan

### Phase 1: Fix CAI CONTACT Boundary (Prevent Education Leakage)
- Increase skip range for early paragraphs (0-10)
- Add explicit CAI CONTACT section detection
- Stop education insertion before CAI CONTACT area

### Phase 2: Fix Section Ordering
- Implement strict section order: SUMMARY → EMPLOYMENT → EDUCATION → SKILLS → CERTIFICATES
- Track section positions
- Insert missing sections in correct order

### Phase 3: Remove Gaps
- Clean empty paragraphs between sections
- Normalize spacing: 12pt before, 6pt after headings
- Remove orphaned bullets more aggressively

### Phase 4: Preserve Template Formatting
- Detect and preserve paragraph alignment
- Maintain font styles from template
- Copy formatting from template headings

### Phase 5: Dynamic Section Addition
- Scan candidate resume for all sections
- Add missing sections after education
- Support: Skills, Certificates, Projects, Languages, etc.
