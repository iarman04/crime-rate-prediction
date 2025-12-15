import sqlite3
import pandas as pd
import os

# Adjust the database path if it's not in the current folder
db_path = 'chicago_crimes.db'  # Or full path, e.g., r'C:\Users\admin\OneDrive\Desktop\new final project\chicago_crimes.db'

# Step 1: Check if the database file exists
if not os.path.exists(db_path):
    print(f"ERROR: Database file '{db_path}' not found! Check the path.")
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir('.'))
    exit()  # Stop here if file is missing

print(f"✓ Database file '{db_path}' found (size: {os.path.getsize(db_path)} bytes).")

# Step 2: Try to connect
try:
    conn = sqlite3.connect(db_path)
    print("✓ Database connection successful.")
except Exception as e:
    print(f"ERROR: Failed to connect to database: {e}")
    exit()

# Step 3: List all tables
try:
    tables_df = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print("\nExisting tables in the database:")
    if tables_df.empty:
        print("No tables found! The database might be empty or corrupted.")
    else:
        for table in tables_df['name']:
            print(f"  - {table}")
        
        # Specifically check for 'crimes' and 'yearly_crimes'
        crimes_exists = 'crimes' in tables_df['name'].values
        yearly_exists = 'yearly_crimes' in tables_df['name'].values
        print(f"\n- 'crimes' table exists: {crimes_exists}")
        print(f"- 'yearly_crimes' table exists: {yearly_exists}")
        
except Exception as e:
    print(f"ERROR querying tables: {e}")

# Step 4: If 'crimes' exists, show its structure and a sample
if 'crimes' in tables_df['name'].values:
    try:
        # Show column info
        cols_df = pd.read_sql("PRAGMA table_info(crimes);", conn)
        print("\nColumns in 'crimes' table:")
        print(cols_df[['name', 'type']])
        
        # Show row count and sample
        count = pd.read_sql("SELECT COUNT(*) as total_rows FROM crimes;", conn).iloc[0]['total_rows']
        print(f"\nTotal rows in 'crimes': {count:,}")
        
        sample = pd.read_sql("SELECT * FROM crimes LIMIT 5;", conn)
        print("\nSample rows from 'crimes':")
        print(sample)
        
    except Exception as e:
        print(f"ERROR querying 'crimes' table: {e}")
else:
    print("\nNo 'crimes' table— you may need to re-import the data.")

# Step 5: Close connection
conn.close()
print("\nTest complete. If issues persist, share this output!")
