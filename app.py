# from flask import Flask, render_template, request, jsonify
# import numpy as np
# import pickle
# import os







# from flask import Flask, request, jsonify, render_template
# import os
# import pandas as pd
# import sqlite3
# from model import train_model, predict_crime 

 # Import your model functions

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# DB_PATH = 'chicago_crimes.db'  # Match your model.py

# @app.route('/')
# def index():
#     """Serve the main frontend page."""
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     """Handle dataset upload, process CSV, update DB, and retrain model."""
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400
    
#     if not file.filename.endswith('.csv'):
#         return jsonify({'error': 'Only CSV files allowed'}), 400
    
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)
    
#     try:
#         # Process CSV and insert into DB (assumes columns: ID, Year, District, etc.)
#         conn = sqlite3.connect(DB_PATH)
#         df = pd.read_csv(filepath)
        
#         # Basic cleaning: Keep only relevant columns (adjust as needed)
#         required_cols = ['ID', 'Year', 'District']  # Add more if your CSV has them
#         df = df[required_cols].dropna(subset=['Year', 'District'])
        
#         # Insert into 'crimes' table (create if doesn't exist)
#         df.to_sql('crimes', conn, if_exists='append', index=False)
#         conn.commit()
#         conn.close()
        
#         # Retrain model with new data
#         train_model()
        
#         # Clean up uploaded file (optional)
#         os.remove(filepath)
        
#         return jsonify({'message': f'Dataset uploaded successfully! Added {len(df)} rows. Model retrained.'})
    
#     except Exception as e:
#         return jsonify({'error': f'Upload failed: {str(e)}'}), 500

# @app.route('/predict', methods=['POST'])
# def predict():
#     """Handle POST prediction requests."""
#     data = request.json
#     year = data.get('year')
#     district = data.get('district')
    
#     if year is None or district is None:
#         return jsonify({'error': 'Year and district are required'}), 400
    
#     try:
#         prediction = predict_crime(int(year), int(district))
#         if prediction is None:
#             return jsonify({'error': 'Prediction failed. Try retraining the model.'}), 500
        
#         return jsonify({'predicted_crime_count': float(prediction)})
    
#     except Exception as e:
#         return jsonify({'error': f'Prediction error: {str(e)}'}), 500

# if __name__ == '__main__':
#     # Initial data load if DB is empty (uncomment if needed)
#     # load_initial_data()  # Add your initial dataset loading here if required
    
#     app.run(debug=True, host='127.0.0.1', port=5000)

















# from flask import Flask, render_template, request, jsonify
# import numpy as np
# import pickle

# app = Flask(__name__)

# # ---- Load the ML model ----
# with open('model.pkl', 'rb') as file:
#     model = pickle.load(file)

# # ---- Home route ----
# @app.route('/')
# def home():
#     return render_template('index.html')

# # ---- Predict route ----
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     year = data['year']
#     district = data['district']

#     # Predict crime count using the ML model
#     predicted_value = model.predict([[year, district]])[0]

#     # Example district coordinates
#     district_coords = {
#         1: [41.8781, -87.6298],
#         2: [41.8917, -87.6070],
#         3: [41.7650, -87.6100],
#         # ... add more
#     }

#     coords = district_coords.get(district, [41.8781, -87.6298])

#     return jsonify({
#         "predicted_crime_count": float(predicted_value),
#         "latitude": coords[0],
#         "longitude": coords[1]
#     })


# if __name__ == '__main__':
#     app.run(debug=True)






















# app = Flask(__name__)

# # ---- Load the ML model ----
# MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
# with open(MODEL_PATH, 'rb') as file:
#     model = pickle.load(file)

# # ---- Home route ----
# @app.route('/')
# def home():
#     return render_template('index.html')

# # ---- Predict route ----
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()

#     year = data.get('year')
#     district = data.get('district')

#     # Validate input
#     if year is None or district is None:
#         return jsonify({"error": "Missing year or district"}), 400

#     try:
#         # Predict using your model
#         predicted_value = model.predict([[year, district]])[0]

#         # Example district coordinates (update these)
#         district_coords = {
#             1: [41.8781, -87.6298],
#             2: [41.8917, -87.6070],
#             3: [41.7650, -87.6100],
#             # Add more districts here...
#         }

#         coords = district_coords.get(int(district), [41.8781, -87.6298])

#         return jsonify({
#             "predicted_crime_count": float(predicted_value),
#             "latitude": coords[0],
#             "longitude": coords[1]
#         })

#     except Exception as e:
#         print("Error during prediction:", e)
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
    



















# from flask import Flask, render_template, request, jsonify, send_from_directory
# import pandas as pd
# import os
# import pickle
# from werkzeug.utils import secure_filename

# # Optional: enable CORS if frontend and backend are on different origins
# # from flask_cors import CORS

# app = Flask(__name__)
# # CORS(app)  # uncomment if needed

# # Configure upload folder
# BASE_DIR = os.path.dirname(__file__)
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Load model if exists (safe load with try/except)
# MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
# model = None
# try:
#     if os.path.exists(MODEL_PATH):
#         with open(MODEL_PATH, 'rb') as f:
#             model = pickle.load(f)
#         print("Model loaded from model.pkl")
#     else:
#         print("No model.pkl found — prediction route will return a dummy value.")
# except Exception as e:
#     print("Error loading model:", e)
#     model = None

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         # Check if the post request has the file part
#         if 'file' not in request.files:
#             return jsonify({"success": False, "message": "No file part in the request."}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"success": False, "message": "No file selected."}), 400

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(save_path)

#             # Read CSV using pandas to count rows (and optionally retrain)
#             try:
#                 df = pd.read_csv(save_path)
#                 rows = len(df)
#             except Exception as e:
#                 # If pandas fails to read (bad CSV), remove file and return error
#                 os.remove(save_path)
#                 print("Error reading CSV:", e)
#                 return jsonify({"success": False, "message": "Failed to read CSV file: " + str(e)}), 400
            





            # TODO: retrain model here if you have a retrain function
            # Example:
            # try:
            #     model = retrain_model(df)
            #     with open(MODEL_PATH, 'wb') as mfile:
            #         pickle.dump(model, mfile)
            # except Exception as e:
            #     print("Retrain error:", e)
            #     # proceed anyway and notify user
            #     return jsonify({"success": False, "message": "Dataset uploaded but retrain failed: " + str(e)}), 500







#             message = f"Dataset uploaded successfully! Added {rows} rows. Model retrained."
#             print("Upload OK:", message)
#             return jsonify({"success": True, "message": message, "rows": rows}), 200

#         else:
#             return jsonify({"success": False, "message": "Invalid file format. Please upload a CSV file."}), 400

#     except Exception as e:
#         # Catch all exceptions and return JSON (prevents HTML error page)
#         print("Unhandled error in /upload:", e)
#         return jsonify({"success": False, "message": "Server error: " + str(e)}), 500

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Force JSON parsing and provide helpful error if not JSON
#         data = request.get_json(force=True)
#         print("Received prediction request:", data)

#         year = data.get('year')
#         district = data.get('district')

#         if year is None or district is None:
#             return jsonify({"error": "Missing 'year' or 'district' in request."}), 400

#         # Convert to numeric types if strings
#         try:
#             year = int(year)
#             district = int(district)
#         except Exception:
#             return jsonify({"error": "Year and district must be integers."}), 400

#         # If real model exists, predict. Otherwise return dummy example
#         if model is not None:
#             try:
#                 predicted_value = model.predict([[year, district]])[0]
#                 predicted_value = float(predicted_value)
#             except Exception as e:
#                 print("Model predict error:", e)
#                 return jsonify({"error": "Model prediction failed: " + str(e)}), 500
#         else:
#             # Dummy prediction (replace with real logic)
#             predicted_value = float( (year % 100) + district )  # placeholder

#         # Example coordinates (update with your district mapping)
#         district_coords = {
#             1: [41.8781, -87.6298],
#             2: [41.8917, -87.6070],
#             3: [41.7650, -87.6100],
#             # add others...
#         }
#         coords = district_coords.get(district, [41.8781, -87.6298])

#         return jsonify({
#             "predicted_crime_count": predicted_value,
#             "latitude": coords[0],
#             "longitude": coords[1]
#         }), 200

#     except Exception as e:
#         print("Unhandled error in /predict:", e)
#         return jsonify({"error": "Server error: " + str(e)}), 500

# # Optional: serve uploaded files for debug (not required)
# @app.route('/uploads/<path:filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

# if __name__ == '__main__':
#     app.run(debug=True)











from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
import pickle
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from datetime import datetime
from geopy.geocoders import Nominatim


# geolocator = Nominatim(user_agent="crime_app")
# location = geolocator.geocode("Delhi, India", timeout=10)
# coords = (location.latitude, location.longitude)


from dotenv import load_dotenv
load_dotenv()
import os

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")


# -------------------------------------------------------------
# 🔧 Basic Flask App Setup
# -------------------------------------------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
model = None

# -------------------------------------------------------------
# 🔍 Load Trained Model (if available)
# -------------------------------------------------------------
try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully from model.pkl")
    else:
        print("⚠️ model.pkl not found — using dummy predictions.")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


# -------------------------------------------------------------
# 📧 Email Alert Function (SMTP - Gmail)
# -------------------------------------------------------------
def send_email_alert(area, risk_level, crime_type):
    sender = "armannaina2006@gmail.com"                # 🔹 your Gmail (example: crimealertproject@gmail.com)
    receiver =  "nainavaid2006@gmail.com"             # 🔹 receiver email (can be same or different)
    password = "hmlx ottn lhie zgpr"   # 🔹 Gmail App Password (not your real password)
    

    subject = f"🚨 Crime Alert: High Risk in {area}"
    body = f"""
    ALERT: High Crime Risk Detected!
    -------------------------------
    📍 Area: {area}
    ⚠️ Risk Level: {risk_level}%
    🕵️ Crime Type: {crime_type}
    ⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Please stay alert and take necessary precautions.

    - Crime Prediction System
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print(f"✅ Email Alert Sent to {receiver}")
    except Exception as e:
        print(f"❌ Email Sending Failed: {e}")


# -------------------------------------------------------------
# 📱 SMS Alert Function (Twilio API)
# -------------------------------------------------------------
def send_sms_alert(area, risk_level, crime_type):
    account_sid = "AC59fb9daa3b804ad482fe5d8be99eed93"          # 🔹 Twilio Account SID
    auth_token = "ac61e88befb5f5e883c0cf5f1d3107ec"            # 🔹 Twilio Auth Token
    from_number = "+12174396750"                      # 🔹 Twilio phone number (from your account)
    to_number ="+91 9041853975"                     # 🔹 Your verified phone number

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=from_number,
            to=to_number,
            body=f"🚨 ALERT: High crime risk detected in {area}! ({risk_level}% - {crime_type}) Stay safe."
        )
        print(f"✅ SMS sent successfully (SID: {message.sid})")
    except Exception as e:
        print(f"❌ SMS Sending Failed: {e}")


# -------------------------------------------------------------
# 🧠 Helper Function for File Validation
# -------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------------------------------------
# 🌐 Routes
# -------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------- 📤 File Upload --------------------------
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file part in the request."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected."}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            try:
                df = pd.read_csv(save_path)
                rows = len(df)
            except Exception as e:
                os.remove(save_path)
                print("Error reading CSV:", e)
                return jsonify({"success": False, "message": "Failed to read CSV: " + str(e)}), 400

            message = f"Dataset uploaded successfully! Added {rows} rows."
            print("✅", message)
            return jsonify({"success": True, "message": message, "rows": rows}), 200

        else:
            return jsonify({"success": False, "message": "Invalid file format. Please upload a CSV file."}), 400

    except Exception as e:
        print("Unhandled error in /upload:", e)
        return jsonify({"success": False, "message": "Server error: " + str(e)}), 500


# -------------------- 🔮 Prediction ---------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        print("📩 Received prediction request:", data)

        year = data.get('year')
        district = data.get('district')
        area = f"District {district}"
        crime_type = "General"

        if year is None or district is None:
            return jsonify({"error": "Missing 'year' or 'district'"}), 400

        year = int(year)
        district = int(district)

        # ✅ Step 1: Predict value
        if model is not None:
            predicted_value = model.predict([[year, district]])[0]
            predicted_value = float(predicted_value)
        else:
            predicted_value = float((year % 100) + district)  # Dummy fallback

        # ✅ Step 2: Define coordinates
        district_coords = {
            1: [41.8781, -87.6298],
            2: [41.8917, -87.6070],
            3: [41.7650, -87.6100],
        }
        coords = district_coords.get(district, [41.8781, -87.6298])

        # ✅ Step 3: Trigger alerts (AFTER coords exist)
        risk_level = int(predicted_value)
        if risk_level >= 70:
            send_email_alert(area, risk_level, crime_type)
            send_sms_alert(area, risk_level, crime_type)

        # ✅ Step 4: Return results
        return jsonify({
            "predicted_crime_count": predicted_value,
            "latitude": coords[0],
            "longitude": coords[1],
            "alert_sent": risk_level >= 60
        }), 200

    except Exception as e:
        print("❌ Unhandled error in /predict:", e)
        return jsonify({"error": "Server error: " + str(e)}), 500


        # Example district coordinates
        district_coords = {
            1: [41.8781, -87.6298],
            2: [41.8917, -87.6070],
            3: [41.7650, -87.6100],
        }
        coords = district_coords.get(district, [41.8781, -87.6298])

        # 🚨 Trigger Alerts for High Risk
        risk_level = int(predicted_value)
        if risk_level >= 70:
            send_email_alert(area, risk_level, crime_type)
            send_sms_alert(area, risk_level, crime_type)

        return jsonify({
            "predicted_crime_count": predicted_value,
            "latitude": coords[0],
            "longitude": coords[1],
            "alert_sent": risk_level >= 10
        }), 200

    except Exception as e:
        print("❌ Unhandled error in /predict:", e)
        return jsonify({"error": "Server error: " + str(e)}), 500


# -------------------- 📂 Serve Uploaded Files -----------------
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)


# -------------------------------------------------------------
# 🚀 Run Flask App
# -------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
