# Transport-OCR-Agent 📄

OCR Agent Streamlit App for intelligent document entity extraction using AI-powered character recognition with OpenAI and Google Gemini APIs.

## Features ✨

- 🤖 **AI-Powered OCR**: Leverages OpenAI GPT-4 Vision or Google Gemini Vision models
- 📝 **Multiple Document Types**: Supports invoices, receipts, emails, and general documents
- 🔍 **Entity Extraction**: Automatically extracts structured data from documents
- 🎯 **Smart Detection**: Auto-detects document type or allows manual selection
- 💾 **Export Results**: Download extracted entities as text files
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit UI
- 🔌 **Dual API Support**: Choose between OpenAI or Google Gemini

## Supported Document Types 📑

1. **Invoices**: Extract invoice numbers, dates, line items, totals, vendor details, etc.
2. **Receipts**: Extract store information, items purchased, prices, payment methods
3. **Emails**: Extract sender, recipient, subject, body content, attachments info
4. **General Documents**: Extract any relevant entities from various document types

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- OpenAI API key or Google Gemini API key

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/alvinjchua888/Transport-OCR-Agent.git
cd Transport-OCR-Agent
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage 💡

### Running the App

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using the App

1. **Select AI Provider**: Choose between OpenAI or Google Gemini in the sidebar
2. **Enter API Key**: Input your API key (or use the one from .env file)
3. **Choose Model**: Select the specific model you want to use
4. **Select Document Type**: Choose the type of document or use auto-detect
5. **Upload Document**: Click "Browse files" and select your document image
6. **Extract Entities**: Click the "Extract Entities" button
7. **Review Results**: View the extracted information
8. **Download**: Optionally download the results as a text file

### Supported File Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- PDF (.pdf)
- BMP (.bmp)
- GIF (.gif)

## API Keys 🔑

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into the app or .env file

### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste into the app or .env file

## Technology Stack 🛠️

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **AI Providers**: OpenAI GPT-4 Vision, Google Gemini Vision
- **Image Processing**: Pillow (PIL)
- **Environment Management**: python-dotenv

## Project Structure 📁

```
Transport-OCR-Agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Configuration Options ⚙️

### OpenAI Models
- `gpt-4-vision-preview`: Most capable vision model
- `gpt-4o`: Optimized GPT-4 with vision
- `gpt-4o-mini`: Faster, cost-effective option

### Google Gemini Models
- `gemini-pro-vision`: Pro model with vision capabilities
- `gemini-1.5-pro`: Latest pro model
- `gemini-1.5-flash`: Faster, lightweight model

## Examples 📸

### Invoice Processing
Upload an invoice image and the app will extract:
- Invoice number, dates, amounts
- Vendor and customer details
- Line items with quantities and prices
- Tax information and totals

### Receipt Processing
Upload a receipt and extract:
- Store information
- Items purchased with prices
- Payment method and transaction details
- Date and time of purchase

### Email Processing
Upload an email screenshot and extract:
- Sender and recipient information
- Subject and body content
- Dates and attachments mentioned
- Contact details

## Troubleshooting 🔧

### Common Issues

**Issue**: "API key not found"
- **Solution**: Make sure you've entered your API key in the sidebar or added it to the .env file

**Issue**: "Error processing image"
- **Solution**: Ensure your image is in a supported format and is clear/readable

**Issue**: "Model not available"
- **Solution**: Check that you have access to the selected model with your API key

### Dependencies Issues

If you encounter issues with dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://www.langchain.com/)
- AI models from [OpenAI](https://openai.com/) and [Google](https://deepmind.google/technologies/gemini/)

---

**Happy Document Processing! 🎉**
