"""Quick test to see if classifier loads"""
try:
    from utils.enhanced_section_classifier import get_section_classifier
    print("✅ Classifier module loaded successfully")
    
    classifier = get_section_classifier(confidence_threshold=0.6)
    print("✅ Classifier initialized successfully")
    
    # Test basic classification
    result, conf = classifier.classify_by_heading("Work Experience", ["EMPLOYMENT HISTORY", "EDUCATION"])
    print(f"✅ Classification test: 'Work Experience' → '{result}' (confidence: {conf:.2f})")
    
    print("\n🎉 Classifier is working in fallback mode!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
