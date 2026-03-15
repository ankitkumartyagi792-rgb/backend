from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import os

app = Flask(__name__)

# Allow your GitHub Pages frontend
CORS(app, origins=["https://ankitkumartyagi05.github.io"])

# Model paths
MODEL_PATH = os.path.join("model", "fraud_model.pkl")
VECTORIZER_PATH = os.path.join("model", "vectorizer.pkl")

model = None
vectorizer = None


# Load ML models
def load_models():
    global model, vectorizer
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        with open(VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)

        print("✅ Models loaded successfully")

    except Exception as e:
        print("❌ Error loading models:", e)


load_models()


# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


# URL extraction
def extract_urls(text):
    return re.findall(r"http[s]?://\S+", text)


# URL risk detection
def analyze_url(url):
    suspicious_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf", ".top", ".loan"]

    for tld in suspicious_tlds:
        if tld in url:
            return "Malicious"

    return "Suspicious"


# Health check route
@app.route("/")
def home():
    return "🚀 Fraud Detection API Running"


# Main prediction route
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded"}), 500

    # Clean text
    cleaned = clean_text(message)

    # Vectorize
    vec = vectorizer.transform([cleaned])

    # Prediction
    probability = model.predict_proba(vec)[0]
    fraud_prob = float(probability[1])

    classification = "Fraud" if fraud_prob > 0.5 else "Safe"

    # URL analysis
    detected_links = extract_urls(message)

    link_status = "None"

    if detected_links:
        link_status = analyze_url(detected_links[0])

    # Suspicious keywords
    suspicious_words = []

    fraud_keywords = [
        "urgent",
        "verify",
        "suspend",
        "blocked",
        "winner",
        "click",
        "pay",
        "lottery"
    ]

    for word in fraud_keywords:
        if word in cleaned:
            suspicious_words.append(word)

    result = {
        "classification": classification,
        "probability": round(fraud_prob, 2),
        "detected_links": detected_links,
        "link_status": link_status,
        "suspicious_words": suspicious_words
    }

    return jsonify(result)


# Railway compatible run
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
