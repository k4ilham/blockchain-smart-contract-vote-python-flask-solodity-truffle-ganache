import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
import hashlib
import math

# Inisialisasi Flask
app = Flask(__name__)

# Membaca dataset dari file CSV
df = pd.read_csv('dataset.csv')  # Pastikan file CSV ada di direktori yang sama

# Memastikan kolom yang diperlukan ada dalam dataset
if not all(col in df.columns for col in ["voter_id", "candidate_id", "vote_time", "label"]):
    raise ValueError("CSV file must contain columns: 'voter_id', 'candidate_id', 'vote_time', 'label'")

# Split data menjadi fitur dan label
X = df[["voter_id", "candidate_id", "vote_time"]].values  # Fitur
y = df["label"].values  # Label

# Melatih model machine learning (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

@app.route('/detect_double_vote', methods=['POST'])
def detect_double_vote():
    try:
        # Ambil data suara dari permintaan POST
        vote_data = request.json  # Data dalam format JSON
        voter_id = vote_data["voter_id"]
        candidate_id = vote_data["candidate_id"]
        vote_time = vote_data["vote_time"]

        # Memastikan data lengkap
        if not all([voter_id, candidate_id, vote_time]):
            return jsonify({"error": "Missing data"}), 400

        # Encode voter_id as a numeric value using hashing
        voter_id_hash = int(hashlib.sha256(voter_id.encode('utf-8')).hexdigest(), 16) % (2**32 - 1)  # Limit size to fit float32

        # Ensure there are no NaN or infinity values
        if math.isinf(voter_id_hash) or math.isnan(voter_id_hash):
            return jsonify({"error": "Invalid data (infinity or NaN value)"}), 400

        # Prediksi suara menggunakan model
        prediction = model.predict([[voter_id_hash, candidate_id, vote_time]])

        # Tentukan status suara (Double Vote atau Valid Vote)
        result = "Double Vote" if prediction[0] == 1 else "Valid Vote"

        # Kirimkan hasil prediksi kembali
        return jsonify({"status": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
