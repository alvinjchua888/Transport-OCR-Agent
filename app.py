import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import io
from typing import Optional
from datetime import datetime
import json

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# Supabase imports
from supabase import create_client, Client

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
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
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
    
    # Supabase Configuration
    st.header("💾 Database Configuration")
    enable_db = st.checkbox(
        "Enable Supabase Storage",
        value=False,
        help="Save extracted entities to Supabase database"
    )
    
    if enable_db:
        supabase_url = st.text_input(
            "Supabase URL",
            type="default",
            value=os.getenv("SUPABASE_URL", ""),
            help="Your Supabase project URL"
        )
        supabase_key = st.text_input(
            "Supabase API Key",
            type="password",
            value=os.getenv("SUPABASE_KEY", ""),
            help="Your Supabase anon/public API key"
        )
        
        table_name = st.text_input(
            "Table Name",
            value="ocr_documents",
            help="Name of the Supabase table to store extracted data"
        )
    else:
        supabase_url = ""
        supabase_key = ""
        table_name = "ocr_documents"
    
    st.markdown("---")
    st.markdown("""
    ### 📝 Instructions
    1. Select your AI provider
    2. Enter your API key
    3. Choose document type
    4. (Optional) Enable Supabase storage
    5. Upload your document
    6. Click 'Extract Entities'
    """)


def get_supabase_client(url: str, key: str) -> Optional[Client]:
    """Initialize Supabase client."""
    try:
        if url and key:
            return create_client(url, key)
        return None
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        return None


def save_to_supabase(client: Client, table_name: str, data: dict) -> bool:
    """Save extracted entities to Supabase."""
    try:
        response = client.table(table_name).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error saving to database: {e}")
        return False


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
    """
    Process an image using a vision-capable LLM to extract structured information.
    This function handles image processing for both OpenAI and Google Gemini vision models,
    converting image bytes to the appropriate format and invoking the respective AI service
    to extract information based on the specified document type.
    Args:
        image_bytes (bytes): The raw bytes of the image to be processed.
        doc_type (str): The type of document to extract information from (e.g., 'invoice', 'receipt').
        llm: The language model instance to use for processing. Should be either an OpenAI or Gemini model.
        provider (str): The AI provider name, either "OpenAI" or "Gemini". Determines the processing format.
    Returns:
        str: The extracted text content from the image as processed by the vision model.
    Raises:
        Exception: May raise exceptions related to API calls, image processing, or model invocation.
    Notes:
        - For OpenAI: Uses HumanMessage with multimodal content (text + image_url).
        - For Gemini: Uses google.generativeai SDK directly with PIL Image objects.
        - The function converts images to base64 for OpenAI and back to PIL Image for Gemini.
        - Gemini API key is retrieved from the llm instance or environment variables.
    """
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
        import google.generativeai as genai
        
        # Get API key from llm instance
        if hasattr(llm, 'google_api_key'):
            api_key_to_use = llm.google_api_key
        else:
            # Fallback to the api_key from environment or parameter
            api_key_to_use = os.getenv("GOOGLE_API_KEY", "")
        
        genai.configure(api_key=api_key_to_use)
        
        # Use the generative AI SDK directly for vision
        # Map model names to ensure compatibility
        model_name = llm.model if hasattr(llm, 'model') else 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)
        
        # Create image part
        from PIL import Image
        import io
        
        # Convert base64 back to image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        response = model.generate_content([prompt_text, image])
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
                        
                        # Store result in session state for saving to DB
                        st.session_state['last_result'] = result
                        st.session_state['last_filename'] = uploaded_file.name
                        st.session_state['last_doc_type'] = actual_doc_type
                        
                        # Download button for results
                        st.download_button(
                            label="💾 Download Results",
                            data=result,
                            file_name=f"extracted_entities_{uploaded_file.name}.txt",
                            mime="text/plain"
                        )
                        
                        # Save to Supabase button
                        if enable_db:
                            st.markdown("---")
                            if st.button("💾 Save to Database", type="secondary"):
                                if not supabase_url or not supabase_key:
                                    st.error("⚠️ Please enter Supabase credentials in the sidebar!")
                                else:
                                    with st.spinner("Saving to database..."):
                                        supabase_client = get_supabase_client(supabase_url, supabase_key)
                                        if supabase_client:
                                            # Prepare data for database
                                            db_data = {
                                                "document_type": actual_doc_type,
                                                "filename": uploaded_file.name,
                                                "extracted_text": result,
                                                "ai_provider": api_provider,
                                                "model_used": model_name,
                                                "created_at": datetime.utcnow().isoformat()
                                            }
                                            
                                            if save_to_supabase(supabase_client, table_name, db_data):
                                                st.success("✅ Successfully saved to database!")
                                            else:
                                                st.error("❌ Failed to save to database.")
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
