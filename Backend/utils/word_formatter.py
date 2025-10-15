"""
Enhanced Word Document Formatter
Handles both .doc and .docx templates
Preserves all formatting, images, headers, footers
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
import os
import re
import shutil
import traceback
import json

# Try to import win32com for .doc support
try:
    import win32com.client
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("⚠️  win32com not available - .doc files will have limited support")

class WordFormatter:
    """Enhanced Word document formatting"""
    
    def __init__(self, resume_data, template_analysis, output_path):
        self.resume_data = resume_data
        self.template_analysis = template_analysis
        self.output_path = output_path
        self.template_path = template_analysis.get('template_path')
        self.template_type = template_analysis.get('template_type')
        
    def format(self):
        """Main formatting method"""
        print(f"\n{'='*70}")
        print(f"📝 WORD DOCUMENT FORMATTING")
        print(f"{'='*70}\n")
        
        print(f"📄 Template: {os.path.basename(self.template_path)}")
        print(f"👤 Candidate: {self.resume_data['name']}")
        print(f"📁 Output: {os.path.basename(self.output_path)}\n")
        
        try:
            # Handle .doc files
            if self.template_path.lower().endswith('.doc'):
                return self._format_doc_file()
            else:
                return self._format_docx_file()
                
        except Exception as e:
            print(f"❌ Error formatting Word document: {e}")
            traceback.print_exc()
            return False
    
    def _format_doc_file(self):
        """Handle .doc files (old Word format)"""
        print("📋 Processing .doc file (old Word format)...")
        
        if HAS_WIN32:
            # Convert .doc to .docx first
            print("✓ Converting .doc to .docx...")
            docx_path = self._convert_doc_to_docx(self.template_path)
            
            if docx_path:
                # Update template path temporarily
                original_path = self.template_path
                self.template_path = docx_path
                
                # Format the docx
                result = self._format_docx_file()
                
                # Cleanup
                try:
                    os.remove(docx_path)
                except:
                    pass
                
                self.template_path = original_path
                return result
            else:
                print("❌ Failed to convert .doc to .docx")
                return False
        else:
            print("⚠️  Cannot process .doc files without win32com")
            print("💡 Please convert template to .docx format or install pywin32")
            return False
    
    def _convert_doc_to_docx(self, doc_path):
        """Convert .doc to .docx using Word COM"""
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            
            # Open .doc file
            doc = word.Documents.Open(os.path.abspath(doc_path))
            
            # Save as .docx
            docx_path = doc_path.replace('.doc', '_temp.docx')
            doc.SaveAs2(os.path.abspath(docx_path), FileFormat=16)  # 16 = docx format
            
            doc.Close()
            word.Quit()
            
            print(f"✓ Converted to: {docx_path}")
            return docx_path
            
        except Exception as e:
            print(f"❌ Conversion error: {e}")
            return None
    
    def _format_docx_file(self):
        """Format .docx file"""
        print("📋 Processing .docx file...")
        
        # Open template
        doc = Document(self.template_path)
        
        print(f"✓ Template loaded: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables")
        
        # Ensure CAI CONTACT section is inserted with persistent data
        try:
            self._ensure_cai_contact(doc)
        except Exception as e:
            print(f"⚠️  CAI Contact insertion error: {e}")
        
        # Show what data we have from resume
        print(f"\n📊 Resume Data Available:")
        print(f"  • Name: {self.resume_data.get('name', 'NOT FOUND')}")
        print(f"  • Email: {self.resume_data.get('email', 'NOT FOUND')}")
        print(f"  • Phone: {self.resume_data.get('phone', 'NOT FOUND')}")
        print(f"  • Experience entries: {len(self.resume_data.get('experience', []))}")
        print(f"  • Education entries: {len(self.resume_data.get('education', []))}")
        print(f"  • Skills: {len(self.resume_data.get('skills', []))}")
        print(f"  • Sections: {list(self.resume_data.get('sections', {}).keys())}")
        
        # Create comprehensive replacement map
        replacements = self._create_replacement_map()
        print(f"\n📝 Created {len(replacements)} replacement mappings")
        
        # Replace in all paragraphs
        replaced_count = 0
        print(f"\n🔍 Scanning {len(doc.paragraphs)} paragraphs for placeholders...")
        
        for para_idx, paragraph in enumerate(doc.paragraphs):
            if not paragraph.text.strip():
                continue
                
            # Check each replacement
            for key, value in replacements.items():
                if self._text_contains(paragraph.text, key):
                    print(f"  📍 Found '{key}' in paragraph {para_idx}: '{paragraph.text[:50]}...'")
                    count = self._replace_in_paragraph(paragraph, key, value)
                    if count > 0:
                        print(f"  ✅ Replaced with: '{value[:50]}...'")
                    else:
                        print(f"  ⚠️  Found but couldn't replace (might be in multiple runs)")

            # Regex-driven fallback for angle bracket placeholders with variations
            # Candidate name generic patterns - very flexible to catch all variations
            name_patterns = [
                r"<\s*Candidate[’']?s\s+full\s+name\s*>",
                r"<\s*Candidate\s*Name\s*>",
                r"<\s*Name\s*>",
                r"<\s*[Pp]lease\s+[Ii]nsert\s+[Cc]andidate[’']?s?\s+[Nn]ame\s+[Hh]ere\s*>",
                r"<\s*[Ii]nsert\s+[Cc]andidate[’']?s?\s+[Nn]ame\s+[Hh]ere\s*>",
                r"<\s*[Ii]nsert\s+[Cc]andidate\s+[Nn]ame\s*>",
                r"<\s*[Pp]lease\s+[Ii]nsert\s+[Nn]ame\s*>",
                r"<\s*[Cc]andidate\s+[Nn]ame\s+[Hh]ere\s*>",
            ]
            for pat in name_patterns:
                if re.search(pat, paragraph.text, re.IGNORECASE):
                    before = paragraph.text
                    self._regex_replace_paragraph(paragraph, pat, self.resume_data.get('name', '').strip() or 'Candidate Name')
                    if paragraph.text != before:
                        print(f"  ✅ Regex replaced candidate name in paragraph {para_idx}")
                        replaced_count += 1

            # Generic catch-all: any <...> containing both 'candidate' and 'name' (any order)
            generic_name_pat = r"<[^>]*?(candidate[^>]*name|name[^>]*candidate)[^>]*?>"
            if re.search(generic_name_pat, paragraph.text, re.IGNORECASE):
                before = paragraph.text
                self._regex_replace_paragraph(paragraph, generic_name_pat, self.resume_data.get('name', '').strip() or 'Candidate Name')
                if paragraph.text != before:
                    print(f"  ✅ Generic regex replaced candidate name in paragraph {para_idx}")
                    replaced_count += 1

            # Employment placeholder generic patterns (very flexible)
            emp_patterns = [
                r"<[^>]*employment[^>]*history[^>]*>",
                r"<[^>]*work[^>]*history[^>]*>",
                r"<[^>]*professional[^>]*experience[^>]*>",
                r"<[^>]*career[^>]*(history|experience)[^>]*>",
                r"<[^>]*history[^>]*(employ|employer|work|career)[^>]*>",
                r"<[^>]*list[^>]*employment[^>]*history[^>]*>",
            ]
            for emp_pat in emp_patterns:
                if re.search(emp_pat, paragraph.text, re.IGNORECASE):
                    content = self._find_matching_resume_section('experience', self.resume_data.get('sections', {}))
                    if content:
                        bullets = []
                        for item in content[:10]:
                            if item.strip():
                                bullets.append('• ' + item.strip().lstrip('•').strip())
                        self._regex_replace_paragraph(paragraph, emp_pat, '\n'.join(bullets))
                        print(f"  ✅ Regex replaced experience placeholder in paragraph {para_idx}")
                        replaced_count += 1
                        break

            # Education placeholder generic pattern
            edu_pat = r"<[^>]*education[^>]*background[^>]*>"
            if re.search(edu_pat, paragraph.text, re.IGNORECASE):
                content = self._find_matching_resume_section('education', self.resume_data.get('sections', {}))
                if content:
                    bullets = []
                    for item in content[:10]:
                        if item.strip():
                            bullets.append('• ' + item.strip().lstrip('•').strip())
                    self._regex_replace_paragraph(paragraph, edu_pat, '\n'.join(bullets))
                    print(f"  ✅ Regex replaced education placeholder in paragraph {para_idx}")
        
        print(f"\n✓ Replaced {replaced_count} placeholders in paragraphs")
        
        # Replace in tables and detect skills tables
        table_replaced = 0
        print(f"\n🔍 Scanning {len(doc.tables)} tables...")
        
        for table_idx, table in enumerate(doc.tables):
            # Check if this is a skills table
            if self._is_skills_table(table):
                print(f"  📊 Found skills table at index {table_idx}")
                skills_filled = self._fill_skills_table(table)
                print(f"  ✅ Filled {skills_filled} skill rows")
                table_replaced += skills_filled
            else:
                # Regular placeholder replacement in non-skills tables
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for key, value in replacements.items():
                                if self._text_contains(paragraph.text, key):
                                    table_replaced += self._replace_in_paragraph(paragraph, key, value)
        
        print(f"✓ Replaced {table_replaced} placeholders in tables")
        
        # Replace in headers/footers
        header_footer_replaced = 0
        for section in doc.sections:
            # Header
            for paragraph in section.header.paragraphs:
                for key, value in replacements.items():
                    if self._text_contains(paragraph.text, key):
                        header_footer_replaced += self._replace_in_paragraph(paragraph, key, value)
            
            # Footer
            for paragraph in section.footer.paragraphs:
                for key, value in replacements.items():
                    if self._text_contains(paragraph.text, key):
                        header_footer_replaced += self._replace_in_paragraph(paragraph, key, value)
        
        if header_footer_replaced > 0:
            print(f"✓ Replaced {header_footer_replaced} placeholders in headers/footers")
        
        # Add sections content
        sections_added = self._add_sections_content(doc)
        print(f"✓ Added {sections_added} sections")
        
        # Save output
        output_docx = self.output_path.replace('.pdf', '.docx')
        doc.save(output_docx)
        
        print(f"\n✅ Successfully created formatted document!")
        print(f"📁 Saved to: {output_docx}\n")
        
        # Optionally convert to PDF
        if self.output_path.endswith('.pdf'):
            print("📄 Converting to PDF...")
            if self._convert_to_pdf(output_docx, self.output_path):
                print(f"✓ PDF created: {self.output_path}")
                # Keep both docx and pdf
            else:
                print("⚠️  PDF conversion failed, keeping .docx file")
        
        return True

    # Helper: insert a new paragraph directly after a given paragraph
    def _insert_paragraph_after(self, paragraph, text):
        try:
            new_p = OxmlElement('w:p')
            paragraph._p.addnext(new_p)
            new_para = Paragraph(new_p, paragraph._parent)
            new_para.add_run(text)
            return new_para
        except Exception:
            # Fallback: append to document if direct insert fails
            return paragraph._parent.add_paragraph(text)
    
    def _add_right_tab(self, paragraph, pos_twips=9360):
        """Add a right-aligned tab stop to a paragraph at the given twips position (1 inch = 1440 twips)."""
        try:
            pPr = paragraph._p.get_or_add_pPr()
            tabs = pPr.find(qn('w:tabs'))
            if tabs is None:
                tabs = OxmlElement('w:tabs')
                pPr.append(tabs)
            tab = OxmlElement('w:tab')
            tab.set(qn('w:val'), 'right')
            tab.set(qn('w:pos'), str(pos_twips))
            tabs.append(tab)
        except Exception:
            # If this fails, the text will still render; right text just won't align via tab stop
            pass

    # ===== CAI CONTACT PERSISTENCE AND INSERTION =====
    def _cai_store_path(self):
        """Return a stable file path to store CAI contact details."""
        home = os.path.expanduser("~")
        return os.path.join(home, ".resume_formatter_cai_contact.json")

    def _load_cai_contact(self, proposed=None, edit=False):
        """Load CAI contact from disk. If edit=True and proposed provided, overwrite and save.
        Structure: {"name": str, "phone": str, "email": str}
        """
        path = self._cai_store_path()
        stored = {}
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    stored = json.load(f) or {}
        except Exception:
            stored = {}

        if edit and isinstance(proposed, dict) and any(proposed.get(k) for k in ("name", "phone", "email")):
            data = {
                "name": (proposed.get("name") or stored.get("name") or ""),
                "phone": (proposed.get("phone") or stored.get("phone") or ""),
                "email": (proposed.get("email") or stored.get("email") or ""),
            }
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
            return data

        # No edit: fall back to stored, else proposed, else empty
        if stored:
            return stored
        if isinstance(proposed, dict):
            return {
                "name": proposed.get("name", ""),
                "phone": proposed.get("phone", ""),
                "email": proposed.get("email", ""),
            }
        return {"name": "", "phone": "", "email": ""}

    def _ensure_cai_contact(self, doc):
        """Ensure the CAI CONTACT section exists and is filled from persistent storage.
        Will not change stored values unless an explicit edit flag is provided via
        resume_data['edit_cai_contact'] or template_analysis['edit_cai_contact'].
        """
        edit_flag = bool(self.resume_data.get('edit_cai_contact') or (self.template_analysis or {}).get('edit_cai_contact'))
        proposed = self.resume_data.get('cai_contact', {})
        cai = self._load_cai_contact(proposed=proposed, edit=edit_flag)

        # Find existing CAI CONTACT heading
        heading_idx = None
        for idx, p in enumerate(doc.paragraphs):
            if (p.text or '').strip().upper() == 'CAI CONTACT':
                heading_idx = idx
                break

        if heading_idx is None:
            # Insert near the top: after the first paragraph
            anchor = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph("")
            heading = self._insert_paragraph_after(anchor, 'CAI CONTACT')
            if heading is None:
                heading = doc.add_paragraph('CAI CONTACT')
            for r in heading.runs:
                r.bold = True
                r.font.size = Pt(11)
            # Write lines under heading
            self._write_cai_contact_block(heading, cai)
        else:
            heading = doc.paragraphs[heading_idx]
            # Clear the next few contact lines (up to 5) if they look like contact lines
            to_clear = []
            for j in range(1, 6):
                k = heading_idx + j
                if k >= len(doc.paragraphs):
                    break
                txt = (doc.paragraphs[k].text or '').strip()
                if not txt:
                    to_clear.append(doc.paragraphs[k])
                    continue
                upper = txt.upper()
                if any(kw in upper for kw in ['SUMMARY', 'EMPLOYMENT HISTORY', 'WORK EXPERIENCE', 'EDUCATION']):
                    break
                if ('PHONE:' in upper) or ('EMAIL' in upper) or ('@' in txt) or (len(txt.split())<=4):
                    to_clear.append(doc.paragraphs[k])
                else:
                    break
            for para in to_clear:
                try:
                    for r in para.runs:
                        r.text = ''
                    para.text = ''
                except Exception:
                    pass
            # Ensure heading styling
            for r in heading.runs:
                r.bold = True
                r.font.size = Pt(11)
            # Write fresh block after heading
            self._write_cai_contact_block(heading, cai)

    def _write_cai_contact_block(self, heading_para, cai):
        """Write CAI contact lines under the given heading paragraph."""
        name = (cai.get('name') or '').strip()
        phone = (cai.get('phone') or '').strip()
        email = (cai.get('email') or '').strip()

        p_name = self._insert_paragraph_after(heading_para, name or '')
        if p_name is not None:
            for r in p_name.runs:
                r.bold = True
                r.font.size = Pt(10)

        if phone:
            p_phone = self._insert_paragraph_after(p_name or heading_para, f"Phone:  {phone}")
            if p_phone is not None:
                for r in p_phone.runs:
                    r.font.size = Pt(10)

        if email:
            p_email = self._insert_paragraph_after(p_phone or p_name or heading_para, f"Email:  {email}")
            if p_email is not None:
                for r in p_email.runs:
                    r.font.size = Pt(10)
    
    def _insert_experience_block(self, doc, after_paragraph, exp_data):
        """Insert a structured 2-column experience block"""
        try:
            # Get parsed data from resume parser
            company = exp_data.get('company', '')
            role = exp_data.get('role', '')
            duration = exp_data.get('duration', '')
            details = exp_data.get('details', [])
            
            # Fallback: if company/role not parsed, try to extract from title
            if not company and not role:
                title = exp_data.get('title', '')
                company, role = self._parse_company_role(title)
            
            # CRITICAL: Remove date fragments from company/role
            # Sometimes dates like "City – 08/ 06/" end up in company field
            import re
            if company:
                # Remove patterns like "City – 08/ 06/" or "– 04/" etc
                company = re.sub(r'\s*[–-]\s*\d{2}/\s*\d{2}/?\s*.*?$', '', company)
                company = re.sub(r'\s*City\s*[–-]\s*\d{2}/.*?$', '', company)
                company = company.strip(' ,–-')
            
            if role:
                role = re.sub(r'\s*[–-]\s*\d{2}/\s*\d{2}/?/\s*.*?$', '', role)
                role = re.sub(r'\s*City\s*[–-]\s*\d{2}/.*?$', '', role)
                role = role.strip(' ,–-')
            
            # Clean up duration format
            duration_clean = self._clean_duration(duration)
            
            # Build header line using a right-aligned tab instead of a table
            header_para = self._insert_paragraph_after(after_paragraph, '')
            # Right tab at ~6.5" (letter page width minus 1" margins), 1 inch = 1440 twips
            self._add_right_tab(header_para, pos_twips=9360)

            # Left text: prefer company, then role, then fallback
            left_text = (company or role or 'Experience').strip()
            left_run = header_para.add_run(left_text)
            left_run.bold = True
            left_run.font.size = Pt(10)

            if duration_clean:
                header_para.add_run('\t')
                dur_run = header_para.add_run(duration_clean)
                dur_run.bold = False
                dur_run.font.size = Pt(9)
            header_para.paragraph_format.space_after = Pt(0)

            # Role on its own line (bold)
            last_para = header_para
            if role:
                role_para = self._insert_paragraph_after(header_para, '')
                role_run = role_para.add_run(role)
                role_run.bold = True
                role_run.font.size = Pt(10)
                role_para.paragraph_format.space_after = Pt(0)
                last_para = role_para

            # Add details as individual bullet paragraphs
            if details:
                opt_details = self._optimize_details(details, max_bullets=12, max_words=22, max_chars=160)
                for detail in opt_details:
                    txt = (detail or '').strip()
                    if not txt:
                        continue
                    p = self._insert_paragraph_after(last_para, '')
                    p.paragraph_format.left_indent = Inches(0.25)
                    run = p.add_run('• ' + txt.lstrip('•–—-*● '))
                    run.font.size = Pt(9)
                    last_para = p
            
            return last_para
            
        except Exception as e:
            print(f"  ⚠️  Error inserting experience block: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _insert_education_block(self, doc, after_paragraph, edu_data):
        """Insert a structured 2-column education block"""
        try:
            # Get parsed data from resume parser
            degree = edu_data.get('degree', '')
            institution = edu_data.get('institution', '')
            year = edu_data.get('year', '')
            details = edu_data.get('details', [])
            
            # DEBUG: Show what we received
            print(f"      📚 Education data: degree='{degree[:50] if degree else ''}', institution='{institution[:30] if institution else ''}', year='{year}'")
            
            # Fallback: if institution not parsed, try to extract from degree or details
            if not institution:
                institution = self._extract_institution(degree, details)
            
            # Clean up year format
            year_clean = self._clean_duration(year)
            
            # Build header line as paragraph with right-aligned tab (no tables)
            header_para = self._insert_paragraph_after(after_paragraph, '')
            self._add_right_tab(header_para, pos_twips=9360)
            
            # Parse degree to separate degree type from field
            # Handle both formats:
            # 1. "Master of Science : Leadership" (colon separator)
            # 2. "Master of Science in Data Science" (in separator)
            # 3. "Bachelor of Technology in Computer Science" (in separator)
            
            degree_type = degree
            field_and_institution = institution
            field = ''
            
            if ':' in degree:
                # Format: "Master of Science : Leadership"
                parts = degree.split(':', 1)
                degree_type = parts[0].strip()  # "Master of Science"
                field = parts[1].strip() if len(parts) > 1 else ''  # "Leadership"
                print(f"      ✂️  Split at colon: LEFT='{degree_type}' | Field='{field}'")
            
            elif ' in ' in degree.lower():
                # Format: "Master of Science in Data Science"
                # Find the position of " in " (case-insensitive)
                lower_degree = degree.lower()
                in_pos = lower_degree.find(' in ')
                if in_pos > 0:
                    degree_type = degree[:in_pos].strip()  # "Master of Science"
                    field = degree[in_pos + 4:].strip()     # "Data Science"
                    print(f"      ✂️  Split at 'in': LEFT='{degree_type}' | Field='{field}'")
            
            else:
                print(f"      ℹ️  No split: Using full degree as LEFT='{degree_type}'")
            
            # Combine field with institution
            if field and institution:
                field_and_institution = f"{field} {institution}"
            elif field:
                field_and_institution = field
            
            print(f"      📐 Format: LEFT='{degree_type}' | RIGHT='{field_and_institution} {year_clean}'")
            
            # Degree type on the left (bold), year on the right
            deg_run = header_para.add_run(degree_type or 'Education')
            deg_run.bold = True
            deg_run.font.size = Pt(10)
            if year_clean:
                header_para.add_run('\t')
                yr_run = header_para.add_run(year_clean)
                yr_run.bold = False
                yr_run.font.size = Pt(9)
            header_para.paragraph_format.space_after = Pt(0)

            # Field + Institution on the next line (normal)
            last_para = header_para
            if field_and_institution:
                fi_para = self._insert_paragraph_after(header_para, field_and_institution)
                for run in fi_para.runs:
                    run.font.size = Pt(10)
                last_para = fi_para

            # Add details as bullet paragraphs
            if details:
                opt_details = self._optimize_details(details, max_bullets=3, max_words=18, max_chars=120)
                for detail in opt_details:
                    txt = (detail or '').strip()
                    if not txt or txt.lower() == (institution or '').lower():
                        continue
                    p = self._insert_paragraph_after(last_para, '')
                    p.paragraph_format.left_indent = Inches(0.25)
                    run = p.add_run('• ' + txt.lstrip('•–—-*● '))
                    run.font.size = Pt(9)
                    last_para = p
            
            return last_para
            
        except Exception as e:
            print(f"  ⚠️  Error inserting education block: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _clean_duration(self, duration):
        """Normalize duration.
        Prefer 'Mon YYYY-Mon YYYY' (e.g., 'Nov 2011-Sept 2025').
        Fallback to 'YYYY-YYYY' or single 'YYYY'.
        """
        if not duration:
            return ''

        t = (duration or '').strip()
        if not t:
            return ''

        # Normalize connectors
        t = re.sub(r'[–—]', '-', t)
        t = re.sub(r'\s*(to|–|—|-)\s*', '-', t, flags=re.IGNORECASE)

        present = bool(re.search(r'\b(current|present)\b', t, re.IGNORECASE))

        # Month map with 'Sept' spelling
        month_map = {
            'january': 'Jan', 'jan': 'Jan',
            'february': 'Feb', 'feb': 'Feb',
            'march': 'Mar', 'mar': 'Mar',
            'april': 'Apr', 'apr': 'Apr',
            'may': 'May',
            'june': 'Jun', 'jun': 'Jun',
            'july': 'Jul', 'jul': 'Jul',
            'august': 'Aug', 'aug': 'Aug',
            'september': 'Sept', 'sept': 'Sept', 'sep': 'Sept',
            'october': 'Oct', 'oct': 'Oct',
            'november': 'Nov', 'nov': 'Nov',
            'december': 'Dec', 'dec': 'Dec',
        }

        def abbr(m):
            return month_map.get(m.lower(), m[:3].title())

        # Find month-year tokens
        my = [m.groups() for m in re.finditer(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s*(?:,\s*)?((?:19|20)\d{2})\b', t, flags=re.IGNORECASE)]
        if my:
            start_m, start_y = my[0]
            start_m = abbr(start_m)
            if len(my) >= 2:
                end_m, end_y = my[-1]
                end_m = abbr(end_m)
                return f"{start_m} {start_y}-{end_m} {end_y}"
            # Single month-year; attach Present or end year if available
            if present:
                return f"{start_m} {start_y}-Present"
            end_years = re.findall(r'\b((?:19|20)\d{2})\b', t)
            if len(end_years) >= 2:
                return f"{start_m} {end_years[0]}-{end_years[-1]}"
            return f"{start_m} {start_y}"

        # Fallback to years-only
        years = re.findall(r'\b(?:19|20)\d{2}\b', t)
        if len(years) >= 2:
            return f"{years[0]}-{years[-1]}"
        if len(years) == 1:
            return years[0]
        return ''
    
    def _parse_company_role(self, title):
        """Parse company and role from title line"""
        # Common patterns: "Company Name - Role" or "Role at Company" or "Role, Company"
        if ' - ' in title:
            parts = title.split(' - ', 1)
            return parts[0].strip(), parts[1].strip()
        elif ' at ' in title.lower():
            parts = re.split(r'\s+at\s+', title, flags=re.IGNORECASE)
            return parts[1].strip() if len(parts) > 1 else '', parts[0].strip()
        elif ', ' in title:
            parts = title.split(', ', 1)
            return parts[1].strip(), parts[0].strip()
        else:
            # Assume entire line is company or role
            return title.strip(), ''
    
    def _extract_institution(self, degree, details):
        """Extract institution name from degree line or details"""
        # Check if degree line contains institution (common pattern: "Degree, Institution")
        if ', ' in degree:
            parts = degree.split(', ', 1)
            return parts[1].strip()
        
        # Look in details for institution keywords
        institution_keywords = ['university', 'college', 'institute', 'school', 'academy']
        for detail in details:
            if any(kw in detail.lower() for kw in institution_keywords):
                return detail.strip()
        
        return ''
    
    def _remove_cell_borders(self, cell):
        """Remove all borders from a table cell"""
        try:
            tc = cell._element
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'none')
                tcBorders.append(border)
            tcPr.append(tcBorders)
        except:
            pass
    
    def _insert_table_after(self, doc, anchor, rows=1, cols=2):
        """Create a table and position it immediately after the given anchor (Paragraph or Table)."""
        try:
            # Simply add table to document - python-docx will handle placement
            table = doc.add_table(rows=rows, cols=cols)
            
            # Try to move it after anchor, but don't fail if it doesn't work
            try:
                tbl = table._element
                if hasattr(anchor, '_element'):
                    anchor_elm = anchor._element
                elif hasattr(anchor, '_tbl'):
                    anchor_elm = anchor._tbl
                else:
                    anchor_elm = anchor
                
                # Only move if we have a valid anchor
                if anchor_elm is not None and hasattr(anchor_elm, 'addnext'):
                    anchor_elm.addnext(tbl)
            except:
                # If moving fails, table will just be at end of document
                pass

            return table

        except Exception as e:
            print(f"  ⚠️  Error creating table: {e}")
            return None

    def _cleanup_duplicate_bullets_after_section(self, doc, section_heading_para, next_section_name):
        """
        AGGRESSIVE cleanup: Scan entire document after inserting formatted content
        and delete ANY remaining bullet points between this section and next section.
        This ensures NO duplication of raw content.
        """
        try:
            print(f"    🧹 AGGRESSIVE cleanup: Removing ALL raw content until '{next_section_name}'...")
            
            # Find the section heading paragraph index
            heading_idx = None
            for idx, para in enumerate(doc.paragraphs):
                if para._element == section_heading_para._element:
                    heading_idx = idx
                    break
            
            if heading_idx is None:
                return
            
            # Now scan from heading to next section and delete EVERYTHING except tables and section headings
            deleted = 0
            paras_to_delete = []
            
            # List of all section keywords to preserve
            section_keywords = ['EDUCATION', 'SKILLS', 'SUMMARY', 'PROJECT', 'CERTIFICATION', 
                              'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT HISTORY', 
                              'PROFESSIONAL EXPERIENCE', 'CAREER HISTORY', 'QUALIFICATIONS',
                              'ACHIEVEMENTS', 'AWARDS', 'LANGUAGES']
            
            for idx in range(heading_idx + 1, len(doc.paragraphs)):
                para = doc.paragraphs[idx]
                text = para.text.strip().upper()
                
                # Stop at next section
                if next_section_name in text and len(text) < 50:
                    print(f"       Stopped at next section: {text[:40]}")
                    break
                
                # Skip if paragraph is empty
                if not text:
                    continue
                
                # PRESERVE section headings (don't delete them!)
                is_section_heading = any(keyword in text for keyword in section_keywords) and len(text) < 50
                if is_section_heading:
                    print(f"       Preserved section heading: '{text[:40]}'")
                    continue
                
                # DELETE this paragraph (it's duplicate raw content)
                paras_to_delete.append(para)
                deleted += 1
                if deleted <= 5:
                    print(f"       Removing duplicate: '{text[:60]}'")
            
            # Actually delete the paragraphs
            for para in paras_to_delete:
                p_element = para._element
                p_element.getparent().remove(p_element)
            
            print(f"    🧹 Cleanup complete: Removed {deleted} duplicate paragraphs")
            
        except Exception as e:
            print(f"    ⚠️  Cleanup error: {e}")
    
    def _delete_following_bullets(self, paragraph, max_scan=200):
        """Delete ALL content after a heading until next section - includes TABLES and paragraphs."""
        try:
            body = paragraph._element.getparent()
            node = paragraph._element.getnext()
            deleted_paras = 0
            deleted_tables = 0
            scanned = 0
            
            print(f"    🔍 Starting deletion scan (max {max_scan} items)...")
            
            while node is not None and scanned < max_scan:
                scanned += 1
                next_node = node.getnext()
                
                # DELETE TABLES (raw content might be in tables)
                if node.tag.endswith('tbl'):
                    print(f"       Deleting table #{deleted_tables + 1}")
                    body.remove(node)
                    deleted_tables += 1
                    node = next_node
                    continue
                
                # DELETE PARAGRAPHS
                if node.tag.endswith('p'):
                    # Extract plain text
                    text_nodes = node.xpath('.//w:t', namespaces=node.nsmap) if hasattr(node, 'xpath') else []
                    text = ''.join([t.text for t in text_nodes if t is not None and t.text is not None])
                    txt = (text or '').strip()
                    norm = txt.upper()
                    
                    # Stop ONLY at next section heading (not at tables or bullets)
                    section_keywords = ['EDUCATION', 'SKILLS', 'SUMMARY', 'PROJECT', 'CERTIFICATION', 
                                      'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT HISTORY', 
                                      'PROFESSIONAL EXPERIENCE', 'CAREER HISTORY', 'QUALIFICATIONS']
                    
                    if any(k in norm for k in section_keywords) and len(txt) < 50:
                        # This looks like a next section heading, stop deleting
                        print(f"       Stopped at next section: '{txt[:40]}'")
                        break
                    
                    # DELETE THIS PARAGRAPH (raw content)
                    if deleted_paras < 5:  # Log first 5 deletions
                        print(f"       Deleting para: '{txt[:60]}'...")
                    body.remove(node)
                    deleted_paras += 1
                
                node = next_node
            
            print(f"    🗑️  DELETED: {deleted_paras} paragraphs + {deleted_tables} tables (scanned {scanned} items)")
            
            if deleted_paras == 0 and deleted_tables == 0:
                print(f"    ⚠️  WARNING: Nothing was deleted! Content might still be there.")
                
        except Exception as e:
            print(f"    ⚠️  Error deleting content: {e}")
            import traceback
            traceback.print_exc()
    
    def _collect_bullets_after_heading(self, paragraph, max_scan=50):
        """Collect consecutive bullet-like paragraphs immediately after a heading/placeholder."""
        bullets = []
        try:
            node = paragraph._element.getnext()
            scanned = 0
            while node is not None and scanned < max_scan:
                scanned += 1
                if node.tag.endswith('tbl'):
                    # Collect all paragraph texts from the table as bullets
                    paras = node.xpath('.//w:p', namespaces=node.nsmap) if hasattr(node, 'xpath') else []
                    for p in paras:
                        tnodes = p.xpath('.//w:t', namespaces=p.nsmap) if hasattr(p, 'xpath') else []
                        text = ''.join([t.text for t in tnodes if t is not None and t.text is not None]).strip()
                        if text:
                            bullets.append(text.lstrip(' •–—-*●'))
                    break
                if node.tag.endswith('p'):
                    text_nodes = node.xpath('.//w:t', namespaces=node.nsmap) if hasattr(node, 'xpath') else []
                    text = ''.join([t.text for t in text_nodes if t is not None and t.text is not None])
                    txt = (text or '').strip()
                    norm = txt.upper()
                    if any(k in norm for k in ['EDUCATION', 'SKILLS', 'SUMMARY', 'PROJECT', 'CERTIFICATION', 'EXPERIENCE', 'WORK EXPERIENCE', 'EMPLOYMENT HISTORY']):
                        break
                    if txt.startswith(('•', '-', '–', '—', '*', '●')) or re.match(r'^\d+[\).\-\s]', txt):
                        bullets.append(txt.lstrip(' •–—-*●'))
                    else:
                        break
                node = node.getnext()
        except Exception:
            pass
        return bullets

    def _delete_next_table(self, paragraph):
        """Delete the immediate next table after a heading/placeholder (used when raw content is a table)."""
        try:
            node = paragraph._element.getnext()
            deleted = 0
            # Delete multiple tables if they exist
            while node is not None and node.tag.endswith('tbl'):
                next_node = node.getnext()
                parent = node.getparent()
                parent.remove(node)
                deleted += 1
                node = next_node
            if deleted > 0:
                print(f"    🗑️  Deleted {deleted} old table(s)")
        except Exception as e:
            print(f"    ⚠️  Error deleting tables: {e}")
    
    def _build_experience_from_bullets(self, bullets):
        """Best-effort convert raw bullet lines into structured exp list when parser is empty."""
        exps = []
        i = 0
        while i < len(bullets):
            line = bullets[i]
            # Case: role + dates on this line
            if re.search(r'(?:19|20)\d{2}', line):
                duration = self._clean_duration(line)
                role = re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z]*\s+(?:19|20)\d{2}\b', '', line, flags=re.IGNORECASE)
                role = re.sub(r'\b(?:19|20)\d{2}\b', '', role)
                role = re.sub(r'\b(to|–|—|-)\b', '', role, flags=re.IGNORECASE).strip(' ,;:-')
                # Next bullet as company if available
                company = ''
                if i + 1 < len(bullets):
                    company = bullets[i+1]
                    # Strip obvious location fragments
                    company = re.sub(r',[^,]*\b(?:city|state|india|usa|uk)\b.*$', '', company, flags=re.IGNORECASE).strip()
                details = []
                j = i + 2
                while j < len(bullets):
                    if re.search(r'(?:19|20)\d{2}', bullets[j]):
                        break
                    details.append(bullets[j])
                    j += 1
                exps.append({'company': company, 'role': role, 'duration': duration, 'details': details})
                i = j
            else:
                i += 1
        return exps
    
    def _build_education_from_bullets(self, bullets):
        """Convert raw education bullets into degree/institution/year list when parser is empty."""
        edus = []
        i = 0
        while i < len(bullets):
            line = bullets[i]
            degree = ''
            institution = ''
            year = ''
            # Try to split by institution keyword
            m = re.search(r'(university|college|school|institute|academy)\b.*', line, flags=re.IGNORECASE)
            if m:
                degree = line[:m.start()].strip(' ,;:-')
                institution = line[m.start():].strip()
                year = self._clean_duration(line)
            else:
                # If next line is year, treat current as degree+institution
                if i + 1 < len(bullets) and re.search(r'(?:19|20)\d{2}', bullets[i+1]):
                    degree = line
                    year = self._clean_duration(bullets[i+1])
                    i += 1
                else:
                    degree = line
                    year = self._clean_duration(line)
            # Cleanup
            degree = degree.strip()
            institution = re.sub(r',[^,]*\b(?:city|state|india|usa|uk)\b.*$', '', institution, flags=re.IGNORECASE).strip()
            edus.append({'degree': degree, 'institution': institution, 'year': year, 'details': []})
            i += 1
        return edus

    def _optimize_details(self, details, max_bullets=12, max_words=22, max_chars=160):
        """Shorten and normalize bullet points while preserving meaning.
        - trims bullets, normalizes acronyms, removes duplicate entries
        - caps each bullet by words/chars
        """
        cleaned = []
        seen = set()
        for d in details:
            if not d or not isinstance(d, str):
                continue
            t = d.strip()
            if not t:
                continue
            # Remove leading bullet chars
            t = t.lstrip('•–—-*● \t-').strip()
            # Normalize common wording
            repl = [
                (r'\bas well as\b', 'and'),
                (r'\bin order to\b', 'to'),
                (r'\bkey performance indicators\s*\(([^\)]+)\)', r'\1'),
                (r'\bkey performance indicators\b', 'KPIs'),
                (r'\bquickbooks\b', 'QuickBooks'),
                (r'\bums?\s*worldship\b', 'UPS WorldShip'),
            ]
            for pattern, repl_to in repl:
                t = re.sub(pattern, repl_to, t, flags=re.IGNORECASE)

            t = self._shorten_text(t, max_words=max_words, max_chars=max_chars)
            t = self._normalize_acronyms(t)

            key = t.lower()
            if key and key not in seen:
                seen.add(key)
                cleaned.append(t.rstrip())

            if len(cleaned) >= max_bullets:
                break
        return cleaned

    def _normalize_acronyms(self, text):
        """Normalize common acronyms casing."""
        mapping = {
            'kpi': 'KPI', 'kpis': 'KPIs',
            'lms': 'LMS',
            'qa': 'QA',
        }
        def repl(m):
            return mapping.get(m.group(0).lower(), m.group(0))
        return re.sub(r'\b(kpis?|lms|qa)\b', repl, text, flags=re.IGNORECASE)

    def _shorten_text(self, text, max_words=22, max_chars=160):
        """Heuristic shortening: prefer cutting at clause boundaries, then word limit."""
        t = re.sub(r'\s+', ' ', text).strip()
        # Prefer to cut at clause markers if too long
        if len(t) > max_chars:
            for marker in ['; ', '. ', ' which ', ' that ', ' ensuring ', ' including ', ' while ', ' whereas ', ' whereby ']:
                idx = t.lower().find(marker)
                if 0 < idx <= max_chars:
                    t = t[:idx].rstrip('.; ,')
                    break
        # Enforce word cap
        words = t.split()
        if len(words) > max_words:
            t = ' '.join(words[:max_words]).rstrip(',;')
        # Ensure terminal period for readability
        if t and t[-1] not in '.!?':
            t = t + '.'
        return t
    
    def _create_replacement_map(self):
        """Create comprehensive replacement map"""
        replacements = {}
        
        # Personal information - Multiple formats
        # NOTE: Be specific to avoid replacing CAI contact manager info
        if self.resume_data.get('name'):
            display_name = f"<{self.resume_data['name']}>"
            replacements['[NAME]'] = display_name
            replacements['[CANDIDATE NAME]'] = display_name
            replacements['<CANDIDATE NAME>'] = display_name
            replacements["<Candidate's full name>"] = display_name
            replacements['<Candidate Name>'] = display_name
            replacements['<Name>'] = display_name
            replacements['Your Name'] = display_name
            replacements['CANDIDATE NAME'] = display_name
            # DO NOT replace "Insert name" as it might be in CAI contact section
        
        if self.resume_data.get('email'):
            # ONLY replace explicit placeholders, NOT actual email addresses
            replacements['[EMAIL]'] = self.resume_data['email']
            replacements['[Email]'] = self.resume_data['email']
            replacements['<EMAIL>'] = self.resume_data['email']
            replacements['<Email>'] = self.resume_data['email']
            replacements['<Candidate Email>'] = self.resume_data['email']
            # DO NOT replace example emails or "Email:" labels to avoid changing CAI contact info
        
        if self.resume_data.get('phone'):
            # ONLY replace explicit placeholders, NOT actual phone numbers
            replacements['[PHONE]'] = self.resume_data['phone']
            replacements['[Phone]'] = self.resume_data['phone']
            replacements['<PHONE>'] = self.resume_data['phone']
            replacements['<Phone>'] = self.resume_data['phone']
            replacements['<Candidate Phone>'] = self.resume_data['phone']
            # DO NOT replace example numbers or "Phone:" labels to avoid changing CAI contact info
        
        if self.resume_data.get('address'):
            replacements['[ADDRESS]'] = self.resume_data['address']
            replacements['[Address]'] = self.resume_data['address']
            replacements['<ADDRESS>'] = self.resume_data['address']
            replacements['<Address>'] = self.resume_data['address']
            replacements['Your Address'] = self.resume_data['address']
        
        if self.resume_data.get('linkedin'):
            replacements['[LINKEDIN]'] = self.resume_data['linkedin']
            replacements['[LinkedIn]'] = self.resume_data['linkedin']
            replacements['<LINKEDIN>'] = self.resume_data['linkedin']
            replacements['<LinkedIn>'] = self.resume_data['linkedin']
            replacements['linkedin.com/in/username'] = self.resume_data['linkedin']
        
        if self.resume_data.get('dob'):
            replacements['[DOB]'] = self.resume_data['dob']
            replacements['[Date of Birth]'] = self.resume_data['dob']
            replacements['<DOB>'] = self.resume_data['dob']
        
        return replacements
    
    def _text_contains(self, text, search_term):
        """Case-insensitive text search"""
        return search_term.lower() in text.lower()
    
    def _replace_in_paragraph(self, paragraph, search_term, replacement):
        """Replace text in paragraph while preserving formatting"""
        replaced = 0
        
        # First try: Replace in individual runs
        for run in paragraph.runs:
            if self._text_contains(run.text, search_term):
                # Case-insensitive replacement
                pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                run.text = pattern.sub(replacement, run.text)
                replaced += 1
        
        # Second try: If not found in individual runs, text might be split
        # Combine all runs and check
        if replaced == 0 and self._text_contains(paragraph.text, search_term):
            # Text is split across runs - need to handle differently
            full_text = paragraph.text
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            new_text = pattern.sub(replacement, full_text)
            
            if new_text != full_text:
                # Clear all runs and add new text
                for run in paragraph.runs:
                    run.text = ''
                
                # Add replacement text to first run
                if paragraph.runs:
                    paragraph.runs[0].text = new_text
                    replaced += 1
                else:
                    # No runs, add new run
                    paragraph.add_run(new_text)
                    replaced += 1
        
        return replaced

    def _regex_replace_paragraph(self, paragraph, pattern, replacement):
        """Regex-based replacement across runs: rebuilds paragraph text."""
        try:
            full_text = paragraph.text or ''
            new_text = re.sub(pattern, replacement, full_text, flags=re.IGNORECASE)
            if new_text != full_text:
                # clear runs and set new_text
                for run in paragraph.runs:
                    run.text = ''
                if paragraph.runs:
                    paragraph.runs[0].text = new_text
                else:
                    paragraph.add_run(new_text)
        except Exception:
            pass
    
    def _add_sections_content(self, doc):
        """Add resume sections to document and replace placeholders - SIMPLIFIED to prevent duplication"""
        sections_added = 0
        
        # Track what we've inserted to prevent duplicates
        if not hasattr(self, '_experience_inserted'):
            self._experience_inserted = False
        if not hasattr(self, '_education_inserted'):
            self._education_inserted = False
        
        print(f"\n🔍 Scanning document for experience/education sections...")
        
        # SINGLE PASS: Look for headings only (ignore placeholders to avoid duplication)
        for para_idx, paragraph in enumerate(doc.paragraphs):
            para_text = paragraph.text.upper().strip()
            
            # EXPERIENCE SECTION
            if not self._experience_inserted and any(marker in para_text for marker in ['EMPLOYMENT HISTORY', 'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE', 'EXPERIENCE']):
                experiences = self.resume_data.get('experience', [])
                # Fallback: build structured experiences from the raw bullets beneath the heading
                if not experiences:
                    raw_bullets = self._collect_bullets_after_heading(paragraph, max_scan=120)
                    if raw_bullets:
                        experiences = self._build_experience_from_bullets(raw_bullets)
                        print(f"  🔄 Built {len(experiences)} experience entries from raw bullets")
                if experiences:
                    print(f"  ✓ Found EXPERIENCE at paragraph {para_idx}: '{paragraph.text[:50]}'")
                    
                    # STEP 1: Clear the heading paragraph (keep only the heading text)
                    original_heading = paragraph.text.strip()
                    for run in paragraph.runs:
                        run.text = ''
                    if paragraph.runs:
                        paragraph.runs[0].text = 'EMPLOYMENT HISTORY'
                        paragraph.runs[0].bold = True
                        paragraph.runs[0].font.size = Pt(12)
                    
                    # STEP 2: Delete ALL following content (tables + paragraphs)
                    self._delete_following_bullets(paragraph)
                    self._delete_next_table(paragraph)
                    
                    # STEP 3: Insert clean structured blocks
                    last_element = paragraph
                    for exp in experiences[:10]:
                        table = self._insert_experience_block(doc, last_element, exp)
                        if table:
                            last_element = table
                    
                    # STEP 4: Skip aggressive cleanup to preserve newly inserted bullets
                    # self._cleanup_duplicate_bullets_after_section(doc, paragraph, 'EDUCATION')
                    
                    self._experience_inserted = True
                    sections_added += 1
                    print(f"    → Inserted {len(experiences[:10])} experience entries")
                    continue
            
            # EDUCATION SECTION
            if not self._education_inserted and 'EDUCATION' in para_text:
                education = self.resume_data.get('education', [])
                if education:
                    print(f"  ✓ Found EDUCATION at paragraph {para_idx}: '{paragraph.text[:50]}'")
                    
                    # STEP 1: Clear the heading paragraph (keep only the heading text)
                    for run in paragraph.runs:
                        run.text = ''
                    if paragraph.runs:
                        paragraph.runs[0].text = 'EDUCATION'
                        paragraph.runs[0].bold = True
                        paragraph.runs[0].font.size = Pt(12)
                    
                    # STEP 2: Delete ALL following content (tables + paragraphs)
                    self._delete_following_bullets(paragraph)
                    self._delete_next_table(paragraph)
                    
                    # STEP 3: Insert clean structured blocks
                    last_element = paragraph
                    for edu in education[:5]:
                        table = self._insert_education_block(doc, last_element, edu)
                        if table:
                            last_element = table
                    
                    # STEP 4: Skip aggressive cleanup to preserve newly inserted bullets
                    # self._cleanup_duplicate_bullets_after_section(doc, paragraph, 'SKILLS')
                    
                    self._education_inserted = True
                    sections_added += 1
                    print(f"    → Inserted {len(education[:5])} education entries")
                    continue
        
        print(f"\n✅ Section insertion complete. Experience inserted: {self._experience_inserted}, Education inserted: {self._education_inserted}")
        return sections_added
    
    def _detect_table_type(self, table):
        """
        DYNAMICALLY detect table type by analyzing column headers.
        Returns: 'skills', 'experience', 'education', or None
        """
        if len(table.rows) < 1:
            return None
        
        # Get all text from first few rows (headers might span multiple rows)
        header_text = ''
        for row_idx in range(min(3, len(table.rows))):
            for cell in table.rows[row_idx].cells:
                header_text += ' ' + cell.text.lower()
        
        # Skills table indicators
        skills_indicators = ['skill', 'technology', 'competency', 'expertise', 'proficiency', 
                           'years used', 'last used', 'technical']
        
        # Experience/Employment table indicators  
        experience_indicators = ['employment', 'company', 'employer', 'position', 'role', 
                                'job title', 'work history', 'experience', 'responsibilities']
        
        # Education table indicators
        education_indicators = ['education', 'degree', 'institution', 'university', 'college', 
                              'school', 'graduation', 'qualification']
        
        # Count matches for each type
        skills_score = sum(1 for ind in skills_indicators if ind in header_text)
        exp_score = sum(1 for ind in experience_indicators if ind in header_text)
        edu_score = sum(1 for ind in education_indicators if ind in header_text)
        
        # Return type with highest score
        if skills_score > 0 and skills_score >= exp_score and skills_score >= edu_score:
            return 'skills'
        elif exp_score > 0 and exp_score >= edu_score:
            return 'experience'
        elif edu_score > 0:
            return 'education'
        
        return None
    
    def _fill_dynamic_table(self, table, table_type):
        """
        DYNAMICALLY fill table based on column headers and data type.
        Works with ANY column structure!
        """
        if len(table.rows) < 1:
            return 0
        
        print(f"     🔍 Analyzing table structure...")
        
        # Get column headers (from first row)
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
        print(f"     📋 Column headers: {headers}")
        
        # Map columns to data fields intelligently
        column_mapping = self._map_columns_to_fields(headers, table_type)
        print(f"     🗺️  Column mapping: {column_mapping}")
        
        # Get data to fill
        if table_type == 'skills':
            data_items = self._get_skills_data()
        elif table_type == 'experience':
            data_items = self._get_experience_data()
        elif table_type == 'education':
            data_items = self._get_education_data()
        else:
            return 0
        
        if not data_items:
            print(f"     ⚠️  No {table_type} data available")
            return 0
        
        print(f"     📊 Found {len(data_items)} {table_type} items to fill")
        
        # Clear existing rows (keep header)
        for i in reversed(range(1, len(table.rows))):
            table._element.remove(table.rows[i]._element)
        
        # Fill rows dynamically
        filled = 0
        for item in data_items[:15]:  # Limit to 15 rows
            new_row = table.add_row()
            
            for col_idx, field_name in column_mapping.items():
                if col_idx < len(new_row.cells) and field_name:
                    value = item.get(field_name, '')
                    new_row.cells[col_idx].text = str(value)
            
            filled += 1
            if filled <= 3:
                print(f"        ✓ Row {filled}: {list(item.values())[:3]}")
        
        return filled
    
    def _map_columns_to_fields(self, headers, table_type):
        """
        INTELLIGENT column mapping - maps table columns to resume data fields
        based on semantic understanding of column names.
        """
        mapping = {}  # {column_index: field_name}
        
        if table_type == 'skills':
            # Define possible column patterns for skills
            patterns = {
                'skill': ['skill', 'technology', 'competency', 'expertise', 'tool', 'name'],
                'years': ['year', 'experience', 'exp', 'yrs', 'duration', 'used'],
                'last_used': ['last', 'recent', 'current', 'latest', 'when']
            }
        elif table_type == 'experience':
            patterns = {
                'company': ['company', 'employer', 'organization', 'firm'],
                'role': ['role', 'position', 'title', 'job'],
                'duration': ['date', 'year', 'period', 'duration', 'from', 'to', 'when'],
                'location': ['location', 'city', 'state', 'place'],
                'responsibilities': ['responsibilit', 'duties', 'description', 'summary']
            }
        elif table_type == 'education':
            patterns = {
                'degree': ['degree', 'qualification', 'certificate', 'program'],
                'institution': ['institution', 'university', 'college', 'school'],
                'year': ['year', 'date', 'graduation', 'completion'],
                'field': ['field', 'major', 'specialization', 'subject'],
                'gpa': ['gpa', 'grade', 'marks', 'score']
            }
        else:
            return mapping
        
        # Map each column to best matching field
        for col_idx, header in enumerate(headers):
            header_lower = header.lower()
            best_match = None
            best_score = 0
            
            for field_name, keywords in patterns.items():
                score = sum(1 for kw in keywords if kw in header_lower)
                if score > best_score:
                    best_score = score
                    best_match = field_name
            
            if best_match and best_score > 0:
                mapping[col_idx] = best_match
                print(f"        Column {col_idx} ('{header}') → {best_match}")
        
        return mapping
    
    def _get_skills_data(self):
        """Get skills data in standardized format"""
        skills_list = []
        raw_skills = self.resume_data.get('skills', [])
        
        for skill in raw_skills[:15]:
            skill_name = skill if isinstance(skill, str) else skill.get('name', '')
            skills_list.append({
                'skill': skill_name,
                'years': '2+ years',  # Default
                'last_used': 'Recent'
            })
        
        return skills_list
    
    def _get_experience_data(self):
        """Get experience data in standardized format"""
        exp_list = []
        experiences = self.resume_data.get('experience', [])
        
        for exp in experiences[:10]:
            exp_list.append({
                'company': exp.get('company', ''),
                'role': exp.get('role', ''),
                'duration': exp.get('duration', ''),
                'location': '',  # Extract if available
                'responsibilities': '\n'.join(exp.get('details', [])[:3])
            })
        
        return exp_list
    
    def _get_education_data(self):
        """Get education data in standardized format"""
        edu_list = []
        education = self.resume_data.get('education', [])
        
        for edu in education[:5]:
            edu_list.append({
                'degree': edu.get('degree', ''),
                'institution': edu.get('institution', ''),
                'year': edu.get('year', ''),
                'field': '',  # Extract from degree if available
                'gpa': ''
            })
        
        return edu_list
    
    def _is_skills_table(self, table):
        """Check if table is a skills table by examining headers - FLEXIBLE detection"""
        if len(table.rows) < 1:  # Changed from 2 to 1 - just need header row
            print(f"       ⚠️  Table has <1 rows ({len(table.rows)}), skipping")
            return False
        
        # Get first row (header) text - check multiple rows in case header spans multiple
        header_texts = []
        rows_to_check = min(3, len(table.rows))  # Check first 3 rows for headers
        
        for row_idx in range(rows_to_check):
            row_texts = [cell.text.strip().lower() for cell in table.rows[row_idx].cells]
            # Skip completely empty rows
            if any(t for t in row_texts):
                header_texts.extend(row_texts)
        
        # Join all potential headers
        all_headers = ' '.join(header_texts)
        
        print(f"       🔍 Table has {len(table.rows)} rows, {len(table.columns)} columns")
        print(f"       🔍 First row cells: {[cell.text.strip() for cell in table.rows[0].cells]}")
        print(f"       🔍 All header candidates: {header_texts[:6]}")  # Show first 6
        print(f"       🔍 Combined text: '{all_headers[:100]}'")  # First 100 chars
        
        # Check for skills table indicators - VERY FLEXIBLE
        skills_keywords = ['skill', 'skills', 'technology', 'technologies', 'competency', 'competencies', 
                          'technical', 'proficiency', 'expertise', 'tool', 'tools', 'qualification']
        years_keywords = ['years', 'experience', 'years used', 'years of experience', 'exp', 'yrs', 
                         'year', 'duration']
        last_used_keywords = ['last used', 'last', 'recent', 'most recent', 'latest', 'when', 'current']
        
        has_skill_col = any(kw in all_headers for kw in skills_keywords)
        has_years_col = any(kw in all_headers for kw in years_keywords)
        has_last_used_col = any(kw in all_headers for kw in last_used_keywords)
        
        # Also check if table has exactly 3 columns (Skill, Years, Last Used pattern)
        has_three_cols = len(table.columns) == 3
        
        print(f"       📊 Detection results:")
        print(f"          - Has 3 columns: {has_three_cols} (actual: {len(table.columns)})")
        print(f"          - Has skill column: {has_skill_col}")
        print(f"          - Has years column: {has_years_col}")
        print(f"          - Has last_used column: {has_last_used_col}")
        
        # It's a skills table if:
        # 1. Has skill keyword AND (years OR last_used keyword)
        # 2. OR has 3 columns with years AND last_used (common pattern)
        is_skills = (has_skill_col and (has_years_col or has_last_used_col)) or \
                    (has_three_cols and has_years_col and has_last_used_col)
        
        print(f"       {'✅ IS SKILLS TABLE' if is_skills else '❌ NOT SKILLS TABLE'}")
        
        return is_skills
    
    def _fill_skills_table(self, table):
        """Fill skills table with candidate's skills data"""
        if len(table.rows) < 1:
            print(f"     ⚠️  Table has no rows, cannot fill")
            return 0
        
        # Get header row to identify columns
        header_row = table.rows[0]
        header_texts = [cell.text.strip().lower() for cell in header_row.cells]
        
        print(f"     📋 Filling skills table...")
        print(f"     📋 Table headers: {header_texts}")
        print(f"     📋 Table has {len(table.rows)} rows initially")
        
        # Find column indices - FLEXIBLE matching
        skill_col = None
        years_col = None
        last_used_col = None
        
        skill_keywords = ['skill', 'technology', 'competency', 'technical', 'tool', 'expertise', 'proficiency']
        years_keywords = ['years', 'experience', 'exp', 'yrs', 'years used']
        last_keywords = ['last', 'recent', 'latest', 'last used', 'most recent']
        
        for idx, header in enumerate(header_texts):
            # Match skill column
            if any(kw in header for kw in skill_keywords) and skill_col is None:
                skill_col = idx
                print(f"     ✓ Skill column: {idx} ('{header}')")
            # Match years column
            elif any(kw in header for kw in years_keywords) and years_col is None:
                years_col = idx
                print(f"     ✓ Years column: {idx} ('{header}')")
            # Match last used column
            elif any(kw in header for kw in last_keywords) and last_used_col is None:
                last_used_col = idx
                print(f"     ✓ Last Used column: {idx} ('{header}')")
        
        if skill_col is None:
            print(f"     ⚠️  No skill column found in headers: {header_texts}")
            return 0
        
        # Get skills from resume
        skills_data = self._extract_skills_with_details()
        
        print(f"     📊 Extracted {len(skills_data) if skills_data else 0} skills from resume")
        
        if not skills_data or len(skills_data) == 0:
            print(f"     ⚠️  No skills data to fill!")
            # Get raw skills list as fallback
            raw_skills = self.resume_data.get('skills', [])
            print(f"     ℹ️  Raw skills available: {len(raw_skills)}")
            if raw_skills:
                # Convert raw skills to format expected
                skills_data = [{'skill': s, 'years': '1+ years', 'last_used': 'Recent'} for s in raw_skills[:15]]
                print(f"     ✓ Using {len(skills_data)} raw skills as fallback")
            else:
                return 0
        
        # Clear existing data rows (keep header)
        rows_to_delete = []
        for i in range(1, len(table.rows)):
            rows_to_delete.append(i)
        
        # Delete from bottom to top to avoid index issues
        for i in reversed(rows_to_delete):
            table._element.remove(table.rows[i]._element)
        
        # Add skills rows
        filled_count = 0
        print(f"     🔄 Adding {min(15, len(skills_data))} skill rows to table...")
        
        for skill_info in skills_data[:15]:  # Limit to 15 skills
            # Add new row
            new_row = table.add_row()
            
            skill_name = skill_info.get('skill', '')
            
            # Fill skill name
            if skill_col is not None:
                new_row.cells[skill_col].text = skill_name
            
            # Fill years
            if years_col is not None:
                new_row.cells[years_col].text = skill_info.get('years', '')
            
            # Fill last used
            if last_used_col is not None:
                new_row.cells[last_used_col].text = skill_info.get('last_used', '')
            
            filled_count += 1
            if filled_count <= 3:
                print(f"        ✓ Added: {skill_name}")
        
        print(f"     ✅ Successfully filled {filled_count} skill rows")
        return filled_count
    
    def _extract_skills_with_details(self):
        """Extract skills with years and last used info from resume data"""
        skills_list = []
        
        # Get skills from resume data
        skills = self.resume_data.get('skills', [])
        experience = self.resume_data.get('experience', [])
        
        # Try to extract years from experience
        current_year = 2025
        
        for skill in skills[:15]:  # Limit to 15 skills
            skill_name = skill if isinstance(skill, str) else skill.get('name', '')
            
            # Try to find this skill in experience to get dates
            years_exp = ''
            last_used = ''
            
            # Search through experience for this skill
            for exp in experience:
                exp_text = str(exp).lower()
                if skill_name.lower() in exp_text:
                    # Try to extract years
                    duration = exp.get('duration', '') if isinstance(exp, dict) else ''
                    
                    # Parse years from duration like "2020-2023" or "2020-Present"
                    import re
                    year_matches = re.findall(r'(20\d{2})', str(duration))
                    if year_matches:
                        start_year = int(year_matches[0])
                        end_year = int(year_matches[-1]) if len(year_matches) > 1 else current_year
                        
                        if 'present' in str(duration).lower() or 'current' in str(duration).lower():
                            end_year = current_year
                        
                        years_count = end_year - start_year
                        if years_count > 0:
                            years_exp = f"{years_count}+ years"
                            last_used = str(end_year) if end_year < current_year else "Present"
                    
                    break
            
            # Default values if not found in experience
            if not years_exp:
                years_exp = "1+ years"
            if not last_used:
                last_used = "Recent"
            
            skills_list.append({
                'skill': skill_name,
                'years': years_exp,
                'last_used': last_used
            })
        
        return skills_list
    
    def _find_matching_resume_section(self, section_key, resume_sections):
        """Find matching resume section with synonyms"""
        # Direct match
        if section_key in resume_sections:
            return resume_sections[section_key]

        synonyms = {
            'experience': ['experience', 'employment', 'work', 'professional'],
            'education': ['education', 'academic', 'qualification', 'academics'],
            'skills': ['skills', 'technical', 'competencies', 'expertise'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'projects': ['projects', 'portfolio'],
            'certifications': ['certifications', 'certificates', 'licenses'],
            'awards': ['awards', 'achievements', 'honors']
        }

        patterns = synonyms.get(section_key, [section_key])
        for resume_key, content in resume_sections.items():
            key_lower = resume_key.lower()
            if any(p in key_lower for p in patterns):
                return content

        return []
    
    def _convert_to_pdf(self, docx_path, pdf_path):
        """Convert DOCX to PDF"""
        try:
            if HAS_WIN32:
                # Use Word COM to convert
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                
                doc = word.Documents.Open(os.path.abspath(docx_path))
                doc.SaveAs2(os.path.abspath(pdf_path), FileFormat=17)  # 17 = PDF format
                doc.Close()
                word.Quit()
                
                return True
            else:
                print("⚠️  PDF conversion requires Microsoft Word")
                return False
                
        except Exception as e:
            print(f"❌ PDF conversion error: {e}")
            return False


def format_word_document(resume_data, template_analysis, output_path):
    """Main function for Word document formatting"""
    formatter = WordFormatter(resume_data, template_analysis, output_path)
    return formatter.format()
