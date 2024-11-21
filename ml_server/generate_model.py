import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import hashlib
import math
import joblib  # Import joblib untuk menyimpan model

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

# Membagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Melatih model machine learning (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediksi pada data uji
y_pred = model.predict(X_test)

# Menghitung akurasi dan metrik evaluasi lainnya
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred, zero_division=1)

print("Akurasi Model: ", accuracy)
print("Laporan Klasifikasi:\n", class_report)

# Menyimpan model ke dalam file menggunakan joblib
joblib.dump(model, 'random_forest_model.joblib')

# Atau Anda bisa menggunakan pickle, jika lebih familiar dengan itu
# import pickle
# with open('random_forest_model.pkl', 'wb') as file:
#     pickle.dump(model, file)

