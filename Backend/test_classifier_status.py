"""Test if enhanced classifier is available"""
print("="*70)
print("TESTING ENHANCED CLASSIFIER STATUS")
print("="*70)

try:
    from utils.enhanced_formatter_integration import ENHANCED_CLASSIFIER_AVAILABLE
    print(f"\n✅ Import successful")
    print(f"📊 ENHANCED_CLASSIFIER_AVAILABLE = {ENHANCED_CLASSIFIER_AVAILABLE}")
    
    if ENHANCED_CLASSIFIER_AVAILABLE:
        print("\n✅ Enhanced classifier IS available")
        print("   The formatter SHOULD use intelligent section mapping")
    else:
        print("\n❌ Enhanced classifier NOT available")
        print("   The formatter will use standard formatting")
        
    # Try to actually get the classifier
    try:
        from utils.enhanced_section_classifier import get_section_classifier
        classifier = get_section_classifier()
        print("\n✅ Classifier instance created successfully")
    except Exception as e:
        print(f"\n❌ Failed to create classifier: {e}")
        
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
