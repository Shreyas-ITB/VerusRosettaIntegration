# Verus Network Data API
# Used to provide data for rosetta integration 
# Coded by Shreyas and Shreya S from the verus community


# Module imports.
from flask import Flask, jsonify, request
import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import gevent.pywsgi
import uuid

# Initializing Flask module and getting the env variable values.
app = Flask(__name__)
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
RPCUSER = os.environ.get("RPCUSER")
RPCPASS = os.environ.get("RPCPASS")
PORT = os.environ.get("DATAPIPORT")
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
    response = requests.request(method, url, headers=headers, json=data, auth=(RPCUSER, RPCPASS))
    response.raise_for_status()
    return response.json()


# Fetches the network options from the RPC.
def get_network_options():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getnetworkinfo",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        # Parse the response JSON and extract relevant information
        network_status = {
            "version": response_json["result"]["version"],
            "subversion": response_json["result"]["subversion"],
            "protocolversion": response_json["result"]["protocolversion"],
            "localservices": response_json["result"]["localservices"],
            "timeoffset": response_json["result"]["timeoffset"],
            "connections": response_json["result"]["connections"],
            "networks": [
                {
                    "name": network["name"],
                    "limited": network["limited"],
                    "reachable": network["reachable"],
                    "proxy": network.get("proxy", "")
                }
                for network in response_json["result"]["networks"]
            ],
            "relayfee": response_json["result"]["relayfee"],
            "localaddresses": [
                {
                    "address": address["address"],
                    "port": address["port"],
                    "score": address["score"]
                }
                for address in response_json["result"]["localaddresses"]
            ],
            "warnings": response_json["result"].get("warnings", "")
        }

        return network_status
    else:
        # Handle the error case
        return None


# Fetches the network status from the RPC.
def get_network_status():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblockchaininfo",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        # Parse the response JSON and extract relevant information
        blockchain_info = response_json["result"]

        network_options = {
            "chain": blockchain_info["chain"],
            "name": blockchain_info["name"],
            "chainid": blockchain_info["chainid"],
            "blocks": blockchain_info["blocks"],
            "headers": blockchain_info["headers"],
            "bestblockhash": blockchain_info["bestblockhash"],
            "difficulty": blockchain_info["difficulty"],
            "verificationprogress": blockchain_info["verificationprogress"],
            "chainwork": blockchain_info["chainwork"],
            "chainstake": blockchain_info["chainstake"],
            "pruned": blockchain_info["pruned"],
            "size_on_disk": blockchain_info["size_on_disk"],
            "commitments": blockchain_info["commitments"],
            "valuePools": [
                {
                    "id": pool["id"],
                    "monitored": pool["monitored"],
                    "chainValue": pool["chainValue"],
                    "chainValueZat": pool["chainValueZat"]
                }
                for pool in blockchain_info.get("valuePools", [])
            ],
            "softforks": blockchain_info.get("softforks", []),
            "upgrades": blockchain_info.get("upgrades", {}),
            "consensus": blockchain_info.get("consensus", {})
        }

        return network_options
    else:
        # Handle the error case
        return None


# Fetches the network versions from the RPC.
def get_network_version():
    try:
        blockchain_info = get_network_options()
        network_version = {
        "rosetta_version": "1.2.5",
        "node_version": blockchain_info["version"],
        "sub_version": blockchain_info["subversion"],
        "protocol_version": blockchain_info["protocolversion"],
        "middleware_version": "0.2.7",
        "metadata": None
    }
        return network_version
    except:
        return None

def getcurrentblockindex():
    payload = {}
    data = send_request("GET", "https://explorer.verus.io/api/getblockcount", {'content-type': 'text/plain;'}, payload)
    return data

# Gets the block information, takes in an argument called identifier which should be a transaction ID or a block number.
def get_block_info(identifier):
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblock",
        "params": [f"{identifier}"]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        block_info = response_json["result"]

        return block_info
    elif "error" in response_json:
        return response_json["error"]["message"]
    else:
        return None


# Gets the transaction information, takes in an argument called transaction ID.
def get_transaction_info(txid):
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getrawtransaction",
        "params": [txid, 1]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        transaction_info = response_json["result"]

        return transaction_info
    elif "error" in response_json:
        return response_json["error"]["message"]
    else:
        return None


# Gets all the unconfirmed transactions from the mempool.
def get_mempool_info():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getrawmempool",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        mempool_info = response_json["result"]

        return mempool_info
    else:
        # Handle the error case
        return None


# Gets the balance of an address, takes in an argument called address.
def get_address_balance(address):
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getaddressbalance",
        "params": [{"addresses": [address]}]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        balance_info = response_json["result"]

        return balance_info
    elif "error" in response_json:
        return response_json["error"]["message"]
    else:
        return None


# Gets the unspent transactions of an address, takes in an argument called address.
def get_address_utxos(address):
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getaddressutxos",
        "params": [{"addresses": [address]}]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

    # Check if the request was successful
    if "result" in response_json:
        utxos = response_json["result"]

        return utxos
    elif "error" in response_json:
        return response_json["error"]["message"]
    else:
        return None


# API Endpoints

# Endpoint that is used to get the network lists.
@app.route('/network/list', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_list():
    netinfo = {
  "network_identifiers": [
    {
      "blockchain": "verus",
      "network": "local rpc",
      "sub_network_identifier": {
        "network": "local shard",
        "metadata": None
      }
    }
  ]
}
    errnetinfo = {
  "code": 12,
  "message": "Infoerror",
  "description": "error getting the information",
  "retriable": True,
  "details": None
}
    try:
        return jsonify(netinfo), 200
    except:
        return jsonify(errnetinfo), 500

# Endpoint that is used to get the network status.
@app.route('/network/status', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_status():
    data = request.get_json()
    status_data = get_network_status()
    newdata = getcurrentblockindex()

    if status_data:
        outdata = {
  "current_block_identifier": {
    "index": status_data["blocks"],
    "hash": status_data["bestblockhash"]
  },
  "current_block_timestamp": 1582833600000,
  "genesis_block_identifier": {
    "index": status_data["blocks"],
    "hash": status_data["bestblockhash"]
  },
  "oldest_block_identifier": {
    "index": status_data["blocks"],
    "hash": status_data["bestblockhash"]
  },
  "sync_status": {
    "current_index": newdata,
    "target_index": newdata,
    "stage": "header sync",
    "synced": True
  },
  "peers": [
    {
      "peer_id": uuid.uuid4(),
      "metadata": None
    }
  ]
}
        return jsonify(outdata), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch network status",
            "description": "There was an error while fetching network status from the RPC"
        }), 500


# Endpoint that is used to get network options.
@app.route('/network/options', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_options():
    # Fetch network options from your API
    options_data = get_network_options()

    if options_data:
        return jsonify({"network_options": options_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch network options",
            "description": "There was an error while fetching network options from the RPC"
        }), 500


# Endpoint that is used to get the version information.
@app.route('/network/rosetta/version', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_rosetta_version():
    try:
    # Add the specified text to the output
        versioninfo = {
    "rosetta_version": "1.2.5",
    "node_version": "1.0.2",
    "middleware_version": "0.2.7",
    "metadata": {}
    }
        return jsonify(versioninfo), 200
    except:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch network version",
            "description": "There was an error while fetching network version from the RPC"
        }), 500


# Endpoint that is used to get the information of a block.
@app.route('/block', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def block_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    block_identifier = data.get("block_identifier")

    if not block_identifier:
        return jsonify({"error": "Block identifier not provided"}), 400

    block_data = get_block_info(block_identifier)

    if block_data:
        return jsonify({"block_info": block_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch block information",
            "description": "There was an error while fetching block information from the RPC"
        }), 500


# Endpoint that is used to get the information about a block transaction.
@app.route('/block/transaction', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def block_transaction_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    txid = data.get("transaction_id")

    if not txid:
        return jsonify({"error": "Transaction ID not provided"}), 400

    transaction_data = get_transaction_info(txid)

    if transaction_data:
        return jsonify({"transaction_info": transaction_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch transaction information",
            "description": "There was an error while fetching transaction information from the RPC"
        }), 500


# Endpoint that is used to fetch mempool transactions.
@app.route('/mempool', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def mempool_info():
    mempool_data = get_mempool_info()
    if mempool_data:
        return jsonify({"mempool_info": mempool_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch mempool information",
            "description": "There was an error while fetching mempool information from the RPC"
        }), 500


# Endpoint that is used to fetch an account's balance.
@app.route('/account/balance', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def account_balance():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    address = data.get("address")

    if not address:
        return jsonify({"error": "Address not provided"}), 400

    balance_data = get_address_balance(address)

    if balance_data:
        return jsonify({"balance_info": balance_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch balance information",
            "description": "There was an error while fetching balance information from the API"
        }), 500


# Endpoint that is used to fetch the unspend amount of coins/transaction in an account.
@app.route('/account/coins', methods=['POST'])
@limiter.limit("2 per 5 minutes", override_defaults=False)
def account_coins():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    address = data.get("address")

    if not address:
        return jsonify({"error": "Address not provided"}), 400

    utxos_data = get_address_utxos(address)

    if utxos_data:
        return jsonify({"utxos": utxos_data}), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch UTXOs",
            "description": "There was an error while fetching UTXOs from the API"
        }), 500

@app.route('/call', methods=['POST'])
def call_rpc():
    try:
        data = request.get_json()
        # Check if the request has the necessary parameters
        if not data or "method" not in data:
            return jsonify({"error": "Invalid request. 'method' is a mandatory parameter."}), 400

        # Extract parameters from the request
        method = data["method"]
        parameter = data.get("parameter")
        payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": method,
        "params": parameter if parameter else []
    }
        # Call the send_request function to make a request to your RPC
        response = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)

        # Return the response from your RPC
        return jsonify(response), 200

    except requests.exceptions.RequestException as rpc_error:
        return jsonify({"error": str(rpc_error)}), 500

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
