import sqlite3
import pandas as pd
import os
import joblib  # For saving/loading the model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Database path (adjust if needed)
DB_PATH = 'chicago_crimes.db'
MODEL_PATH = 'crime_model.pkl'  # Where the trained model is saved

def train_model():
    """
    Creates the yearly_crimes table, loads data, trains a Linear Regression model,
    and saves it to MODEL_PATH.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        # Step 1: Drop and recreate yearly_crimes to ensure fresh aggregation
        print("Creating/recreating 'yearly_crimes' table...")
        conn.execute("DROP TABLE IF EXISTS yearly_crimes;")
        conn.execute("""
        CREATE TABLE yearly_crimes AS
        SELECT 
            Year, 
            District, 
            COUNT(*) as CrimeCount
        FROM crimes
        WHERE Year IS NOT NULL AND District IS NOT NULL AND District > 0
        GROUP BY Year, District
        ORDER BY Year, District;
        """)
        conn.commit()
        
        # Step 2: Verify creation
        row_count = pd.read_sql('SELECT COUNT(*) FROM yearly_crimes', conn).iloc[0, 0]
        print(f"✓ 'yearly_crimes' created/verified with {row_count} rows.")
        
        # Step 3: Double-check table existence
        tables_check = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='yearly_crimes';", conn)
        if tables_check.empty:
            print("WARNING: Table missing—re-creating...")
            conn.execute("DROP TABLE IF EXISTS yearly_crimes;")
            conn.execute("""
            CREATE TABLE yearly_crimes AS
            SELECT 
                Year, 
                District, 
                COUNT(*) as CrimeCount
            FROM crimes
            WHERE Year IS NOT NULL AND District IS NOT NULL AND District > 0
            GROUP BY Year, District
            ORDER BY Year, District;
            """)
            conn.commit()
            row_count = pd.read_sql('SELECT COUNT(*) FROM yearly_crimes', conn).iloc[0, 0]
            print(f"Re-created with {row_count} rows.")
        else:
            print("✓ Table confirmed.")
        
        # Step 4: Load data
        df = pd.read_sql('SELECT Year, District, CrimeCount FROM yearly_crimes', conn)
        print(f"✓ Loaded {len(df)} rows for training.")
        
        # Step 5: Train the model
        X = df[['Year', 'District']]
        y = df['CrimeCount']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Model trained! MSE: {mse:,.0f}, R²: {r2:.4f}")
        
        # Save the model
        joblib.dump(model, MODEL_PATH)
        print(f"✓ Model saved to '{MODEL_PATH}'.")
        
    except Exception as e:
        print(f"Error in train_model: {e}")
        # Quick debug: Check crimes columns if needed
        try:
            cols = pd.read_sql("PRAGMA table_info(crimes);", conn)
            print("Columns in 'crimes':", cols['name'].tolist())
        except:
            pass
    finally:
        conn.close()

def predict_crime(year, district):
    """
    Predicts crime count for a given year and district.
    Auto-trains the model if it doesn't exist.
    
    Args:
        year (int): e.g., 2025
        district (int): e.g., 10 (Chicago PD district 1-25)
    
    Returns:
        float: Predicted crime count
    """
    if not os.path.exists(MODEL_PATH):
        print("Model not found—training first...")
        train_model()
    
    # Load the model
    try:
        model = joblib.load(MODEL_PATH)
        prediction = model.predict([[year, district]])[0]
        print(f"Predicted crimes for District {district} in {year}: {prediction:,.0f}")
        return prediction
    except Exception as e:
        print(f"Error in prediction: {e}")
        print("Try running train_model() manually first.")
        return None

# Optional: Train on import (uncomment if you want auto-training when model.py is imported)
# if __name__ == "__main__":
#     train_model()

# For direct runs: Train the model
if __name__ == "__main__":
    train_model()