from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)  # Laat alle domeinen toe voor fetch-verzoeken

# Stel logging in
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UniSat API-key uit omgevingsvariabele (met fallback voor lokale tests)
UNISAT_API_KEY = os.getenv("UNISAT_API_KEY", "f17b2e8795cc08181ac1d553868f31d7d9a5a78ba94a57568f0b2cc5b2c6bf72")
UNISAT_API_URL = "https://open-api.unisat.io/v1/indexer/address/{}/inscriptions"

# Root route om "Not Found" te voorkomen
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Bitmap Backend! Visit /wallet-analyzer to use the app, or use /api/inscriptions to fetch data."})

# Route om de frontend te serveren
@app.route('/wallet-analyzer')
def wallet_analyzer():
    return render_template('index.html')

# API-endpoint om inscripties op te halen
@app.route('/api/inscriptions')
def get_inscriptions():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Missing address"}), 400

    logger.info(f"Fetching inscriptions for address: {address}")
    url = UNISAT_API_URL.format(address)
    headers = {
        "Authorization": f"Bearer {UNISAT_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching inscriptions: {str(e)}")
        return jsonify({"error": "API request failed", "details": str(e)}), 500

# API-endpoint om children op te halen
@app.route('/api/children')
def get_children():
    inscription_id = request.args.get("inscription_id")
    if not inscription_id:
        return jsonify({"error": "Missing inscription_id"}), 400

    logger.info(f"Fetching children for inscription_id: {inscription_id}")
    try:
        response = requests.get(f"https://ordinals.com/r/children/{inscription_id}")
        response.raise_for_status()
        return jsonify({"data": response.json()})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching children: {str(e)}")
        return jsonify({"error": "API request failed", "details": str(e)}), 500

# API-endpoint om content op te halen
@app.route('/api/content')
def get_content():
    inscription_id = request.args.get("inscription_id")
    if not inscription_id:
        return jsonify({"error": "Missing inscription_id"}), 400

    logger.info(f"Fetching content for inscription_id: {inscription_id}")
    try:
        response = requests.get(f"https://ordinals.com/r/content/{inscription_id}")
        response.raise_for_status()
        return jsonify({"data": response.text})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content: {str(e)}")
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
