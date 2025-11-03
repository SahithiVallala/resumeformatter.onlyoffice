"""Test if word formatter is available"""
try:
    from utils.word_formatter import format_word_document
    print("✅ Word formatter imported successfully")
except Exception as e:
    print(f"❌ Word formatter import failed: {e}")
    import traceback
    traceback.print_exc()
