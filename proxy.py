from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

UNISAT_API_KEY = os.getenv("UNISAT_API_KEY")

@app.route('/')
def home():
    return "Bitmap Wallet Analyzer backend is running."

@app.route('/api/inscriptions', methods=['GET'])
def get_inscriptions():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "No address provided"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {UNISAT_API_KEY}"
        }

        url = f"https://open-api.unisat.io/v1/indexer/address/{address}/brc20/summary"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
