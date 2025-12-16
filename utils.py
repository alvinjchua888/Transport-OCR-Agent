"""
Utility functions for OCR Agent application
"""

import json
from typing import Dict, Any, List
from datetime import datetime


def format_extracted_data(raw_text: str) -> str:
    """
    Format extracted data for better readability.
    
    Args:
        raw_text: Raw text extracted from document
        
    Returns:
        Formatted text string
    """
    if not raw_text:
        return "No data extracted"
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"Extraction Timestamp: {timestamp}\n\n"
    formatted += "=" * 50 + "\n"
    formatted += raw_text
    formatted += "\n" + "=" * 50
    
    return formatted


def validate_api_key(api_key: str) -> bool:
    """
    Validate if API key is provided and has minimum length.
    
    Args:
        api_key: API key string
        
    Returns:
        Boolean indicating if key is valid
    """
    if not api_key or len(api_key.strip()) < 10:
        return False
    return True


def get_supported_file_types() -> List[str]:
    """
    Get list of supported file types.
    
    Returns:
        List of file extensions
    """
    return ["png", "jpg", "jpeg", "pdf", "bmp", "gif"]


def get_document_type_fields(doc_type: str) -> List[str]:
    """
    Get expected fields for a given document type.
    
    Args:
        doc_type: Type of document
        
    Returns:
        List of expected field names
    """
    fields = {
        "Invoice": [
            "Invoice Number",
            "Invoice Date",
            "Vendor Name",
            "Customer Name",
            "Line Items",
            "Subtotal",
            "Tax",
            "Total Amount"
        ],
        "Receipt": [
            "Store Name",
            "Receipt Number",
            "Date and Time",
            "Items Purchased",
            "Subtotal",
            "Tax",
            "Total Amount",
            "Payment Method"
        ],
        "Email": [
            "From",
            "To",
            "Date",
            "Subject",
            "Body Content",
            "Attachments"
        ],
        "General Document": [
            "Document Title",
            "Date",
            "Author/Sender",
            "Key Entities",
            "Summary"
        ]
    }
    
    return fields.get(doc_type, fields["General Document"])


def parse_model_name(provider: str, model: str) -> str:
    """
    Parse and validate model name for the given provider.
    
    Args:
        provider: AI provider name
        model: Model name
        
    Returns:
        Validated model name
    """
    openai_models = {
        "gpt-4-vision-preview": "gpt-4-vision-preview",
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini"
    }
    
    gemini_models = {
        "gemini-pro-vision": "gemini-pro-vision",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash"
    }
    
    if provider == "OpenAI":
        return openai_models.get(model, "gpt-4o")
    else:
        return gemini_models.get(model, "gemini-1.5-pro")


def create_summary_stats(extracted_text: str) -> Dict[str, Any]:
    """
    Create summary statistics from extracted text.
    
    Args:
        extracted_text: Extracted text content
        
    Returns:
        Dictionary with summary stats
    """
    if not extracted_text:
        return {"status": "No data"}
    
    stats = {
        "status": "Success",
        "character_count": len(extracted_text),
        "word_count": len(extracted_text.split()),
        "line_count": len(extracted_text.split('\n')),
        "timestamp": datetime.now().isoformat()
    }
    
    return stats
