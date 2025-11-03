"""
Test Suite for Enhanced Section Classification
Tests the new intelligent section mapping system
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.enhanced_section_classifier import EnhancedSectionClassifier, get_section_classifier


def test_section_normalization():
    """Test section name normalization"""
    print("\n" + "="*70)
    print("TEST 1: Section Name Normalization")
    print("="*70)
    
    classifier = EnhancedSectionClassifier()
    
    test_cases = [
        ("Professional Profile", "summary"),
        ("Work Experience", "employment history"),
        ("Academic Background", "education"),
        ("Technical Skills", "skills"),
        ("Certificates", "certifications"),
        ("Key Projects", "projects"),
        ("Awards and Honors", "awards"),
        ("Language Skills", "languages")
    ]
    
    passed = 0
    for input_name, expected in test_cases:
        result = classifier.normalize_section_name(input_name)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_name}' → '{result}' (expected: '{expected}')")
        if result == expected:
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_heading_classification():
    """Test heading-based classification"""
    print("\n" + "="*70)
    print("TEST 2: Heading-Based Classification")
    print("="*70)
    
    classifier = EnhancedSectionClassifier(confidence_threshold=0.6)
    
    template_sections = [
        "SUMMARY",
        "EMPLOYMENT HISTORY",
        "EDUCATION",
        "SKILLS",
        "CERTIFICATIONS",
        "PROJECTS"
    ]
    
    test_cases = [
        ("Professional Profile", "SUMMARY"),
        ("Work Experience", "EMPLOYMENT HISTORY"),
        ("Academic Background", "EDUCATION"),
        ("Technical Skills", "SKILLS"),
        ("Certificates", "CERTIFICATIONS"),
        ("Key Projects", "PROJECTS")
    ]
    
    passed = 0
    for heading, expected in test_cases:
        result, confidence = classifier.classify_by_heading(heading, template_sections)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{heading}' → '{result}' (confidence: {confidence:.2f})")
        if result == expected:
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_content_classification():
    """Test content-based classification"""
    print("\n" + "="*70)
    print("TEST 3: Content-Based Classification")
    print("="*70)
    
    classifier = EnhancedSectionClassifier(confidence_threshold=0.5)
    
    test_cases = [
        {
            "content": "Experienced software engineer with 5 years of expertise in Python and cloud technologies. Seeking challenging opportunities in backend development.",
            "expected": "summary",
            "position": 0
        },
        {
            "content": "Software Engineer at Google (2020-2024). Developed microservices using Python and AWS. Led a team of 5 engineers. Managed deployment pipelines.",
            "expected": "employment history",
            "position": 1
        },
        {
            "content": "Bachelor of Technology in Computer Science from JNTUH, graduated in 2020 with 8.5 GPA. Major in Software Engineering.",
            "expected": "education",
            "position": 2
        },
        {
            "content": "Proficient in Python, Java, JavaScript, React, AWS, Docker, Kubernetes. Expertise in microservices architecture.",
            "expected": "skills",
            "position": 3
        },
        {
            "content": "Certified AWS Solutions Architect. Azure Fundamentals Certificate. Cisco CCNA License.",
            "expected": "certifications",
            "position": 4
        }
    ]
    
    passed = 0
    for test_case in test_cases:
        result, confidence = classifier.classify_by_content(
            test_case["content"],
            test_case["position"]
        )
        status = "✓" if result == test_case["expected"] else "✗"
        print(f"  {status} Content → '{result}' (expected: '{test_case['expected']}', confidence: {confidence:.2f})")
        if result == test_case["expected"]:
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed >= len(test_cases) * 0.6  # Allow 60% pass rate for content classification


def test_full_classification():
    """Test full section classification pipeline"""
    print("\n" + "="*70)
    print("TEST 4: Full Classification Pipeline")
    print("="*70)
    
    classifier = EnhancedSectionClassifier(confidence_threshold=0.6)
    
    template_sections = [
        "SUMMARY",
        "EMPLOYMENT HISTORY",
        "EDUCATION",
        "SKILLS",
        "CERTIFICATIONS"
    ]
    
    test_sections = [
        {
            "heading": "Professional Profile",
            "content": "Experienced software engineer with 5 years of expertise.",
            "position": 0,
            "expected": "SUMMARY"
        },
        {
            "heading": "Work Experience",
            "content": "Software Engineer at Google (2020-2024).",
            "position": 1,
            "expected": "EMPLOYMENT HISTORY"
        },
        {
            "heading": None,
            "content": "Bachelor of Technology in Computer Science from JNTUH, graduated in 2020.",
            "position": 2,
            "expected": "EDUCATION"
        },
        {
            "heading": "Technical Competencies",
            "content": "Python, Java, AWS, React",
            "position": 3,
            "expected": "SKILLS"
        }
    ]
    
    passed = 0
    for test_section in test_sections:
        result = classifier.classify_section(
            test_section["heading"],
            test_section["content"],
            test_section["position"],
            template_sections
        )
        
        matched = result["matched_section"]
        confidence = result["confidence"]
        method = result["method"]
        
        status = "✓" if matched == test_section["expected"] else "✗"
        heading_display = test_section["heading"] or "[No heading]"
        print(f"  {status} '{heading_display}' → '{matched}' (method: {method}, confidence: {confidence:.2f})")
        
        if matched == test_section["expected"]:
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_sections)} tests passed")
    return passed >= len(test_sections) * 0.75  # Allow 75% pass rate


def test_batch_classification():
    """Test batch classification"""
    print("\n" + "="*70)
    print("TEST 5: Batch Classification")
    print("="*70)
    
    classifier = EnhancedSectionClassifier(confidence_threshold=0.6)
    
    template_sections = [
        "SUMMARY",
        "EMPLOYMENT HISTORY",
        "EDUCATION",
        "SKILLS"
    ]
    
    sections = [
        {
            "heading": "Professional Summary",
            "content": "Experienced engineer with 5 years of expertise.",
            "position": 0
        },
        {
            "heading": "Work History",
            "content": "Software Engineer at Google (2020-2024).",
            "position": 1
        },
        {
            "heading": "Academic Qualifications",
            "content": "B.Tech in Computer Science from JNTUH.",
            "position": 2
        },
        {
            "heading": "Core Competencies",
            "content": "Python, Java, AWS, React",
            "position": 3
        }
    ]
    
    mapped = classifier.batch_classify(sections, template_sections)
    
    print(f"\n  Mapped {len(mapped)} sections:")
    for section, content in mapped.items():
        print(f"    - {section}: {content[:50]}...")
    
    # Check if we got reasonable mappings
    success = len(mapped) >= 3 and '_uncertain' not in mapped
    status = "✓" if success else "✗"
    print(f"\n  {status} Batch classification {'passed' if success else 'failed'}")
    
    return success


def test_confidence_threshold():
    """Test confidence threshold handling"""
    print("\n" + "="*70)
    print("TEST 6: Confidence Threshold Handling")
    print("="*70)
    
    # Test with high threshold
    classifier_high = EnhancedSectionClassifier(confidence_threshold=0.9)
    
    # Test with ambiguous content
    ambiguous_content = "Some random text that doesn't clearly belong to any section."
    
    result, confidence = classifier_high.classify_by_content(ambiguous_content, 5)
    
    print(f"  Ambiguous content classification:")
    print(f"    Result: {result}")
    print(f"    Confidence: {confidence:.2f}")
    print(f"    Threshold: 0.9")
    
    if confidence < 0.9:
        print(f"  ✓ Correctly rejected low-confidence classification")
        return True
    else:
        print(f"  ✗ Should have rejected low-confidence classification")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 ENHANCED SECTION CLASSIFIER TEST SUITE")
    print("="*70)
    
    tests = [
        ("Section Normalization", test_section_normalization),
        ("Heading Classification", test_heading_classification),
        ("Content Classification", test_content_classification),
        ("Full Classification", test_full_classification),
        ("Batch Classification", test_batch_classification),
        ("Confidence Threshold", test_confidence_threshold)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n  ❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Overall: {passed_count}/{total_count} tests passed")
    print("="*70 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
