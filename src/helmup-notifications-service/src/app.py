import os
import requests
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)
# Read tokens from environment variables

if WEBHOOK_URL is None:
    logger.error("WEBHOOK_URL env var can't be empty. Exiting...")
    exit(1)

@app.route('/event', methods=['POST'])
def handle_event_():
    try:
        payload = request.json
        message = payload.get('message', 'No message provided')
        logger.info(f"Starting to send the following message: {message}")
        # Send message to channel via webhook
        response = requests.post(WEBHOOK_URL, json={"text": message})

        if response.status_code != 200:
            raise ValueError(f"Request to notifications channel returned an error {response.status_code}, the response is:\n{response.text}")

        return jsonify({"status": "success", "data": message}), 200

    except Exception as e:
        logger.error({"status": "error", "data": str(e)})
        return jsonify({"status": "error", "data": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "alive"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
