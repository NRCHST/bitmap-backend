from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bitmap Wallet Analyzer backend is running."

@app.route('/api/analyze', methods=['POST'])
def analyze_wallet():
    data = request.get_json()
    address = data.get("address")

    if not address:
        return jsonify({"error": "Walletadres ontbreekt"}), 400

    # Roep externe UniSat API aan
    url = f"https://open-api.unisat.io/v1/indexer/address/{address}/brc20/summary"
    headers = {
        "accept": "application/json"
        # Voeg indien nodig hier een API-key toe
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Externe API faalde"}), 500

    return jsonify(response.json())
