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
import uuid, json

# Initializing Flask module and getting the env variable values.
app = Flask(__name__)
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
RPCUSER = os.environ.get("RPCUSER")
RPCPASS = os.environ.get("RPCPASS")
PORT = os.environ.get("DATAPIPORT")
RUN_PRODUCTION = os.environ.get("RUN_PRODUCTION")
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://",
# )

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

def getcurrentblockidentifier():
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getbestblockhash",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    req = requests.get(f"https://explorer.verus.io/api/getblock?hash={response_json['result']}")
    resp = req.json()['height']
    return response_json['result'], resp

def getgenesisblockidentifier():
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblockhash",
        "params": [0]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    req = requests.get(f"https://explorer.verus.io/api/getblock?hash={response_json['result']}")
    resp = req.json()['height']
    return response_json['result'], resp

def getcurrentblockheight():
    payload = {}
    data = send_request("GET", "https://explorer.verus.io/api/getblockcount", {'content-type': 'text/plain;'}, payload)
    return data

def getsyncstatus():
    hash0, height0 = getcurrentblockidentifier()
    height = getcurrentblockheight()
    calc = int(height) / int(height0)
    if calc == 1:
        syncstat = "Synced"
        boolean = True
    else:
        syncstat = "Out of sync, Syncing.."
        boolean = False
    return syncstat, height0, height, boolean

def getblocktimestamp():
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getinfo",
        "params": []
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    return response_json['result']["tiptime"]

# Gets the block information, takes in an argument called identifier which should be a transaction ID or a block number.
def get_block_info(identifier):
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblock",
        "params": [identifier]
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

def gettxamt(txid):
    txid = str(txid)
    cleaned_string = txid.replace("[", "").replace("]", "").replace("'", "")
    try:
        resp = requests.get(f"https://explorer.verus.io/ext/gettx/{cleaned_string}")
        amount = resp.json()['tx']['vin'][0]['amount']
        addr1 = resp.json()['tx']['vout'][0]['addresses']
        try:
            addr2 = resp.json()['tx']['vout'][1]['addresses']
        except IndexError:
            addr2 = addr1
    except KeyError:
        amount = None
        addr1 = None
        addr2 = None
    return amount, addr1, addr2

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
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_list():
    chain = get_network_status()
    newchainid = chain["chainid"]
    netinfo = {
  "network_identifiers":
  [
      {
          "blockchain":"VRSC",
          "network": newchainid,
          "sub_network_identifier":
          {
              "network": newchainid
          }
      }
              
  ]
              }
    errnetinfo = {
  "code": 12,
  "message": "Invalid account format",
  "description": "This error is returned when the requested AccountIdentifier is improperly formatted.",
  "retriable": "boolean",
  "details": None
}
    try:
        return jsonify(netinfo), 200
    except:
        return jsonify(errnetinfo), 500

# Endpoint that is used to get the network status.
@app.route('/network/status', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_status():
    data = request.get_json()
    try:
        hash, index = getcurrentblockidentifier()
        ghash, gindex = getgenesisblockidentifier()
        syncstat, height0, height, boolean = getsyncstatus()
        timestamp = getblocktimestamp()
        info = {
        "current_block_identifier": {
            "index": index,
            "hash": hash
        },
        "current_block_timestamp": 1582833600000,
        "genesis_block_identifier": {
            "index": gindex,
            "hash": ghash
        },
        "oldest_block_identifier": {
            "index": gindex,
            "hash": ghash
        },
        "sync_status": {
            "current_index": height,
            "target_index": height0,
            "stage": syncstat,
            "synced": boolean
        },
        "peers": [
            {
            "peer_id": uuid.uuid4(),
            "metadata": None
            }
        ]
        }
        return info, 200
    except:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch network version",
            "description": "There was an error while fetching network version from the RPC"
        }), 500


# Endpoint that is used to get network options.
@app.route('/network/options', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def network_options():
    nodeversion = get_network_options()
    chain = get_network_status()
    newchainid = chain["chainid"]
    try:
    # Add the specified text to the output
        versioninfo = {
        "version": {
        "rosetta_version": "1.2.5",
        "node_version": f'{nodeversion["version"]}',
        "middleware_version": "0.2.7",
        "metadata": None
    },
        "allow": {
        "operation_statuses": [
        {
            "status": "confirmed",
            "successful": True
        },
        {
            "status": "unconfirmed",
            "successful": True
        },
        {
            "status": "pubkey",
            "successful": True
        },
        ],
        "operation_types": [
        "Transfer",
        "mined"
        ],
        "errors": [
        {
            "code": 12,
            "message": "Invalid account format",
            "description": "This error is returned when the requested AccountIdentifier is improperly formatted.",
            "retriable": True,
            "details": None
        }, 
        {
            "code": 14,
            "message": "Failed to fetch network version",
            "description": "There was an error while fetching network version from the RPC",
            "retriable": True,
            "details": None
        },
        {
            "code": 16,
            "message": "Failed to fetch block information",
            "description": "There was an error while fetching block information from the RPC",
            "retriable": True,
            "details": None
        },
        {
            "code": 18,
            "message": "Failed to fetch transaction information",
            "description": "There was an error while fetching transaction information from the RPC",
            "retriable": True,
            "details": None
        },
        {
            "code": 20,
            "message": "Failed to fetch mempool information",
            "description": "There was an error while fetching mempool information from the RPC",
            "retriable": True,
            "details": None
        },
        {
            "code": 22,
            "message": "Failed to fetch balance information",
            "description": "There was an error while fetching balance information from the API",
            "retriable": True,
            "details": None
        },
        {
            "code": 24,
            "message": "Failed to fetch UTXOs",
            "description": "There was an error while fetching UTXOs from the API",
            "retriable": True,
            "details": None
        },
        {
            "code": 26,
            "message": "Failed to create new verus wallet address",
            "description": "There was an error while fetching the information from the Local RPC",
            "retriable": True,
            "details": None
        }
        ],
        "historical_balance_lookup": True,
        "timestamp_start_index": 1231006505,
        "call_methods": [
        "POST"
        ],
        "balance_exemptions": [
        {
            "sub_account_address": newchainid,
            "currency": {
            "symbol": "VRSC",
            "decimals": 8,
            "metadata": None
            },
            "exemption_type": "dynamic"
        }
        ],
        "mempool_coins": False
    }
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
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def block_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    block_identifier = data.get("block_identifier")
    try:
        index_value = data['block_identifier']['index']
    except:
        index_value = data['index']
    if not block_identifier:
        block_identifier = data.get("index")
    try:
        newblkidentifier = block_identifier['index']
        data = get_block_info(newblkidentifier)
    except:
        data = get_block_info(block_identifier)
    # data = json.dumps(block_data)
    try:
        txid = data['tx']
    except TypeError:
        txid = None
    hash_value = data['hash']
    height = data['height']
    time = data['time']
    blocktype = data['blocktype']
    confirmations = data['confirmations']
    if int(confirmations) > 15:
        status = "confirmed"
    else:
        status = "unconfirmed"
    finalsaplingroot = data['finalsaplingroot']
    try:
        value, addr1, addr2 = gettxamt(txid)
        newvalue = int(str(value).replace(".", ""))
    except:
        newvalue = "00000000"
    if addr1 == "" and addr2 == "":
        addr1 = "null"
        addr2 = "null"
    else:
        addr1 = addr1
        addr2 = addr2
    chain = get_network_status()
    newchainid = chain["chainid"]
    if data:
        data = {
        "block": {
            "block_identifier": {
            "index": index_value,
            "hash": hash_value
            },
            "parent_block_identifier": {
            "index": 0,
            "hash": finalsaplingroot
            },
            "timestamp": time,
            "transactions": [
            {
                "transaction_identifier": {
                "hash": str(txid)
                },
                "operations": [
                {
                    "operation_identifier": {
                    "index": 0,
                    "network_index": 0
                    },
                    "related_operations": [
                    {
                        "index": -3,
                        "network_index": 0
                    }
                    ],
                    "type": blocktype,
                    "status": status,
                    "account": {
                    "address": "iCRUc98jcJCP3JEntuud7Ae6eeaWtfZaZK",
                    "sub_account": {
                        "address": "iCRUc98jcJCP3JEntuud7Ae6eeaWtfZaZK",
                        "metadata": None
                    },
                    "metadata": None
                    },
                    "amount": {
                    "value": "10000000",
                    "currency": {
                        "symbol": "VRSC",
                        "decimals": 8,
                        "metadata": None
                    },
                    "metadata": None
                    },
                    "coin_change": {
                    "coin_identifier": {
                        "identifier": newchainid
                    },
                    "coin_action": "coin_spent"
                    },
                    "metadata": None
                }
                ],
                "related_transactions": [
                {
                    "network_identifier": {
                    "blockchain": "VRSC",
                    "network": newchainid,
                    "sub_network_identifier":
                    {
                        "network": newchainid,
                        "metadata": None
                    }
                    },
                    "transaction_identifier": {
                    "hash": str(txid)
                    },
                    "direction": "forward"
                }
                ],
                "metadata": None
            }
            ],
            "metadata": None
        },
        "other_transactions": [
            {
            "hash": str(txid)
            }
        ]
        }
        return jsonify(data), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch block information",
            "description": "There was an error while fetching block information from the RPC"
        }), 500


# Endpoint that is used to get the information about a block transaction.
@app.route('/block/transaction', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def block_transaction_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # Parse JSON data
    parsed_data = json.loads(json.dumps(data))
    # Access the desired hash value
    transaction_hash = parsed_data['transaction_identifier']['hash'][2:-2]  # Remove the square brackets and quotes
    transaction_data = get_transaction_info(transaction_hash)
    index_value = data['block_identifier']['index']
    try:
        amount = transaction_data['vout'][0]['value']
        txid = transaction_data["txid"]
        vout_addresses = []
        vout_types = []
        for vout_item in transaction_data['vout']:
            addresses = vout_item['scriptPubKey']['addresses']
            vout_type = vout_item['scriptPubKey']['type']
            vout_addresses.append(addresses)
            vout_types.append(vout_type)
    except TypeError:
        amount = "000000000"
        vout_addresses = None
        vout_types = None
        txid = None
    chain = get_network_status()
    newchainid = chain["chainid"]
    try:
        val = vout_types[0]
        addrv = vout_addresses[0]
        addrv2 = f"{vout_addresses[1]}" if len(vout_addresses) > 1 else f"{vout_addresses[0]}"
    except:
        val = "confirmed"
        addrv = "RMfrbs9eApM4VXV6htayiw1ks5WUGDvGtB"
        addrv2 = "RMfrbs9eApM4VXV6htayiw1ks5WUGDvGtB"
    if transaction_data:
        data = {
    "transaction": {
        "transaction_identifier": {
        "hash": str(txid)
        },
        "operations": [
        {
            "operation_identifier": {
            "index": 0,
            "network_index": 0
            },
            "related_operations": [
            {
                "index": -3,
                "network_index": 0
            }
            ],
            "type": "Transfer",
            "status": val,
            "account": {
            "address": str(addrv),
            "sub_account": {
                "address": addrv2,
                "metadata": None
            },
            "metadata": None
            },
            "amount": {
            "value": "10000000",
            "currency": {
                "symbol": "VRSC",
                "decimals": 8,
                "metadata": None
            },
            "metadata": None
            },
            "coin_change": {
            "coin_identifier": {
                "identifier": f"{txid}:0"
            },
            "coin_action": "coin_spent"
            },
            "metadata": None
        }
        ],
        "related_transactions": [
        {
            "network_identifier": {
            "blockchain": "VRSC",
            "network": newchainid,
            "sub_network_identifier": {
                "network": newchainid,
                "metadata": None
            }
            },
            "transaction_identifier": {
            "hash": str(txid)
            },
            "direction": "forward"
        }
        ],
        "metadata": None
    }
    }
        sub_account = data["transaction"]["operations"]
        for operation in sub_account:
            operation["account"]["sub_account"]["address"] = addrv2
        return jsonify(data), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch transaction information",
            "description": "There was an error while fetching transaction information from the RPC"
        }), 500


# Endpoint that is used to fetch mempool transactions.
@app.route('/mempool', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def mempool_info():
    mempool_data = get_mempool_info()
    if mempool_data:
        data = {
        "transaction_identifiers": [
            {
            "hash": mempool_data
            }
        ]
        }
        return jsonify(data), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch mempool information",
            "description": "There was an error while fetching mempool information from the RPC"
        }), 500


# Endpoint that is used to fetch an account's balance.
@app.route('/account/balance', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def account_balance():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    address = data['account_identifier']['address']
    balance_data = get_address_balance(address)
    index_value = data['block_identifier']['index']
    data = get_block_info(index_value)
    try:
        value_sat = balance_data['vout'][0]['valueSat']
        hash = data['tx']
    except:
        value_sat = "00000000"
        hash = "0000000000000000000000000000000000000000000000000000000000000000"
    if balance_data:
        data = {
        "block_identifier": {
            "index": index_value,
            "hash": str(hash)
        },
        "balances": [
            {
            "value": f"{value_sat}",
            "currency": {
                "symbol": "VRSC",
                "decimals": 8,
                "metadata": None
            },
            "metadata": None
            }
        ],
        "metadata": None
        }
        print(data)
        return jsonify(data), 200
    else:
        return jsonify({
            "code": 500,
            "message": "Failed to fetch balance information",
            "description": "There was an error while fetching balance information from the API"
        }), 500


# Endpoint that is used to fetch the unspend amount of coins/transaction in an account.
@app.route('/account/coins', methods=['POST'])
#@limiter.limit("2 per 5 minutes", override_defaults=False)
def account_coins():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    address = data.get("address")

    if not address:
        return jsonify({"error": "Address not provided"}), 400

    utxos_data = get_address_utxos(address)
    heights = [entry['height'] for entry in utxos_data]
    txids = [entry['txid'] for entry in utxos_data]
    satoshis = [entry['satoshis'] for entry in utxos_data]
    chain = get_network_status()
    newchainid = chain["chainid"]
    if utxos_data:
        data = {
        "block_identifier": {
            "index": heights,
            "hash": txids
        },
        "coins": [
            {
            "coin_identifier": {
                "identifier": newchainid
            },
            "amount": {
                "value": satoshis,
                "currency": {
                "symbol": "VRSC",
                "decimals": 8,
                "metadata": None
                },
                "metadata": None
            }
            }
        ],
        "metadata": None
        }
        return jsonify(data), 200
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
        print("Verus Rosetta DataAPI running on port 5500 in production mode...")
        app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(PORT)), app)
        app_server.serve_forever()
    else:
        print("Please set the RUN_PRODUCTION variable as True or False, Running the API in development mode since the variable is not set...")
        app.run(host='0.0.0.0', port=PORT, debug=True)
