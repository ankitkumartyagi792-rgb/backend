from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import os

app = Flask(__name__)
# CORS is required to allow Frontend (different port) to talk to Backend
CORS(app) 

# Load Model and Vectorizer
MODEL_PATH = 'model/fraud_model.pkl'
VECTORIZER_PATH = 'model/vectorizer.pkl'

model = None
vectorizer = None

def load_models():
    global model, vectorizer
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        print("Models loaded successfully.")
    except FileNotFoundError:
        print("Model files not found. Please run train_model.py first.")

load_models()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def extract_urls(text):
    # Simple regex for URLs
    return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

def analyze_url(url):
    # Simple rule-based URL check
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.top', '.loan']
    for tld in suspicious_tlds:
        if tld in url:
            return "Malicious"
    return "Suspicious"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # 1. Clean and Vectorize
    cleaned = clean_text(message)
    if vectorizer is None or model is None:
        return jsonify({'error': 'Model or vectorizer not loaded'}), 500
    vec = vectorizer.transform([cleaned])
    
    # 2. Predict
    probability = model.predict_proba(vec)[0]
    fraud_prob = float(probability[1]) # Probability of class 1 (Fraud)
    
    # 3. Determine Classification
    classification = "Fraud" if fraud_prob > 0.5 else "Safe"
    
    # 4. Extra Analysis (URLs)
    detected_links = extract_urls(message)
    link_status = "None"
    if detected_links:
        link_status = analyze_url(detected_links[0])

    # 5. Suspicious Keywords Extraction (Simple logic)
    suspicious_words = []
    fraud_keywords = ['urgent', 'verify', 'suspend', 'blocked', 'winner', 'click', 'pay', 'lottery']
    for word in fraud_keywords:
        if word in cleaned:
            suspicious_words.append(word)

    response = {
        'classification': classification,
        'probability': round(fraud_prob, 2),
        'detected_links': detected_links,
        'link_status': link_status,
        'suspicious_words': suspicious_words
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)