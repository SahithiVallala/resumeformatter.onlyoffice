"""Test classification with real resume sections"""

from utils.enhanced_section_classifier import get_section_classifier

# Simulate the sections from your resume
sections_to_classify = [
    {
        'heading': 'certifications',
        'content': '''Project Management Professional (PMP) | Project Management Institute
Certified SAFe® 6 Scrum Master | Scale Agile
Technical Competencies
Agile & Project Management Tools: Jira, Azure DevOps, Rally
Professional Profile
Microsoft |Atlanta, GA| Technical Project manager-contract 5/2024- 6/2025
Provided strategic program leadership for AI/ML product development, translating product vision into actionable execution plans.
Collaborated cross-functionally with product, QA, data, and AI/ML engineering teams to define program scope.
Established and maintained comprehensive program dashboards and reports.
Managed communications related to feature requirements, status updates, and key stakeholder requirements.
Developed and implemented project plans, timelines, to ensure timely and successful project delivery.
Demonstrated Strong experience using ADO to include ability to report progress using Epics, Features, Bugs, and Tasks.
Recognized and articulated risks to project timelines, including possible solutions to stakeholders.
EndTime Harvest Entertainment |Minneapolis, MN| Project manager - 4/2023- 4/2024
Ensured all campaign delivery projects for the Brand studio are well planned, documented and carried out.
Coordinated the preparation of the project budget and various cost, milestone, and management reports.
Provided a pro-active and day to day contract to the sales teams and clients regarding create campaign delivery.''',
        'position': 0
    },
    {
        'heading': 'skills',
        'content': '''Project & Program Management: Agile (Scrum, SAFe, Kanban)
Product Development & Operations: Digital Product Development
Technical Tools & Platforms: Jira, Azure DevOps, Rally''',
        'position': 1
    }
]

template_sections = ['SUMMARY', 'EMPLOYMENT HISTORY', 'EDUCATION', 'SKILLS', 'CERTIFICATIONS']

print("="*70)
print("🧪 TESTING REAL RESUME CLASSIFICATION")
print("="*70)

classifier = get_section_classifier(confidence_threshold=0.6)

print(f"\n📋 Template sections: {', '.join(template_sections)}")
print(f"📄 Candidate sections to classify: {len(sections_to_classify)}\n")

print("🔍 CLASSIFYING SECTIONS")
print("="*70)

for section in sections_to_classify:
    heading = section['heading']
    content_preview = section['content'][:100] + '...'
    
    print(f"\n📝 Section: '{heading}'")
    print(f"   Content: {content_preview}")
    
    # Try heading classification
    matched, conf = classifier.classify_by_heading(heading, template_sections)
    print(f"   Heading match: '{matched}' (confidence: {conf:.2f})")
    
    # Try content classification
    matched_content, conf_content = classifier.classify_by_content(section['content'], section['position'])
    print(f"   Content match: '{matched_content}' (confidence: {conf_content:.2f})")

print("\n" + "="*70)
print("📊 BATCH CLASSIFICATION")
print("="*70)

mapped = classifier.batch_classify(sections_to_classify, template_sections)

for template_section, content in mapped.items():
    if template_section != '_uncertain':
        print(f"\n✅ {template_section}:")
        print(f"   {content[:150]}...")

print("\n" + "="*70)
print("🎯 RESULT")
print("="*70)

if 'EMPLOYMENT HISTORY' in mapped:
    if 'Microsoft' in mapped['EMPLOYMENT HISTORY']:
        print("✅ SUCCESS: 'Professional Profile' correctly classified as EMPLOYMENT HISTORY!")
    else:
        print("❌ FAIL: Employment history not found in correct section")
else:
    print("❌ FAIL: EMPLOYMENT HISTORY section not created")

if 'CERTIFICATIONS' in mapped:
    if 'PMP' in mapped['CERTIFICATIONS']:
        print("✅ SUCCESS: Certifications correctly classified!")
    else:
        print("⚠️  WARNING: PMP not found in certifications")
else:
    print("⚠️  WARNING: CERTIFICATIONS section not created")
