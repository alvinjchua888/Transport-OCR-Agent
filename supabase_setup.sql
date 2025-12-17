-- Supabase Table Setup for Transport-OCR-Agent
-- Run this SQL in your Supabase SQL Editor to create the required table

-- Create the document_extractions table
CREATE TABLE IF NOT EXISTS document_extractions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    document_type TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    entities JSONB NOT NULL,
    raw_text TEXT,
    file_name TEXT,
    model_used TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an index on uploaded_at for faster queries
CREATE INDEX IF NOT EXISTS idx_document_extractions_uploaded_at 
ON document_extractions(uploaded_at DESC);

-- Create an index on document_type for filtering
CREATE INDEX IF NOT EXISTS idx_document_extractions_document_type 
ON document_extractions(document_type);

-- Create a GIN index on entities JSONB column for efficient querying
CREATE INDEX IF NOT EXISTS idx_document_extractions_entities 
ON document_extractions USING GIN (entities);

-- Enable Row Level Security (RLS) - optional but recommended
ALTER TABLE document_extractions ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (adjust based on your needs)
-- For development: allow all operations
CREATE POLICY "Allow all operations on document_extractions" 
ON document_extractions 
FOR ALL 
USING (true) 
WITH CHECK (true);

-- Optional: Create a view for recent extractions
CREATE OR REPLACE VIEW recent_extractions AS
SELECT 
    id,
    document_type,
    uploaded_at,
    file_name,
    model_used,
    jsonb_pretty(entities) as entities_formatted
FROM document_extractions
ORDER BY uploaded_at DESC
LIMIT 100;

-- Optional: Function to search entities by key
CREATE OR REPLACE FUNCTION search_entities(search_key TEXT)
RETURNS TABLE (
    id UUID,
    document_type TEXT,
    uploaded_at TIMESTAMPTZ,
    file_name TEXT,
    entity_value TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        de.id,
        de.document_type,
        de.uploaded_at,
        de.file_name,
        de.entities->>search_key as entity_value
    FROM document_extractions de
    WHERE de.entities ? search_key
    ORDER BY de.uploaded_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Supabase tables and indexes created successfully!';
    RAISE NOTICE 'You can now use the Transport-OCR-Agent app with Supabase.';
END $$;
