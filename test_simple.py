import sys
sys.path.insert(0, 'Backend')
from utils.advanced_resume_parser import parse_resume

# Test resume
test = """
Employment History
Information Technology Technician I Aug 2007 to Current
Company Name - City , State
Migrating and managing user accounts in Microsoft Office 365
Creating and managing virtual machines

Education
Bachelor of Science , Information Technology 2005
Florida International University - City , State
Coursework in Programming
"""

with open('temp_test.txt', 'w', encoding='utf-8') as f:
    f.write(test)

result = parse_resume('temp_test.txt', 'txt')

print("\n=== EXPERIENCE ===")
for exp in result.get('experience', []):
    print(f"Company: {exp.get('company')}")
    print(f"Role: {exp.get('role')}")
    print(f"Duration: {exp.get('duration')}")
    print(f"Details: {len(exp.get('details', []))}")
    print()

print("\n=== EDUCATION ===")
for edu in result.get('education', []):
    print(f"Degree: {edu.get('degree')}")
    print(f"Institution: {edu.get('institution')}")
    print(f"Year: {edu.get('year')}")
    print()
