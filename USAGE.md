# Usage Guide for Transport OCR Agent

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/alvinjchua888/Transport-OCR-Agent.git
cd Transport-OCR-Agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Set up your API keys in a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

Add your API keys:
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
GOOGLE_API_KEY=your-actual-google-api-key-here
```

### 3. Run the Application

```bash
# Using the run script
./run_app.sh

# Or directly with streamlit
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Using the Application

### Step-by-Step Guide

1. **Select AI Provider**
   - Choose between "OpenAI" or "Google Gemini" in the sidebar
   - Each provider has different models available

2. **Enter API Key**
   - Input your API key for the selected provider
   - Or use the key from your `.env` file (auto-loaded)

3. **Choose Model**
   - OpenAI options: GPT-4 Vision, GPT-4o, GPT-4o-mini
   - Gemini options: Gemini Pro Vision, Gemini 1.5 Pro, Gemini 1.5 Flash

4. **Select Document Type**
   - Auto-detect: Let AI determine the document type
   - Invoice: For billing documents
   - Receipt: For purchase receipts
   - Email: For email screenshots
   - General Document: For other documents

5. **Upload Document**
   - Click "Browse files" button
   - Select your document image (PNG, JPG, PDF, etc.)
   - Preview will appear on the left side

6. **Extract Entities**
   - Click the "🚀 Extract Entities" button
   - Wait for processing (usually 5-15 seconds)
   - View results on the right side

7. **Download Results**
   - Click "💾 Download Results" to save extracted data
   - Results are saved as a text file

## Document Types & Extracted Fields

### Invoice
Extracts:
- Invoice number, dates, amounts
- Vendor and customer information
- Line items with quantities and prices
- Tax and total amounts
- Payment terms

### Receipt
Extracts:
- Store name and location
- Transaction ID and date/time
- Items purchased with prices
- Payment method
- Tax and total amounts

### Email
Extracts:
- Sender and recipient details
- Subject line
- Email body content
- Mentioned attachments
- Dates and action items

### General Document
Extracts:
- Document title and type
- Key entities (names, organizations)
- Important dates and amounts
- Contact information
- Summary of content

## Best Practices

### For Best Results

1. **Image Quality**
   - Use high-resolution images
   - Ensure text is clear and readable
   - Avoid blurry or dark images

2. **Document Orientation**
   - Keep documents upright
   - Avoid rotated or skewed images

3. **File Format**
   - PNG and JPG work best
   - PDF support available
   - Keep file sizes reasonable (< 10MB)

4. **API Selection**
   - OpenAI GPT-4o: Most accurate, higher cost
   - GPT-4o-mini: Good balance, lower cost
   - Gemini 1.5 Flash: Fast and economical
   - Gemini 1.5 Pro: High accuracy

### Cost Considerations

- **OpenAI**: Charges per token and image
  - GPT-4o: ~$0.01-0.03 per image
  - GPT-4o-mini: ~$0.001-0.005 per image

- **Google Gemini**: Free tier available
  - Gemini 1.5 Flash: Fastest and cheapest
  - Gemini 1.5 Pro: Higher accuracy

## Troubleshooting

### Common Issues

**Problem**: "API key not found" error
- **Solution**: Check your `.env` file or enter key in sidebar

**Problem**: "Error processing image"
- **Solution**: Try a different image format or reduce file size

**Problem**: Poor extraction quality
- **Solution**: Try a different model or improve image quality

**Problem**: Slow processing
- **Solution**: Use faster models (GPT-4o-mini or Gemini Flash)

### Getting Help

If you encounter issues:
1. Check the error message in the app
2. Review the console output
3. Verify API key is valid
4. Ensure image format is supported
5. Open an issue on GitHub

## Advanced Usage

### Running Tests

```bash
# Run the test suite
python test_app.py
```

### Custom Prompts

You can modify prompts in `app.py` by editing the `create_extraction_prompt()` function for different extraction needs.

### Batch Processing

For multiple documents:
1. Process one document at a time through the UI
2. Download results for each
3. Or modify the code to add batch processing capabilities

## API Keys

### Getting OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to "API Keys"
4. Create new key
5. Copy and save securely

### Getting Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy and save securely

## Security Notes

- Never commit `.env` file to git
- Keep API keys secure and private
- Rotate keys regularly
- Monitor API usage and costs
- Use environment variables in production

## Performance Tips

1. **Use appropriate models**: Don't use expensive models for simple tasks
2. **Optimize images**: Compress images before upload
3. **Batch similar documents**: Process similar types together
4. **Monitor costs**: Track API usage regularly
5. **Cache results**: Save extraction results to avoid reprocessing

## Example Workflow

```
1. Start app: streamlit run app.py
2. Select: OpenAI + GPT-4o-mini
3. Enter: Your API key
4. Choose: Invoice
5. Upload: your_invoice.png
6. Click: Extract Entities
7. Review: Extracted data
8. Download: Save results
9. Process next document
```

## Support

For questions or issues:
- GitHub Issues: https://github.com/alvinjchua888/Transport-OCR-Agent/issues
- Documentation: See README.md
- Tests: Run test_app.py

---

**Happy Document Processing! 📄✨**
