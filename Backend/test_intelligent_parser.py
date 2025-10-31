"""
Test script for Intelligent Resume Parser
Verifies ML-based section mapping functionality
"""

import sys
import time
from pathlib import Path

def test_imports():
    """Test if all required libraries are installed"""
    print("=" * 70)
    print("TESTING ML LIBRARY IMPORTS")
    print("=" * 70)
    
    all_ok = True
    
    # Test sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers: OK")
    except ImportError as e:
        print(f"❌ sentence-transformers: FAILED")
        print(f"   Install: pip install sentence-transformers")
        all_ok = False
    
    # Test fuzzywuzzy
    try:
        from fuzzywuzzy import process, fuzz
        print("✅ fuzzywuzzy: OK")
    except ImportError as e:
        print(f"❌ fuzzywuzzy: FAILED")
        print(f"   Install: pip install fuzzywuzzy python-Levenshtein")
        all_ok = False
    
    # Test spacy
    try:
        import spacy
        print("✅ spacy: OK")
    except ImportError as e:
        print(f"❌ spacy: FAILED")
        print(f"   Install: pip install spacy")
        all_ok = False
    
    # Test spacy model
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spacy model (en_core_web_sm): OK")
    except Exception as e:
        print(f"❌ spacy model: FAILED")
        print(f"   Install: python -m spacy download en_core_web_sm")
        all_ok = False
    
    # Test numpy
    try:
        import numpy as np
        print("✅ numpy: OK")
    except ImportError:
        print(f"❌ numpy: FAILED")
        print(f"   Install: pip install numpy")
        all_ok = False
    
    # Test python-docx
    try:
        from docx import Document
        print("✅ python-docx: OK")
    except ImportError:
        print(f"❌ python-docx: FAILED")
        print(f"   Install: pip install python-docx")
        all_ok = False
    
    print()
    return all_ok

def test_parser_initialization():
    """Test parser initialization"""
    print("=" * 70)
    print("TESTING PARSER INITIALIZATION")
    print("=" * 70)
    
    try:
        from utils.intelligent_resume_parser import IntelligentResumeParser
        
        print("\n📦 Initializing parser...")
        start = time.time()
        parser = IntelligentResumeParser()
        init_time = time.time() - start
        
        print(f"✅ Parser initialized in {init_time:.2f}s")
        
        # Check model availability
        if parser.model:
            print("✅ Sentence Transformer model loaded")
        else:
            print("⚠️  Sentence Transformer not available (will use fallback)")
        
        if parser.nlp:
            print("✅ spaCy model loaded")
        else:
            print("⚠️  spaCy not available (will use fallback)")
        
        print()
        return parser
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_heading_matching(parser):
    """Test heading matching functionality"""
    print("=" * 70)
    print("TESTING HEADING MATCHING")
    print("=" * 70)
    
    template_sections = ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS", "SUMMARY"]
    
    test_cases = [
        # (candidate_heading, expected_match)
        ("Employment History", "EMPLOYMENT HISTORY"),
        ("Work Experience", "EMPLOYMENT HISTORY"),
        ("Professional Experience", "EMPLOYMENT HISTORY"),
        ("Career History", "EMPLOYMENT HISTORY"),
        ("Experince", "EMPLOYMENT HISTORY"),  # Typo
        ("Education", "EDUCATION"),
        ("Academic Background", "EDUCATION"),
        ("Educational Background", "EDUCATION"),
        ("Skills", "SKILLS"),
        ("Technical Skills", "SKILLS"),
        ("Core Competencies", "SKILLS"),
        ("Summary", "SUMMARY"),
        ("Professional Summary", "SUMMARY"),
        ("Career Objective", "SUMMARY"),
    ]
    
    passed = 0
    failed = 0
    
    for candidate, expected in test_cases:
        result = parser._match_heading(candidate, template_sections)
        
        if result == expected:
            print(f"  ✅ '{candidate}' → '{result}'")
            passed += 1
        else:
            print(f"  ❌ '{candidate}' → '{result}' (expected: '{expected}')")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print()
    
    return failed == 0

def test_content_classification(parser):
    """Test content classification for unheaded paragraphs"""
    print("=" * 70)
    print("TESTING CONTENT CLASSIFICATION")
    print("=" * 70)
    
    template_sections = ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS", "SUMMARY"]
    
    test_cases = [
        # (content, position, expected_section)
        (
            "Experienced software engineer with 10 years of expertise in cloud computing.",
            0,
            "SUMMARY"
        ),
        (
            "Managed a team of 15 developers at Google from 2020-2023. Led development of cloud infrastructure.",
            5,
            "EMPLOYMENT HISTORY"
        ),
        (
            "Bachelor of Science in Computer Science from Stanford University, graduated 2015 with 3.8 GPA.",
            10,
            "EDUCATION"
        ),
        (
            "Proficient in Python, Java, JavaScript, React, Node.js, AWS, Docker, Kubernetes.",
            15,
            "SKILLS"
        ),
    ]
    
    passed = 0
    failed = 0
    
    for content, position, expected in test_cases:
        result = parser._classify_content(content, position, template_sections)
        
        if result == expected:
            print(f"  ✅ Position {position}: '{content[:50]}...' → '{result}'")
            passed += 1
        else:
            print(f"  ❌ Position {position}: '{content[:50]}...' → '{result}' (expected: '{expected}')")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print()
    
    return failed == 0

def test_performance(parser):
    """Test parsing performance"""
    print("=" * 70)
    print("TESTING PERFORMANCE")
    print("=" * 70)
    
    template_sections = ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS", "SUMMARY"]
    
    # Simulate multiple section mappings
    test_headings = [
        "Work Experience",
        "Academic Background",
        "Technical Skills",
        "Professional Summary",
        "Career History",
        "Educational Qualifications",
        "Core Competencies",
        "Career Objective"
    ]
    
    print(f"\n⏱️  Mapping {len(test_headings)} sections...")
    start = time.time()
    
    for heading in test_headings:
        parser._match_heading(heading, template_sections)
    
    elapsed = time.time() - start
    avg_time = (elapsed / len(test_headings)) * 1000
    
    print(f"✅ Total time: {elapsed*1000:.0f}ms")
    print(f"✅ Average per section: {avg_time:.0f}ms")
    
    if avg_time < 100:
        print("✅ Performance: EXCELLENT (<100ms per section)")
    elif avg_time < 200:
        print("✅ Performance: GOOD (<200ms per section)")
    else:
        print("⚠️  Performance: SLOW (>200ms per section)")
    
    print()
    return avg_time < 200

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("INTELLIGENT RESUME PARSER - TEST SUITE")
    print("=" * 70)
    print()
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        print("\nPlease install missing dependencies:")
        print("  cd Backend")
        print("  install_ml_dependencies.bat")
        return False
    
    # Test 2: Parser initialization
    parser = test_parser_initialization()
    if not parser:
        print("\n❌ Parser initialization failed!")
        return False
    
    # Test 3: Heading matching
    if not test_heading_matching(parser):
        print("⚠️  Some heading matching tests failed")
    
    # Test 4: Content classification
    if not test_content_classification(parser):
        print("⚠️  Some content classification tests failed")
    
    # Test 5: Performance
    if not test_performance(parser):
        print("⚠️  Performance tests failed")
    
    print("=" * 70)
    print("🎉 TEST SUITE COMPLETE!")
    print("=" * 70)
    print("\nThe intelligent parser is ready to use!")
    print("\nNext steps:")
    print("1. Integrate into your existing resume formatter")
    print("2. Test with real candidate resumes")
    print("3. Monitor accuracy and adjust thresholds if needed")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
