from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Bitmap Wallet Analyzer backend is running."

@app.route("/wallet/<address>")
def get_wallet_data(address):
    try:
        url = f"https://open-api.unisat.io/v1/indexer/address/{address}/inscription-summary"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer f17b2e8795cc08181ac1d553868f31d7d9a5a78ba94a57568f0b2cc5b2c6bf72"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500
