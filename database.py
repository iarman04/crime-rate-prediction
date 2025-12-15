import sqlite3
import pandas as pd
import os
import csv  # For quoting constant
from sqlalchemy import create_engine

def init_db():
    print("Loading dataset and initializing database...")
    csv_path = 'chicago_crimes.csv'  # Ensure this matches your file name
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found. Available CSV files: {[f for f in os.listdir('.') if f.endswith('.csv')]}")
        return
    
    # Create or connect to SQLite database
    db_path = 'chicago_crimes.db'
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Check existing row count to resume if partial
    try:
        existing_count = pd.read_sql('SELECT COUNT(*) as count FROM crimes', engine).iloc[0, 0]
        print(f"Existing rows in DB: {existing_count:,}")
        if_exists_mode = 'append'
    except:
        existing_count = 0
        if_exists_mode = 'replace'
        print("Starting fresh DB.")
    
    # Robust CSV reading for malformed data
    chunksize = 10000  
    total_rows = existing_count
    skipped_rows = 0
    
    try:
        # Use Python engine for better error handling
        chunk_iterator = pd.read_csv(
            csv_path,
            chunksize=chunksize,
            
            engine='python',  # Robust parser for bad quotes/EOF
            on_bad_lines='skip',  # Skip malformed rows (logs warning)
            quoting=csv.QUOTE_ALL,  # Quote all fields to prevent tokenization issues
            encoding='utf-8',  # Handle encoding problems
            dtype=str  # Read as strings initially to avoid type errors
        )
        
        first_chunk = existing_count == 0  # Only print columns on fresh load
        
        for chunk_num, chunk in enumerate(chunk_iterator, start=1):
            if first_chunk:
                print("CSV columns found:", list(chunk.columns[:10]), "...")
                first_chunk = False
            
            # Convert dtypes after reading (safer for large chunks)
            for col in chunk.columns:
                if col in ['Arrest', 'Domestic']:  # Booleans
                    chunk[col] = chunk[col].astype(bool, errors='ignore')
                elif col in ['Beat', 'District', 'Ward', 'Community Area', 'Year']:  # Integers
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0).astype(int)
                elif col in ['Latitude', 'Longitude', 'X Coordinate', 'Y Coordinate']:  # Floats
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
            
            # Select key columns
            key_cols = [
                'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description',
                'Location Description', 'Arrest', 'Domestic', 'Beat', 'District', 'Ward',
                'Community Area', 'FBI Code', 'X Coordinate', 'Y Coordinate', 'Year',
                'Updated On', 'Latitude', 'Longitude', 'Location'
            ]
            available_cols = [col for col in key_cols if col in chunk.columns]
            chunk = chunk[available_cols]
            
            # Drop invalid location rows
            initial_chunk_size = len(chunk)
            chunk = chunk.dropna(subset=['Latitude', 'Longitude'])
            skipped_rows += (initial_chunk_size - len(chunk))
            
            if chunk.empty:
                print(f"Chunk {chunk_num}: Empty after cleaning, skipping.")
                continue
            
            # Parse dates with specific format (suppresses warning)
            if 'Date' in chunk.columns:
                chunk['Date'] = pd.to_datetime(chunk['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
            
            # Insert into DB
            chunk.to_sql('crimes', con=engine, if_exists=if_exists_mode, index=False, chunksize=1000)
            total_rows += len(chunk)
            print(f"Chunk {chunk_num}: Processed {len(chunk):,} rows (total: {total_rows:,}; skipped in chunk: {initial_chunk_size - len(chunk)})")
            
            if_exists_mode = 'append'  # Switch to append after first
        
        # Add indexes for performance
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_date ON crimes(Date)",
            "CREATE INDEX IF NOT EXISTS idx_type ON crimes(`Primary Type`)",
            "CREATE INDEX IF NOT EXISTS idx_location ON crimes(Latitude, Longitude)"
        ]
        for idx in indexes:
            cursor.execute(idx)
        conn.commit()
        conn.close()
        
        print(f"\nSuccess! Database '{db_path}' updated with {total_rows:,} total rows.")
        print(f"Skipped rows due to errors/cleaning: ~{skipped_rows:,}")
        print(f"Expected full dataset: ~8M rows. If low, re-download CSV.")
        print("Test query: SELECT * FROM crimes LIMIT 3;")
        
        # Quick integrity check
        test_df = pd.read_sql('SELECT Date, `Primary Type`, Latitude FROM crimes ORDER BY Date DESC LIMIT 5', engine)
        print("\nRecent sample rows:")
        print(test_df)
    
    except Exception as e:
        print(f"Error during loading: {e}")
        print("Troubleshooting:")
        print("- Re-download CSV from https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2")
        print("- Ensure no other apps have the file open.")
        print("- If persists, try smaller chunksize=10000.")

if __name__ == '__main__':
    init_db()
