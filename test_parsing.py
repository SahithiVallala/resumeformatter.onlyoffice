"""
Test resume parsing and formatting with your sample data
"""
import sys
sys.path.insert(0, 'Backend')

from utils.advanced_resume_parser import parse_resume
import json

# Create a test resume text file with your sample (exactly as shown in your output)
test_resume = """
John Doe
john@email.com
555-123-4567

Employment History
• Information Technology Technician I Aug 2007 to Current
• Company Name ï¼ City , State
• Migrating and managing user accounts in Microsoft Office 365 and Exchange Online.
• Creating and managing virtual machines for systems such as domain controllers and Active Directory Federation Services (ADFS) in Microsoft Windows Azure (IaaS).
• Creating and managing storage in Microsoft Windows Azure (IaaS).
• Installing and configuring StorSimple iSCSI cloud array (STaaS/BaaS).

Education
• Bachelor of Science , Information Technology 2005
Florida International Univeristy ï¼ City , State , United States
• Coursework in Programming, Web Administration, Network Administration, Database Administration, and Systems Administration â€" Linux
• Programming Languages: C++, Java, JSP, HTML, CSS, VB.Net, Bash, T-SQL
"""

# Save to temp file
with open('C:\\Users\\valla\\Desktop\\Resume formatter\\temp_test_resume.txt', 'w', encoding='utf-8') as f:
    f.write(test_resume)

# Parse it
print("="*70)
print("PARSING TEST RESUME")
print("="*70)
result = parse_resume('C:\\Users\\valla\\Desktop\\Resume formatter\\temp_test_resume.txt', 'txt')

print("\n" + "="*70)
print("PARSING RESULTS")
print("="*70)

print(f"\nName: {result.get('name')}")
print(f"Email: {result.get('email')}")
print(f"Phone: {result.get('phone')}")

print(f"\n🔹 EXPERIENCE ({len(result.get('experience', []))} entries):")
for idx, exp in enumerate(result.get('experience', []), 1):
    print(f"\n  Entry {idx}:")
    print(f"    Company: {exp.get('company')}")
    print(f"    Role: {exp.get('role')}")
    print(f"    Duration: {exp.get('duration')}")
    print(f"    Details: {len(exp.get('details', []))} items")
    if exp.get('details'):
        for d in exp.get('details')[:3]:
            print(f"      - {d[:80]}...")

print(f"\n🔹 EDUCATION ({len(result.get('education', []))} entries):")
for idx, edu in enumerate(result.get('education', []), 1):
    print(f"\n  Entry {idx}:")
    print(f"    Degree: {edu.get('degree')}")
    print(f"    Institution: {edu.get('institution')}")
    print(f"    Year: {edu.get('year')}")

print("\n" + "="*70)
print("EXPECTED OUTPUT FORMAT")
print("="*70)
print("\nEMPLOYMENT HISTORY")
for exp in result.get('experience', []):
    company = exp.get('company', '').upper()
    role = exp.get('role', '').upper()
    duration = exp.get('duration', '')
    print(f"{company} – {role}                    {duration}")
    for detail in exp.get('details', [])[:3]:
        print(f"  • {detail}")

print("\nEDUCATION")
for edu in result.get('education', []):
    degree = edu.get('degree', '').upper()
    institution = edu.get('institution', '').upper()
    year = edu.get('year', '')
    print(f"{degree}  {institution}                    {year}")
