# Verus Network Construction API
# Used to provide data for rosetta integration 
# Coded by Shreyas from the verus community


# Module imports.
from flask import Flask, jsonify, request, render_template
import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import gevent.pywsgi

# Initializing Flask module and getting the env variable values.
app = Flask(__name__)
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
PORT = os.environ.get("CONSTAPIPORT")
RUN_PRODUCTION = os.environ.get("RUN_PRODUCTION")
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Function definitions.

# Helps to send the request to the RPC.
def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Helps to create a new verus address
def getnewaddress():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getnewaddress",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    return response_json


# Helps to create an unsigned raw transaction, takes in a few arguments to create a transaction.
def create_unsigned_transaction(txid, vout, address, amount):
    request_data = {
        "jsonrpc": "1.0",
        "id": "flask-app",
        "method": "createrawtransaction",
        "params": [
            [{"txid": txid, "vout": vout}],
            {address: amount}
        ]
    }
    try:
        result = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, request_data)
        unsigned_transaction = result.get("transaction")
        return unsigned_transaction
    except Exception as e:
        raise Exception(f"Failed to create unsigned transaction: {str(e)}")


# Helps to parse, verify and sign the unsigned raw transaction, takes in an argument called hex.
def parse_and_sign_transaction(unsigned_hex):

    request_data = {
        "jsonrpc": "1.0",
        "id": "flask-app",
        "method": "signrawtransaction",
        "params": [unsigned_hex]
    }

    try:
        result = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, request_data)
        return result
    except Exception as e:
        raise Exception(f"Failed to parse and sign transaction: {str(e)}")


# Helps to broadcast a signed raw transaction into the network, takes in an argument called hex (signed hex).
def submit_signed_transaction(signed_hex):
    request_data = {
        "jsonrpc": "1.0",
        "id": "flask-app",
        "method": "sendrawtransaction",
        "params": [signed_hex]
    }

    try:
        result = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, request_data)
        return result
    except Exception as e:
        raise Exception(f"Failed to submit signed transaction: {str(e)}")

# API Endpoints

# Endpoint that is used to get a new verus address.
@app.route('/construction/derive', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_status():
    data = getnewaddress()

    if data:
        return jsonify({"address": data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to create new verus wallet address",
            "description": "There was an error while fetching the information from the Local RPC"
        }), 500


# Endpoint that is used to create a raw unsigned transaction.
@app.route('/construction/payloads', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def create_unsigned_transaction_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    txid = data.get("txid")
    vout = data.get("vout")
    address = data.get("address")
    amount = data.get("amount")

    if not txid or not vout or not address or not amount:
        return jsonify({"error": "Invalid arguments"}), 400

    try:
        unsigned_transaction = create_unsigned_transaction(txid, vout, address, amount)
        return jsonify({"transaction": unsigned_transaction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint that is used to verify and sign a raw unsigned transaction.
@app.route('/construction/parse', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def parse_and_sign_transaction_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    unsigned_hex = data.get("unsigned_hex")

    if not unsigned_hex:
        return jsonify({"error": "Unsigned hex not provided"}), 400

    try:
        result = parse_and_sign_transaction(unsigned_hex)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint that is used to broadcast a signed transaction into the blockchain.
@app.route('/construction/submit', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def submit_signed_transaction_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    signed_hex = data.get("signed_hex")

    if not signed_hex:
        return jsonify({"error": "Signed hex not provided"}), 400

    try:
        result = submit_signed_transaction(signed_hex)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the API
if __name__ == '__main__':
    # Only use the debug=True in development environment.
    # Use WSGI to run the API in production environment.
    if RUN_PRODUCTION == "False":
        app.run(host='0.0.0.0', port=PORT, debug=True)
    elif RUN_PRODUCTION == "True":
        app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', PORT), app)
        app_server.serve_forever()
    else:
        print("Please set the RUN_PRODUCTION variable as True or False, Running the API in development mode since the variable is not set...")
        app.run(host='0.0.0.0', port=PORT, debug=True)
