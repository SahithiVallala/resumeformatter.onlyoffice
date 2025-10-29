from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import os
import traceback
import json

from config import Config
from models.database import TemplateDB
from utils.advanced_template_analyzer import analyze_template
from utils.advanced_resume_parser import parse_resume
from utils.intelligent_formatter import format_resume_intelligent

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Enable CORS for React frontend (allow multiple localhost ports)
CORS(
    app,
    resources={r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001"
        ]
    }}
)

db = TemplateDB()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# ===== Persistent CAI Contact storage used by both backend and formatter =====
def _cai_store_path():
    home = os.path.expanduser("~")
    return os.path.join(home, ".resume_formatter_cai_contact.json")


@app.route('/api/cai-contact', methods=['GET'])
def get_cai_contact():
    """Return stored CAI contact. If none, return empty fields."""
    path = _cai_store_path()
    data = {"name": "", "phone": "", "email": ""}
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                loaded = json.load(f) or {}
                data.update({k: loaded.get(k, "") for k in data.keys()})
    except Exception:
        pass
    return jsonify({"success": True, "contact": data})


@app.route('/api/cai-contact', methods=['POST'])
def save_cai_contact():
    """Persist CAI contact. Overwrites stored values. Body: JSON {name, phone, email}."""
    try:
        payload = request.get_json(silent=True) or {}
        data = {
            "name": str(payload.get("name", "")).strip(),
            "phone": str(payload.get("phone", "")).strip(),
            "email": str(payload.get("email", "")).strip(),
        }
        path = _cai_store_path()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"success": True, "contact": data})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get all templates"""
    templates = db.get_all_templates()
    return jsonify({'success': True, 'templates': templates})

@app.route('/api/templates', methods=['POST'])
def upload_template():
    """Upload and analyze template"""
    try:
        if 'template_file' not in request.files or 'template_name' not in request.form:
            return jsonify({'success': False, 'message': 'Missing file or name'}), 400
        
        file = request.files['template_file']
        name = request.form['template_name'].strip()
        
        if file.filename == '' or not name:
            return jsonify({'success': False, 'message': 'Invalid input'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_type = filename.rsplit('.', 1)[1].lower()
        template_id = str(uuid.uuid4())
        saved_filename = f"{template_id}_{filename}"
        file_path = os.path.join(Config.TEMPLATE_FOLDER, saved_filename)
        file.save(file_path)
        
        print(f"\n{'='*70}")
        print(f"📤 UPLOADING TEMPLATE: {name}")
        print(f"{'='*70}\n")
        
        # Analyze template with advanced analyzer
        format_data = analyze_template(file_path)
        
        # Save to database
        db.add_template(template_id, name, saved_filename, file_type, format_data)
        
        return jsonify({
            'success': True,
            'id': template_id,
            'name': name,
            'message': 'Template uploaded and analyzed successfully'
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/format', methods=['POST'])
def format_resumes():
    """Format resumes using selected template"""
    try:
        if 'template_id' not in request.form or 'resume_files' not in request.files:
            return jsonify({'success': False, 'message': 'Missing template or files'}), 400
        
        template_id = request.form['template_id']
        template = db.get_template(template_id)
        
        if not template:
            return jsonify({'success': False, 'message': 'Template not found'}), 404
        
        files = request.files.getlist('resume_files')
        formatted_files = []
        
        # Get template analysis
        template_analysis = template['format_data']
        
        # Ensure paths are set
        template_file_path = os.path.join(Config.TEMPLATE_FOLDER, template['filename'])
        template_analysis['template_path'] = template_file_path
        template_analysis['template_type'] = template['file_type']
        
        print(f"\n{'='*70}")
        print(f"🎯 FORMATTING SESSION")
        print(f"{'='*70}")
        print(f"📋 Template: {template['name']}")
        print(f"📁 Template Path: {template_file_path}")
        print(f"✓ Template Exists: {os.path.exists(template_file_path)}")
        print(f"📊 Resumes to Process: {len(files)}")
        print(f"{'='*70}\n")
        
        for idx, file in enumerate(files, 1):
            if file.filename == '' or not allowed_file(file.filename):
                continue
            
            # Save resume
            filename = secure_filename(file.filename)
            file_type = filename.rsplit('.', 1)[1].lower()
            resume_id = str(uuid.uuid4())
            saved_filename = f"{resume_id}_{filename}"
            file_path = os.path.join(Config.RESUME_FOLDER, saved_filename)
            file.save(file_path)
            
            print(f"\n{'─'*70}")
            print(f"📄 Processing Resume {idx}/{len(files)}: {filename}")
            print(f"{'─'*70}")
            
            # Parse resume with advanced parser
            resume_data = parse_resume(file_path, file_type)
            
            # Add CAI contact data from request if provided
            if 'cai_contact' in request.form:
                try:
                    import json
                    cai_data = json.loads(request.form['cai_contact'])
                    resume_data['cai_contact'] = cai_data
                    resume_data['edit_cai_contact'] = request.form.get('edit_cai_contact') == 'true'
                    print(f"  ✏️  CAI Contact edit enabled: {cai_data}")
                except Exception as e:
                    print(f"  ⚠️  Error parsing CAI contact data: {e}")
            
            if resume_data:
                # Format resume with intelligent formatter
                # Create DOCX only (no PDF conversion for speed)
                docx_filename = f"formatted_{resume_id}.docx"
                docx_path = os.path.join(Config.OUTPUT_FOLDER, docx_filename)
                
                if format_resume_intelligent(resume_data, template_analysis, docx_path):
                    # Check if DOCX was created
                    if os.path.exists(docx_path):
                        # Convert DOCX to PDF for preview
                        pdf_filename = docx_filename.replace('.docx', '.pdf')
                        pdf_path = os.path.join(Config.OUTPUT_FOLDER, pdf_filename)
                        
                        try:
                            print(f"📄 Converting to PDF for preview...")
                            from docx2pdf import convert
                            convert(docx_path, pdf_path)
                            print(f"✅ PDF preview created: {pdf_filename}")
                        except Exception as e:
                            print(f"⚠️  PDF conversion failed: {e}")
                            # Continue anyway - DOCX is still available
                        
                        # Return DOCX filename for download, PDF for preview
                        formatted_files.append({
                            'filename': docx_filename,
                            'original': filename,
                            'name': resume_data['name'],
                            'pdf': pdf_filename if os.path.exists(pdf_path) else None
                        })
                        print(f"✅ Successfully formatted: {filename} → {docx_filename}\n")
                    else:
                        print(f"⚠️  Formatting completed but output file not found\n")
                else:
                    print(f"❌ Failed to format: {filename}\n")
            else:
                print(f"❌ Failed to parse resume: {filename}\n")
            
            # Cleanup
            try:
                os.remove(file_path)
            except:
                pass
        
        print(f"{'='*70}")
        print(f"✅ FORMATTING COMPLETE: {len(formatted_files)}/{len(files)} successful")
        print(f"{'='*70}\n")
        
        return jsonify({
            'success': True,
            'files': formatted_files,
            'message': f'Formatted {len(formatted_files)} resume(s)'
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download formatted resume"""
    return send_from_directory(Config.OUTPUT_FOLDER, filename, as_attachment=True)

@app.route('/api/preview/<filename>')
def preview_file(filename):
    """Convert DOCX to HTML for fast preview - no PDF needed"""
    try:
        # Security: validate filename
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'success': False, 'error': 'Invalid filename'}), 400
        
        # Handle both .docx and .pdf requests (convert .pdf to .docx)
        if filename.endswith('.pdf'):
            filename = filename.replace('.pdf', '.docx')
        
        # Look for DOCX file in output directory
        docx_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        
        if not os.path.exists(docx_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Convert DOCX to HTML using mammoth (fast!)
        try:
            import mammoth
        except ImportError:
            return jsonify({
                'success': False, 
                'error': 'mammoth library not installed. Run: pip install mammoth'
            }), 500
        
        print(f"📄 Converting DOCX to HTML preview: {filename}")
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html_body = result.value
        
        # Wrap HTML with proper styling for resume display
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            max-width: 850px;
            margin: 20px auto;
            padding: 20px;
            background: white;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        td, th {{
            border: 1px solid #333;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        h1, h2, h3 {{
            color: #333;
            margin-top: 15px;
            margin-bottom: 10px;
        }}
        ul, ol {{
            margin-left: 20px;
        }}
        p {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
        
        print(f"✅ HTML preview generated ({len(html_content)} chars)")
        return jsonify({
            'success': True,
            'html': html_content,
            'filename': filename
        })
        
    except Exception as e:
        print(f"❌ Preview error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/templates/<template_id>/thumbnail')
def get_template_thumbnail(template_id):
    """Generate and return template thumbnail image with caching"""
    try:
        template = db.get_template(template_id)
        if not template:
            return jsonify({'success': False, 'message': 'Template not found'}), 404
        
        file_path = os.path.join(Config.TEMPLATE_FOLDER, template['filename'])
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'Template file not found'}), 404
        
        # Generate thumbnail (convert first page to image)
        thumbnail_filename = f"{template_id}_thumb.png"
        thumbnail_path = os.path.join(Config.OUTPUT_FOLDER, thumbnail_filename)
        
        # Check if thumbnail already exists
        if not os.path.exists(thumbnail_path):
            try:
                import pythoncom
                from docx2pdf import convert
                import fitz  # PyMuPDF for PDF to image conversion
                from PIL import Image
                
                # Convert DOCX to PDF first
                temp_pdf = os.path.join(Config.OUTPUT_FOLDER, f"{template_id}_temp.pdf")
                
                pythoncom.CoInitialize()
                try:
                    convert(file_path, temp_pdf)
                finally:
                    pythoncom.CoUninitialize()
                
                # Convert first page of PDF to image
                if os.path.exists(temp_pdf):
                    pdf_document = fitz.open(temp_pdf)
                    first_page = pdf_document[0]
                    # Render at 120 DPI for faster loading (reduced from 150)
                    pix = first_page.get_pixmap(matrix=fitz.Matrix(120/72, 120/72))
                    
                    # Save as PNG first
                    temp_png = thumbnail_path.replace('.png', '_temp.png')
                    pix.save(temp_png)
                    pdf_document.close()
                    
                    # Optimize with PIL for smaller file size
                    img = Image.open(temp_png)
                    img.save(thumbnail_path, 'PNG', optimize=True, quality=85)
                    
                    # Clean up temp files
                    os.remove(temp_pdf)
                    os.remove(temp_png)
                else:
                    return jsonify({'success': False, 'message': 'PDF conversion failed'}), 500
                    
            except Exception as e:
                print(f"⚠️  Thumbnail generation failed: {e}")
                traceback.print_exc()
                return jsonify({'success': False, 'message': f'Thumbnail generation failed: {str(e)}'}), 500
        
        # Return the thumbnail image with aggressive caching
        response = send_from_directory(Config.OUTPUT_FOLDER, thumbnail_filename, mimetype='image/png')
        response.headers['Cache-Control'] = 'public, max-age=86400, immutable'  # Cache for 24 hours
        response.headers['ETag'] = template_id  # Use template ID as ETag
        return response
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete template"""
    try:
        template = db.get_template(template_id)
        if template:
            file_path = os.path.join(Config.TEMPLATE_FOLDER, template['filename'])
            if os.path.exists(file_path):
                os.remove(file_path)
            db.delete_template(template_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎯 RESUME FORMATTER - BACKEND SERVER")
    print("="*70)
    print("✅ API running on http://127.0.0.1:5000")
    print("✅ React frontend: http://localhost:3000")
    print("="*70 + "\n")
    app.run(debug=True, port=5000)
