from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bitmap Wallet Analyzer backend is running.'

@app.route('/wallet/<address>')
def get_wallet_data(address):
    try:
        # UniSat API (alternatief: OpenOrdex of anderen)
        url = f"https://openordex.org/api/inscriptions?address={address}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": "Fout bij ophalen van data via OpenOrdex."}), 500

        data = response.json()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
