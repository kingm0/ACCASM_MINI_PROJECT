#!/usr/bin/env python3
"""
Test script to verify the Gemini AI integration setup
"""

import os
import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not found. Install with: pip install flask")
        return False
    
    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image imported successfully")
    except ImportError:
        print("❌ pdf2image not found. Install with: pip install pdf2image")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError:
        print("❌ Pillow not found. Install with: pip install Pillow")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ google-generativeai imported successfully")
    except ImportError:
        print("❌ google-generativeai not found. Install with: pip install google-generativeai")
        return False
    
    return True

def test_api_key():
    """Test if Gemini API key is configured"""
    print("\nTesting API key configuration...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and api_key != 'YOUR_GEMINI_API_KEY_HERE':
        print("✅ GEMINI_API_KEY environment variable is set")
        return True
    else:
        print("❌ GEMINI_API_KEY not found or not configured")
        print("   Set it with: export GEMINI_API_KEY='your-api-key-here'")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'gemini_integration.py',
        'templates/use.html',
        'templates/loading.html',
        'templates/gemini_result.html',
        'requirements_gemini.txt'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Gemini AI Integration Setup Test")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("API Key Configuration", test_api_key)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    print("\n📊 Test Results Summary")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Set your Gemini API key: export GEMINI_API_KEY='your-key'")
        print("2. Run the application: python app.py")
        print("3. Visit http://localhost:5001/use to test the new features")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nFor help, see GEMINI_SETUP.md")

if __name__ == "__main__":
    main()
