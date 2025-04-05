from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Laat alle domeinen toe voor fetch-verzoeken

# UniSat API-key (beveiligd in backend)
UNISAT_API_KEY = "f17b2e8795cc08181ac1d553868f31d7d9a5a78ba94a57568f0b2cc5b2c6bf72"
UNISAT_API_URL = "https://open-api.unisat.io/v1/indexer/address/{}/inscriptions"

@app.route('/api/inscriptions')
def get_inscriptions():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Missing address"}), 400

    url = UNISAT_API_URL.format(address)
    headers = {
        "Authorization": f"Bearer {UNISAT_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)