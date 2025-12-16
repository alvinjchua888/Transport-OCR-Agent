import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io
from pathlib import Path
import tempfile
from typing import Optional, Dict, Any

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="OCR Agent - Document Entity Extractor",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("📄 OCR Agent - Document Entity Extractor")
st.markdown("""
This app uses AI-powered OCR to extract entities from various document types including:
- **Invoices** 📝
- **Receipts** 🧾
- **Emails** 📧
- **Other documents** 📑

Upload your document and let the AI extract key information!
""")

# Sidebar for API selection and configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Provider selection
    api_provider = st.selectbox(
        "Select AI Provider",
        ["OpenAI", "Google Gemini"],
        help="Choose between OpenAI or Google Gemini for OCR and entity extraction"
    )
    
    # API Key input
    if api_provider == "OpenAI":
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key"
        )
        model_name = st.selectbox(
            "Model",
            ["gpt-4-vision-preview", "gpt-4o", "gpt-4o-mini"],
            help="Select the OpenAI model to use"
        )
    else:
        api_key = st.text_input(
            "Google API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", ""),
            help="Enter your Google API key"
        )
        model_name = st.selectbox(
            "Model",
            ["gemini-pro-vision", "gemini-1.5-pro", "gemini-1.5-flash"],
            help="Select the Gemini model to use"
        )
    
    # Document type selection
    doc_type = st.selectbox(
        "Document Type",
        ["Auto-detect", "Invoice", "Receipt", "Email", "General Document"],
        help="Select the type of document you're uploading"
    )
    
    st.markdown("---")
    st.markdown("""
    ### 📝 Instructions
    1. Select your AI provider
    2. Enter your API key
    3. Choose document type
    4. Upload your document
    5. Click 'Extract Entities'
    """)


def get_llm(provider: str, api_key: str, model: str):
    """Initialize the appropriate LLM based on provider."""
    if provider == "OpenAI":
        return ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            temperature=0
        )
    else:
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0
        )


def create_extraction_prompt(doc_type: str) -> str:
    """Create a prompt based on document type."""
    base_prompt = """You are an expert document analyzer. Extract all relevant entities from the provided document image.
    
Document Type: {doc_type}

Please extract and structure the following information:
"""
    
    if doc_type == "Invoice":
        specific_fields = """
- Invoice Number
- Invoice Date
- Due Date
- Vendor/Supplier Name
- Vendor Address
- Vendor Contact
- Customer/Buyer Name
- Customer Address
- Billing Address
- Shipping Address
- Line Items (with descriptions, quantities, unit prices, totals)
- Subtotal
- Tax Amount
- Tax Rate
- Discount (if any)
- Total Amount
- Payment Terms
- Currency
- Purchase Order Number (if any)
"""
    elif doc_type == "Receipt":
        specific_fields = """
- Store/Merchant Name
- Store Address
- Store Contact
- Receipt Number/Transaction ID
- Date and Time
- Cashier/Server Name (if any)
- Items Purchased (with quantities and prices)
- Subtotal
- Tax Amount
- Total Amount
- Payment Method
- Card Last 4 Digits (if applicable)
- Change Given (if any)
- Return Policy Information
"""
    elif doc_type == "Email":
        specific_fields = """
- From: Sender name and email address
- To: Recipient name(s) and email address(es)
- CC: Carbon copy recipients (if any)
- BCC: Blind carbon copy (if visible)
- Date and Time
- Subject Line
- Email Body Content
- Attachments Mentioned
- Signature Block
- Contact Information
- Any URLs or Links
- Action Items or Requests
- Key Dates or Deadlines
"""
    else:  # General Document or Auto-detect
        specific_fields = """
- Document Title/Type
- Document Date
- Sender/Author Information
- Recipient Information
- Key Entities (Names, Organizations, Locations)
- Important Dates
- Monetary Amounts
- Contact Information
- Reference Numbers
- Main Content Summary
- Action Items (if any)
"""
    
    return base_prompt + specific_fields + """

Format your response as a structured JSON-like output with clear labels and values.
If a field is not present in the document, mark it as "Not found" or "N/A".
Be thorough and extract all visible information from the document.
"""


def process_image_with_vision(image_bytes: bytes, doc_type: str, llm, provider: str) -> str:
    """Process image using vision-capable LLM."""
    import base64
    
    # Convert image bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Create the prompt
    prompt_text = create_extraction_prompt(doc_type)
    
    if provider == "OpenAI":
        # OpenAI format
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        )
        response = llm.invoke([message])
        return response.content
    else:
        # Gemini format - using the vision model
        from langchain_google_genai import ChatGoogleGenerativeAI
        import google.generativeai as genai
        
        genai.configure(api_key=llm.google_api_key)
        
        # Use the generative AI SDK directly for vision
        model = genai.GenerativeModel(llm.model)
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": image_base64
            }
        ]
        
        response = model.generate_content([prompt_text, image_parts[0]])
        return response.text


def extract_entities(uploaded_file, doc_type: str, provider: str, api_key: str, model: str) -> Optional[str]:
    """Extract entities from uploaded document."""
    try:
        # Read the file
        file_bytes = uploaded_file.read()
        
        # Check if it's an image
        try:
            image = Image.open(io.BytesIO(file_bytes))
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Initialize LLM
            llm = get_llm(provider, api_key, model)
            
            # Process with vision model
            result = process_image_with_vision(img_byte_arr, doc_type, llm, provider)
            
            return result
            
        except Exception as e:
            return f"Error processing image: {str(e)}"
            
    except Exception as e:
        return f"Error: {str(e)}"


# Main app layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=["png", "jpg", "jpeg", "pdf", "bmp", "gif"],
        help="Upload an image of your document"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document", use_container_width=True)
            uploaded_file.seek(0)  # Reset file pointer
        except Exception as e:
            st.error(f"Error displaying image: {e}")

with col2:
    st.header("🔍 Extracted Entities")
    
    if uploaded_file is not None:
        if st.button("🚀 Extract Entities", type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your API key in the sidebar!")
            else:
                with st.spinner("🔄 Processing document and extracting entities..."):
                    # Determine actual doc type
                    actual_doc_type = doc_type if doc_type != "Auto-detect" else "General Document"
                    
                    # Extract entities
                    result = extract_entities(
                        uploaded_file,
                        actual_doc_type,
                        api_provider,
                        api_key,
                        model_name
                    )
                    
                    if result:
                        st.success("✅ Entities extracted successfully!")
                        st.markdown("### Extracted Information:")
                        st.markdown(result)
                        
                        # Download button for results
                        st.download_button(
                            label="💾 Download Results",
                            data=result,
                            file_name=f"extracted_entities_{uploaded_file.name}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ Failed to extract entities. Please try again.")
    else:
        st.info("👆 Please upload a document to begin extraction.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit, LangChain, and AI</p>
    <p><small>Supports OpenAI and Google Gemini APIs</small></p>
</div>
""", unsafe_allow_html=True)
