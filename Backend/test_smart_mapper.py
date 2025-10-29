"""
Test script for Smart Section Mapper
Run this to verify the ML dependencies are installed correctly
"""

import sys
import time

def test_imports():
    """Test if all required libraries are installed"""
    print("=" * 60)
    print("Testing ML Library Imports")
    print("=" * 60)
    
    # Test sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers: OK")
    except ImportError as e:
        print(f"❌ sentence-transformers: FAILED - {e}")
        print("   Install: pip install sentence-transformers")
        return False
    
    # Test fuzzywuzzy
    try:
        from fuzzywuzzy import process, fuzz
        print("✅ fuzzywuzzy: OK")
    except ImportError as e:
        print(f"❌ fuzzywuzzy: FAILED - {e}")
        print("   Install: pip install fuzzywuzzy python-Levenshtein")
        return False
    
    # Test spacy
    try:
        import spacy
        print("✅ spacy: OK")
    except ImportError as e:
        print(f"❌ spacy: FAILED - {e}")
        print("   Install: pip install spacy")
        return False
    
    # Test spacy model
    try:
        nlp = spacy.load("en_core_web_sm")
        print("✅ spacy model (en_core_web_sm): OK")
    except Exception as e:
        print(f"❌ spacy model: FAILED - {e}")
        print("   Install: python -m spacy download en_core_web_sm")
        return False
    
    print()
    return True

def test_mapper():
    """Test the smart section mapper"""
    print("=" * 60)
    print("Testing Smart Section Mapper")
    print("=" * 60)
    
    try:
        from utils.smart_section_mapper import get_section_mapper
        
        # Initialize mapper
        print("\n📦 Loading mapper...")
        start = time.time()
        mapper = get_section_mapper()
        load_time = time.time() - start
        print(f"✅ Mapper loaded in {load_time:.2f}s")
        
        # Test 1: Exact match
        print("\n" + "=" * 60)
        print("Test 1: Exact Match")
        print("=" * 60)
        result = mapper.map_section(
            "Employment History",
            ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS"]
        )
        print(f"Input: 'Employment History'")
        print(f"Output: '{result}'")
        assert result == "EMPLOYMENT HISTORY", "Exact match failed!"
        print("✅ PASSED")
        
        # Test 2: Synonym matching
        print("\n" + "=" * 60)
        print("Test 2: Synonym Matching")
        print("=" * 60)
        result = mapper.map_section(
            "Work Experience",
            ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS"]
        )
        print(f"Input: 'Work Experience'")
        print(f"Output: '{result}'")
        assert result == "EMPLOYMENT HISTORY", "Synonym match failed!"
        print("✅ PASSED")
        
        # Test 3: Typo correction
        print("\n" + "=" * 60)
        print("Test 3: Typo Correction")
        print("=" * 60)
        result = mapper.map_section(
            "Experince",
            ["EXPERIENCE", "EDUCATION", "SKILLS"]
        )
        print(f"Input: 'Experince' (typo)")
        print(f"Output: '{result}'")
        assert result == "EXPERIENCE", "Typo correction failed!"
        print("✅ PASSED")
        
        # Test 4: Semantic similarity
        print("\n" + "=" * 60)
        print("Test 4: Semantic Similarity")
        print("=" * 60)
        result = mapper.map_section(
            "Professional Background",
            ["EMPLOYMENT HISTORY", "EDUCATION", "SKILLS"]
        )
        print(f"Input: 'Professional Background'")
        print(f"Output: '{result}'")
        assert result == "EMPLOYMENT HISTORY", "Semantic match failed!"
        print("✅ PASSED")
        
        # Test 5: Content classification
        print("\n" + "=" * 60)
        print("Test 5: Content Classification (Unheaded)")
        print("=" * 60)
        text = "Managed a team of 10 developers at Google from 2020-2023. Led development of cloud infrastructure."
        result = mapper.classify_unheaded_content(text, position_index=5)
        print(f"Input: '{text[:60]}...'")
        print(f"Output: '{result}'")
        assert result == "EMPLOYMENT", "Content classification failed!"
        print("✅ PASSED")
        
        # Test 6: Batch mapping
        print("\n" + "=" * 60)
        print("Test 6: Batch Mapping")
        print("=" * 60)
        candidate_sections = {
            "Career Summary": "Experienced professional with 10 years...",
            "Work History": "Company A - 2020-2023...",
            "Academic Background": "University of XYZ..."
        }
        template_sections = ["SUMMARY", "EMPLOYMENT", "EDUCATION", "SKILLS"]
        
        start = time.time()
        mapped = mapper.batch_map_sections(candidate_sections, template_sections)
        batch_time = time.time() - start
        
        print(f"Input sections: {list(candidate_sections.keys())}")
        print(f"Mapped sections: {list(mapped.keys())}")
        print(f"Processing time: {batch_time*1000:.0f}ms")
        
        assert "SUMMARY" in mapped, "Summary not mapped!"
        assert "EMPLOYMENT" in mapped, "Employment not mapped!"
        assert "EDUCATION" in mapped, "Education not mapped!"
        print("✅ PASSED")
        
        # Performance summary
        print("\n" + "=" * 60)
        print("Performance Summary")
        print("=" * 60)
        print(f"Model load time: {load_time:.2f}s (one-time)")
        print(f"Batch mapping time: {batch_time*1000:.0f}ms (3 sections)")
        print(f"Average per section: {(batch_time/3)*1000:.0f}ms")
        
        if batch_time < 0.5:
            print("✅ Performance: EXCELLENT (<500ms)")
        elif batch_time < 1.0:
            print("✅ Performance: GOOD (<1s)")
        else:
            print("⚠️  Performance: SLOW (>1s) - may need optimization")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe smart section mapper is working correctly!")
        print("You can now integrate it into your resume parser.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SMART SECTION MAPPER - TEST SUITE")
    print("=" * 60)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        print("\nPlease run: install_ml_dependencies.bat")
        return False
    
    # Test mapper
    if not test_mapper():
        print("\n❌ Mapper tests failed!")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Integrate mapper into resume_parser.py")
    print("2. Test with real resumes")
    print("3. Monitor accuracy and adjust thresholds if needed")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
