# Verus Network Data API
# Used to provide data for rosetta integration 
# Coded by Shreyas from the verus community
# Coinbase Docs: https://docs.cloud.coinbase.com/rosetta/docs/welcome
# Github: https://github.com/Shreyas-ITB/VerusRosettaIntegration


# Module imports.
# from flask import Flask, jsonify, request
from fastapi import FastAPI, Request, HTTPException
import os
import requests
from dotenv import load_dotenv, find_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import uvicorn
import json

# Initializing Flask module and getting the env variable values.
# app = Flask(__name__)
app = FastAPI()
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
RPCUSER = os.environ.get("RPCUSER")
RPCPASS = os.environ.get("RPCPASS")
PORT = os.environ.get("APIPORT")
RUN_PRODUCTION = os.environ.get("RUN_PRODUCTION")

# Initialize the rate limiter only in production mode
if RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
    )
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)
else: 
    None
    

# Create a dictionary to save all the balance related data for temporary use
baldata = []

# Function definitions.

# Helps to send the request to the RPC.
def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data, auth=(RPCUSER, RPCPASS), timeout=10000)
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
    # Define the JSON-RPC request payload
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
    # Define the JSON-RPC request payload
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
        }
        return network_options
    else:
        # Handle the error case
        return None

# Get the current block identifier
def getcurrentblockidentifier():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getbestblockhash",
        "params": []
    }
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    return response_json['result']

# Get genesis block identifier
def getgenesisblockidentifier():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblockhash",
        "params": [0]
    }

    # Make the request using the provided function
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    resp = get_block_info(response_json['result'])
    resp = resp['height']
    return response_json['result'], resp

# Get current block height 
def getcurrentblockheight():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getblockchaininfo",
        "params": []
    }
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    return int(response_json["result"]["blocks"])

def getpeerinfo():
    # Define the JSON-RPC request payload
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getpeerinfo",
        "params": []
    }
    response_json = send_request("POST", RPCURL, {'content-type': 'text/plain;'}, payload)
    formatted_data = []
    for item in response_json['result']:
        item_id = item.pop('id')  # Extract and remove the 'id' key from the dictionary
        formatted_data.append({'id': item_id, 'data': item})

    formatted_json = json.dumps(formatted_data, indent=2)
    formatted_data = json.loads(formatted_json)

    ids = [item['id'] for item in formatted_data]
    data_without_id = [item['data'] for item in formatted_data]
    return ids


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

# Get current block identifier height from a hash
def getcurrentblockidentifierheight(hash):
    resp = get_block_info(hash)
    resp = resp['height']
    return resp

# Get the syncing status
def getsyncstatus():
    # Calculate the block sync status
    hash0 = getcurrentblockidentifier()
    height0 = getcurrentblockidentifierheight(hash0)
    height = getcurrentblockheight()
    calc = int(height) / int(height0)
    if calc == 1:
        syncstat = "Synced"
        boolean = True
    else:
        syncstat = "Out of sync, Syncing.."
        boolean = False
    return syncstat, height0, height, boolean

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

# Get transaction amount from a transaction id
def gettxamt(txid):
    txid = str(txid)
    cleaned_string = txid.replace("[", "").replace("]", "").replace("'", "")
    try:
        # resp = requests.get(f"https://explorer.verus.io/ext/gettx/{cleaned_string}")
        # amount = resp.json()['tx']['vin'][0]['amount']
        # addr1 = resp.json()['tx']['vout'][0]['addresses']
        # try:
        #     addr2 = resp.json()['tx']['vout'][1]['addresses']
        # except IndexError:
        #     addr2 = addr1
        transaction = get_transaction_info(cleaned_string)
        # Extract valueSat from each vout
        valuesats = [vout["valueSat"] for vout in transaction["vout"]]

        # Extract addresses from scriptPubKey for the first two vouts
        addresses = [vout["scriptPubKey"]["addresses"] for vout in transaction["vout"][:2]]
        amount = valuesats
        addr1 = addresses[0][0]
        try:
            addr2 = addresses[1][0]
        except IndexError:
            addr2 = addr1
    except:
        amount = "00000000"
        addr1 = "iCRUc98jcJCP3JEntuud7Ae6eeaWtfZaZK"
        addr2 = "iCRUc98jcJCP3JEntuud7Ae6eeaWtfZaZK"
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
@app.post('/network/list')
async def network_list():
    # request chainid from the vrsc daemon
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
    # error message for /network/list endpoint
    errnetinfo = {  
  "code": 12,
  "message": "Invalid account format",
  "description": "This error is returned when the requested AccountIdentifier is improperly formatted.",
  "retriable": "boolean",
  "details": None
}
    try:
        return netinfo
    except:
        return HTTPException(status_code=500, detail=errnetinfo)

# Endpoint that is used to get the network status.
@app.post('/network/status')
async def network_status(request: Request):
    data = await request.json()
    if data:
        ids = getpeerinfo()
        hashhe = get_block_info(1500)
        hash = getcurrentblockidentifier()
        indexval = getcurrentblockidentifierheight(hash)
        ghash, gindex = getgenesisblockidentifier()
        syncstat, height0, height, boolean = getsyncstatus()
        if RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
            hash = hash
            indexval = indexval
        else:
            hash = hash
            indexval = indexval
        timestamp = hashhe['time']
        milliseconds = timestamp * 1000
        info = {
        "current_block_identifier": {
            "index": indexval,
            "hash": hash
        },
        "current_block_timestamp": milliseconds,
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
            "peer_id": str(ids),
            "metadata": None
            }
        ]
        }
        return info
    else:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": "Failed to fetch network version",
            "description": "There was an error while fetching network version from the RPC"
        })


# Endpoint that is used to get network options.
@app.post('/network/options')
async def network_options():
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
            "status": "processing",
            "successful": True
        },
        {
            "status": "pubkey",
            "successful": True
        },
        ],
        "operation_types": [
        "Transfer",
        "mined",
        "minted"
        "pubkey"
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
        return versioninfo
    except Exception as e:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": f"Failed to fetch network version: {e}",
            "description": "There was an error while fetching network version from the RPC"
        })


# Endpoint that is used to get the information of a block.
@app.post('/block')
async def block_info(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})

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
    value, addr1, addr2 = gettxamt(txid)
    chain = get_network_status()
    newchainid = chain["chainid"]
    if index_value == 0:
        newindexv = 0
    else:
        newindexv = index_value - 1
    parent_hash = get_block_info(newindexv)
    parent_hash = parent_hash['hash']
    RUN_PRODUCTION = os.environ.get("RUN_PRODUCTION")
    if RUN_PRODUCTION == True or RUN_PRODUCTION == "true":
        value = int(str(value).replace(".", ""))
    else:
        value = "00000000"
    if data:
        data = {
        "block": {
            "block_identifier": {
            "index": index_value,
            "hash": hash_value
            },
            "parent_block_identifier": {
            "index": newindexv,
            "hash": parent_hash
            },
            "timestamp": time,
            "transactions": [
            {
                "transaction_identifier": {
                "hash": str(txid[:1])
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
                    "status": status,
                    "account": {
                    "address": addr1,
                    "sub_account": {
                        "address": addr2,
                        "metadata": None
                    },
                    "metadata": None
                    },
                    "amount": {
                    "value": f"{value}",
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
                    "hash": str(txid[:1])
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
            "hash": str(txid[:1])
            }
        ]
        }
        return data
    else:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": "Failed to fetch block information",
            "description": "There was an error while fetching block information from the RPC"
        })


# Endpoint that is used to get the information about a block transaction.
@app.post('/block/transaction')
async def block_transaction_info(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})
    # Parse JSON data
    parsed_data = json.loads(json.dumps(data))
    # Access the desired hash value
    try:
        chain = get_network_status()
        newchainid = chain["chainid"]
        transaction_hash = parsed_data['transaction_identifier']['hash'][2:-2]  #Remove the square brackets and quotes
        if transaction_hash == "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b":
            txid = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
            if RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
                value = "500000000"
            else:
                value = "00000000"
            address = "RJJBTXXfgE5DjiPQpZSnYrQe73NhrBZ3ao"
            status = "confirmed"
        else:
            # Split the variable by comma, strip whitespace, and remove single quotes
            strings = [s.strip().strip("'") for s in transaction_hash.split(',')]

            # Check the length of the list
            if len(strings) > 1:
                result = strings[0]  # Return the first string
            else:
                result = transaction_hash.strip("'")
            data = get_transaction_info(result)
            # Extracting values
            txid = data["txid"]
            if RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
                value = data["vout"][0]["valueSat"]
            else:
                value = "00000000"
            try:
                address = data["vout"][0]["scriptPubKey"]["addresses"]
            except:
                address = "RJJBTXXfgE5DjiPQpZSnYrQe73NhrBZ3ao"
            confirmations = data["confirmations"]
            # Checking confirmations and setting status
            status = "confirmed" if confirmations > 100 else "unconfirmed"
        senddata = {
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
                    "status": status,
                    "account": {
                    "address": str(address),
                    "sub_account": {
                        "address": str(address),
                        "metadata": None
                    },
                    "metadata": None
                    },
                    "amount": {
                    "value": f"{value}0",
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
        return senddata
    except Exception as e:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": f"Failed to fetch the transaction information: {e}",
            "description": "There was an error while fetching transaction information from the RPC"
        })



# Endpoint that is used to fetch mempool transactions.
@app.post('/mempool')
async def mempool_info():
    mempool_data = get_mempool_info()
    if mempool_data:
        data = {
        "transaction_identifiers": [
            {
            "hash": mempool_data
            }
        ]
        }
        return data
    else:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": "Failed to fetch mempool information",
            "description": "There was an error while fetching mempool information from the RPC"
        })


# Endpoint that is used to fetch an account's balance.
@app.post('/account/balance')
async def account_balance(request: Request):
    global baldata
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})
    address = data['account_identifier']['address']
    balance_data = get_address_balance(address)
    baldata.append(balance_data)
    try:
        value_satt = baldata[0]['balance']
    except:
        value_satt = "00000000"
    value_sat = int(str(value_satt)[:8])
    index_value = data['block_identifier']['index']
    data = get_block_info(index_value)
    if RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
        value_sat = value_sat
    else:
        value_sat = "00000000"
    hash = data['hash']
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
    return data
    # else:
    #     return jsonify({
    #         "code": 500,
    #         "message": "Failed to fetch balance information",
    #         "description": "There was an error while fetching balance information from the API"
    #     }), 500


# Endpoint that is used to fetch the unspend amount of coins/transaction in an account.
@app.post('/account/coins')
async def account_coins(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})

    address = data.get("address")

    if not address:
        return HTTPException(status_code=400, detail={"error": "Address not provided"})

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
        return data
    else:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": "Failed to fetch UTXOs",
            "description": "There was an error while fetching UTXOs from the API"
        })

@app.post('/call')
async def call_rpc(request: Request):
    try:
        data = await request.json()
        # Check if the request has the necessary parameters
        if not data or "method" not in data:
            return HTTPException(status_code=400, detail={"error": "Invalid request. 'method' is a mandatory parameter."})
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
        return response
    except requests.exceptions.RequestException as rpc_error:
        return HTTPException(status_code=500, detail={"error": str(rpc_error)})

# Endpoint that is used to get a new verus address.
@app.post('/construction/derive')
async def networkstatus():
    data = getnewaddress()
    if data:
        return {"address": data}
    else:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": "Failed to create new verus wallet address",
            "description": "There was an error while fetching the information from the Local RPC"
        })


# Endpoint that is used to create a raw unsigned transaction.
@app.post('/construction/payloads')
async def create_unsigned_transaction_route(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})
    txid = data.get("txid")
    vout = data.get("vout")
    address = data.get("address")
    amount = data.get("amount")

    if not txid or not vout or not address or not amount:
        return HTTPException(status_code=400, detail={"error": "Invalid arguments"})

    try:
        unsigned_transaction = create_unsigned_transaction(txid, vout, address, amount)
        return {"transaction": unsigned_transaction}
    except Exception as e:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": f"Failed to construct a payload: {e}",
            "description": "There was an error while fetching the information from the Local RPC"
        })


# Endpoint that is used to verify and sign a raw unsigned transaction.
@app.post('/construction/parse')
async def parse_and_sign_transaction_route(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})

    unsigned_hex = data.get("unsigned_hex")

    if not unsigned_hex:
        return HTTPException(status_code=400, detail={"error": "Unsigned hex not provided"})
    try:
        result = parse_and_sign_transaction(unsigned_hex)
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": f"Failed to parse the transaction: {e}",
            "description": "There was an error while fetching the information from the Local RPC"
        })


# Endpoint that is used to broadcast a signed transaction into the blockchain.
@app.post('/construction/submit')
async def submit_signed_transaction_route(request: Request):
    data = await request.json()
    if not data:
        return HTTPException(status_code=400, detail={"error": "No data provided"})

    signed_hex = data.get("signed_hex")

    if not signed_hex:
        return HTTPException(status_code=400, detail={"error": "Signed hex not provided"})

    try:
        result = submit_signed_transaction(signed_hex)
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail={
            "code": 500,
            "message": f"Failed to submit the transaction: {e}",
            "description": "There was an error while fetching the information from the Local RPC"
        })

# Run the API
if __name__ == '__main__':
    # Only use the debug=True in development environment.
    # Use WSGI to run the API in production environment.
    if RUN_PRODUCTION == "False" or RUN_PRODUCTION == "false":
        uvicorn.run(app, port=int(PORT))
    elif RUN_PRODUCTION == "True" or RUN_PRODUCTION == "true":
        print(f"Verus Rosetta DataAPI running on port {PORT} in production mode...")
        uvicorn.run(app, host='0.0.0.0', port=int(PORT))
    else:
        print("Please make sure that the RUN_PRODUCTION variable is either True or False, Running the API in development mode since the variable is not set...")
        uvicorn.run(app, port=int(PORT))
