"""
Test Integration of Enhanced Section Classifier with Main Application
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*70)
    print("TEST: Module Imports")
    print("="*70)
    
    try:
        from utils.enhanced_section_classifier import get_section_classifier
        print("  ✓ Enhanced section classifier imported")
    except ImportError as e:
        print(f"  ✗ Enhanced section classifier import failed: {e}")
        return False
    
    try:
        from utils.ordered_section_renderer import OrderedSectionRenderer
        print("  ✓ Ordered section renderer imported")
    except ImportError as e:
        print(f"  ✗ Ordered section renderer import failed: {e}")
        return False
    
    try:
        from utils.resume_section_integration import format_resume_with_intelligent_mapping
        print("  ✓ Resume section integration imported")
    except ImportError as e:
        print(f"  ✗ Resume section integration import failed: {e}")
        return False
    
    try:
        from utils.enhanced_formatter_integration import format_resume_intelligent
        print("  ✓ Enhanced formatter integration imported")
    except ImportError as e:
        print(f"  ✗ Enhanced formatter integration import failed: {e}")
        return False
    
    print("\n  ✅ All modules imported successfully")
    return True


def test_formatter_integration():
    """Test that the formatter integration works"""
    print("\n" + "="*70)
    print("TEST: Formatter Integration")
    print("="*70)
    
    try:
        from utils.enhanced_formatter_integration import enhance_resume_data_with_intelligent_mapping
        
        # Mock resume data
        resume_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1-234-567-8900',
            'summary': 'Experienced software engineer with 5 years of expertise.',
            'experience': [
                {
                    'role': 'Software Engineer',
                    'company': 'Google',
                    'duration': '2020-2024',
                    'responsibilities': 'Developed microservices using Python and AWS.'
                }
            ],
            'education': [
                {
                    'degree': 'B.Tech in Computer Science',
                    'institution': 'JNTUH',
                    'year': '2020'
                }
            ],
            'skills': ['Python', 'Java', 'AWS', 'React'],
            'sections': {
                'Professional Profile': 'Experienced engineer...',
                'Work Experience': 'Software Engineer at Google...'
            }
        }
        
        # Mock template analysis
        template_analysis = {
            'sections': ['SUMMARY', 'EMPLOYMENT HISTORY', 'EDUCATION', 'SKILLS'],
            'template_path': 'template.docx',
            'template_type': 'docx'
        }
        
        print("  📝 Testing with mock data...")
        enhanced_data = enhance_resume_data_with_intelligent_mapping(
            resume_data, 
            template_analysis,
            confidence_threshold=0.6
        )
        
        if enhanced_data:
            print("  ✓ Enhancement completed")
            if 'sections' in enhanced_data:
                print(f"  ✓ Sections found: {len(enhanced_data['sections'])}")
            print("\n  ✅ Formatter integration test passed")
            return True
        else:
            print("  ✗ Enhancement returned None")
            return False
            
    except Exception as e:
        print(f"  ✗ Formatter integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_integration():
    """Test that app.py can import the enhanced formatter"""
    print("\n" + "="*70)
    print("TEST: App Integration")
    print("="*70)
    
    try:
        # Simulate app.py import
        try:
            from utils.enhanced_formatter_integration import format_resume_intelligent
            print("  ✓ Enhanced formatter imported (app.py will use enhanced version)")
        except ImportError:
            from utils.intelligent_formatter import format_resume_intelligent
            print("  ⚠️  Fallback to standard formatter (enhanced not available)")
        
        print("  ✓ App can import formatter")
        print("\n  ✅ App integration test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ App integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_classifier_availability():
    """Test classifier availability and configuration"""
    print("\n" + "="*70)
    print("TEST: Classifier Availability")
    print("="*70)
    
    try:
        from utils.enhanced_section_classifier import get_section_classifier
        
        classifier = get_section_classifier(confidence_threshold=0.6)
        
        if classifier:
            print("  ✓ Classifier initialized")
            
            # Test normalization
            result = classifier.normalize_section_name("Professional Profile")
            if result:
                print(f"  ✓ Normalization works: 'Professional Profile' → '{result}'")
            
            # Test classification
            matched, conf = classifier.classify_by_heading(
                "Work Experience",
                ["SUMMARY", "EMPLOYMENT HISTORY", "EDUCATION"]
            )
            if matched:
                print(f"  ✓ Classification works: 'Work Experience' → '{matched}' (conf: {conf:.2f})")
            
            print("\n  ✅ Classifier availability test passed")
            return True
        else:
            print("  ✗ Classifier initialization failed")
            return False
            
    except Exception as e:
        print(f"  ✗ Classifier availability test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_integration_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("🧪 INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("Module Imports", test_imports),
        ("Formatter Integration", test_formatter_integration),
        ("App Integration", test_app_integration),
        ("Classifier Availability", test_classifier_availability)
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
    print("📊 INTEGRATION TEST SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n  🎉 ALL INTEGRATION TESTS PASSED!")
        print("  ✅ Enhanced section classifier is integrated and ready to use")
        print("\n  Next steps:")
        print("    1. Restart your Flask application")
        print("    2. Upload a resume and template")
        print("    3. Check console for '🧠 INTELLIGENT SECTION MAPPING' messages")
    else:
        print("\n  ⚠️  Some tests failed. Please check the errors above.")
    
    print("="*70 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
