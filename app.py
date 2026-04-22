from flask import Flask, request, jsonify
import pandas as pd
from model import recommend_jobs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# تحميل الداتا
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "job_descriptions.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")
jobs_df = pd.read_csv(csv_path)

@app.route("/")
def home():
    return {"message": "AI Job Recommendation API Running"}

# Text API
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    if not data or "cv_text" not in data:
        return jsonify({"error": "cv_text is required"}), 400

    results = recommend_jobs(data["cv_text"], jobs_df)

    return jsonify(results)

# File Upload API
@app.route("/recommend-file", methods=["POST"])
def recommend_file():
    if "cv" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["cv"]
    text = file.read().decode("utf-8", errors="ignore")

    results = recommend_jobs(text, jobs_df)

    return jsonify(results)

import logging
logging.basicConfig(level=logging.INFO)

# Health check
@app.route("/health")
def health():
    return {"status": "ok"}

# بدل السطر ده
if __name__ == "__main__":
    app.run(debug=True)

# حط السطر ده في الآخر (بره الـ if)
application = app  # Gunicorn هيستخدم الـ application
