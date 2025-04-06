from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)  # Laat alle domeinen toe voor fetch-verzoeken

# Stel logging in met meer detail
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# UniSat API-key uit omgevingsvariabele
UNISAT_API_KEY = os.getenv("UNISAT_API_KEY")
if not UNISAT_API_KEY:
    logger.error("UNISAT_API_KEY environment variable is not set")
    raise ValueError("UNISAT_API_KEY environment variable is required")
UNISAT_API_URL = "https://open-api.unisat.io/v1/indexer/address/{}/inscription-data?cursor=0&size=100"  # Nieuwe endpoint

# Root route om "Not Found" te voorkomen
@app.route('/')
def home():
    logger.info("Root route accessed")
    return jsonify({"message": "Welcome to Bitmap Backend! Visit /wallet-analyzer to use the app, or use /api/inscriptions to fetch data."})

# Route om de frontend te serveren
@app.route('/wallet-analyzer')
def wallet_analyzer():
    logger.info("Wallet analyzer route accessed")
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return jsonify({"error": "Failed to load frontend", "details": str(e)}), 500

# API-endpoint om inscripties op te halen
@app.route('/api/inscriptions')
def get_inscriptions():
    address = request.args.get("address")
    if not address:
        logger.warning("Missing address parameter in /api/inscriptions request")
        return jsonify({"error": "Missing address"}), 400

    logger.info(f"Fetching inscriptions for address: {address}")
    url = UNISAT_API_URL.format(address)
    logger.info(f"Using UniSat API endpoint: {url}")  # Log de gebruikte URL
    headers = {
        "Authorization": f"Bearer {UNISAT_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched inscriptions for address: {address}")
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching inscriptions: {str(e)}")
        # Fallback data
        fallback_data = {
            "data": {
                "inscriptions": [
                    {
                        "inscriptionId": "840bc0df4ffc5a7ccedbee35e97506c9577160e233982e627d0045d06366e362i0",
                        "content": "example.bitmap",
                        "blockHeight": 862165
                    },
                    {
                        "inscriptionId": "b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8b7e8i0",
                        "content": "another.bitmap",
                        "blockHeight": 890513
                    }
                ]
            }
        }
        logger.info("Using fallback data due to API failure")
        return jsonify(fallback_data)

# API-endpoint om children op te halen
@app.route('/api/children')
def get_children():
    inscription_id = request.args.get("inscription_id")
    if not inscription_id:
        logger.warning("Missing inscription_id parameter in /api/children request")
        return jsonify({"error": "Missing inscription_id"}), 400

    logger.info(f"Fetching children for inscription_id: {inscription_id}")
    try:
        response = requests.get(f"https://ordinals.com/r/children/{inscription_id}")
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched children for inscription_id: {inscription_id}")
        return jsonify({"data": data})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching children: {str(e)}")
        return jsonify({"error": "API request failed", "details": str(e)}), 500

# API-endpoint om content op te halen
@app.route('/api/content')
def get_content():
    inscription_id = request.args.get("inscription_id")
    if not inscription_id:
        logger.warning("Missing inscription_id parameter in /api/content request")
        return jsonify({"error": "Missing inscription_id"}), 400

    logger.info(f"Fetching content for inscription_id: {inscription_id}")
    try:
        response = requests.get(f"https://ordinals.com/r/content/{inscription_id}")
        response.raise_for_status()
        data = response.text
        logger.info(f"Successfully fetched content for inscription_id: {inscription_id}")
        return jsonify({"data": data})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content: {str(e)}")
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask app locally")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
