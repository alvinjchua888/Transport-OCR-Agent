"""
Simple test suite for Transport OCR Agent
Tests basic functionality without requiring actual API keys
"""

import os
import sys
from unittest.mock import Mock, patch
import io
from PIL import Image

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import streamlit as st
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        from dotenv import load_dotenv
        import utils
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    try:
        import utils
        
        # Test validate_api_key
        assert utils.validate_api_key("sk-1234567890abcdef") == True
        assert utils.validate_api_key("") == False
        assert utils.validate_api_key("short") == False
        print("✓ validate_api_key works")
        
        # Test get_supported_file_types
        file_types = utils.get_supported_file_types()
        assert isinstance(file_types, list)
        assert "png" in file_types
        assert "jpg" in file_types
        print("✓ get_supported_file_types works")
        
        # Test get_document_type_fields
        invoice_fields = utils.get_document_type_fields("Invoice")
        assert isinstance(invoice_fields, list)
        assert "Invoice Number" in invoice_fields
        print("✓ get_document_type_fields works")
        
        # Test format_extracted_data
        formatted = utils.format_extracted_data("Test data")
        assert "Test data" in formatted
        assert "Extraction Timestamp" in formatted
        print("✓ format_extracted_data works")
        
        # Test create_summary_stats
        stats = utils.create_summary_stats("Hello world test")
        assert stats["status"] == "Success"
        assert stats["character_count"] > 0
        print("✓ create_summary_stats works")
        
        print("✓ All utility functions tests passed")
        return True
    except AssertionError as e:
        print(f"✗ Assertion error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing utils: {e}")
        return False


def test_prompt_generation():
    """Test prompt generation for different document types."""
    print("\nTesting prompt generation...")
    try:
        # Mock the app module
        import app
        
        # Test different document types
        doc_types = ["Invoice", "Receipt", "Email", "General Document"]
        for doc_type in doc_types:
            prompt = app.create_extraction_prompt(doc_type)
            assert isinstance(prompt, str), f"Prompt for {doc_type} is not a string"
            assert len(prompt) > 0, f"Prompt for {doc_type} is empty"
            # Check that the document type or relevant keywords are in the prompt
            assert doc_type in prompt or "document" in prompt.lower(), f"Document type {doc_type} not found in prompt"
            print(f"✓ Prompt generated for {doc_type}")
        
        print("✓ All prompt generation tests passed")
        return True
    except AssertionError as e:
        print(f"✗ Assertion error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing prompt generation: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_handling():
    """Test basic image handling."""
    print("\nTesting image handling...")
    try:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Test that we can load it back
        test_img = Image.open(io.BytesIO(img_bytes))
        assert test_img.size == (100, 100)
        print("✓ Image creation and loading works")
        
        # Test conversion to RGB
        img_rgba = Image.new('RGBA', (50, 50), color='blue')
        img_rgb = img_rgba.convert('RGB')
        assert img_rgb.mode == 'RGB'
        print("✓ Image mode conversion works")
        
        print("✓ All image handling tests passed")
        return True
    except Exception as e:
        print(f"✗ Error testing image handling: {e}")
        return False


def test_environment_setup():
    """Test environment configuration."""
    print("\nTesting environment setup...")
    try:
        # Check if .env.example exists
        assert os.path.exists('.env.example'), ".env.example file not found"
        print("✓ .env.example file exists")
        
        # Check if requirements.txt exists
        assert os.path.exists('requirements.txt'), "requirements.txt file not found"
        print("✓ requirements.txt file exists")
        
        # Check if README.md has content
        assert os.path.exists('README.md'), "README.md file not found"
        with open('README.md', 'r') as f:
            readme_content = f.read()
            assert len(readme_content) > 100, "README.md seems empty"
            assert "OCR" in readme_content, "README.md doesn't mention OCR"
        print("✓ README.md exists and has content")
        
        print("✓ All environment setup tests passed")
        return True
    except AssertionError as e:
        print(f"✗ Assertion error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing environment: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Transport OCR Agent - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_utils,
        test_prompt_generation,
        test_image_handling,
        test_environment_setup
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed! The app is ready to use.")
        print("\nTo run the app, execute:")
        print("  streamlit run app.py")
        print("\nMake sure to set up your .env file with API keys first!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
