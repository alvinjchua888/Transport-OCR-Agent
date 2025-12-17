# Supabase Setup Guide

## 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in your project details:
   - **Name**: Transport-OCR-Agent
   - **Database Password**: Choose a secure password
   - **Region**: Select closest to your users
4. Click "Create new project" (takes ~2 minutes)

## 2. Run the Database Setup

1. In your Supabase dashboard, click **SQL Editor** in the left sidebar
2. Click **New query**
3. Copy the contents of `supabase_setup.sql`
4. Paste it into the SQL editor
5. Click **Run** or press `Ctrl+Enter`
6. You should see: ✅ Success message

## 3. Get Your API Credentials

1. In Supabase dashboard, go to **Settings** (gear icon) → **API**
2. Copy the following values:

   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbGc...` (long string)

## 4. Configure Your App

### Option A: Using .env file (Recommended)

Add to your `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Option B: Using the Streamlit sidebar

1. Run your app: `streamlit run app.py`
2. In the sidebar under "Database Configuration":
   - Paste your **Supabase URL**
   - Paste your **Supabase API Key**

## 5. Test the Integration

1. Upload a document in the app
2. Click "Extract Entities"
3. After successful extraction, click **"Save to Database"**
4. Check your Supabase dashboard → **Table Editor** → `document_extractions`
5. You should see your saved data! 🎉

## What Gets Stored

Each extraction saves:
- `id`: Unique identifier (UUID)
- `document_type`: Type of document (invoice, receipt, etc.)
- `uploaded_at`: Timestamp
- `entities`: JSON object with all extracted fields
- `raw_text`: Full extracted text
- `file_name`: Original file name
- `model_used`: AI model used for extraction

## Querying Your Data

### View recent extractions in Supabase:
```sql
SELECT * FROM document_extractions 
ORDER BY uploaded_at DESC 
LIMIT 10;
```

### Search for specific entity values:
```sql
SELECT * FROM document_extractions 
WHERE entities->>'invoice_number' = 'INV-001';
```

### Count extractions by document type:
```sql
SELECT document_type, COUNT(*) 
FROM document_extractions 
GROUP BY document_type;
```

## Security Notes

- The default setup allows all operations (good for development)
- For production, update Row Level Security (RLS) policies
- Never commit your `.env` file with real credentials
- Regenerate keys if accidentally exposed

## Troubleshooting

**Error: "Failed to save to database"**
- Check your Supabase URL and API key are correct
- Verify the table exists (run `supabase_setup.sql` again)
- Check Supabase dashboard → Logs for error details

**Error: "relation 'document_extractions' does not exist"**
- The table wasn't created. Run `supabase_setup.sql` in SQL Editor

**Need help?**
- Check Supabase logs: Dashboard → Logs
- Visit Supabase docs: [https://supabase.com/docs](https://supabase.com/docs)
