# VerusRosettaIntegration

The APIs that are used to link Verus blockchain with Open-Source Coinbase Rosetta Blockchain integration tools.

## Requirements

- Python needs to be installed if you are trying to run the API, version 3.9.8 (tested) 3.10, 3.11 works fine.
- A Linux server of atleast 8GB RAM and a decent processor to handle the requests.

## Setting up the APIs

Clone the github repository \
```git clone https://github.com/Shreyas-ITB/VerusRosettaIntegration```

Create a virtual environment just to make everything safe and easy to use \
```python3 -m venv venv && bash venv/bin/activate``` 

Rename the ``example.env`` into ``.env`` and then edit the following information present in it.

```
RPCURL=http://127.0.0.1:27486/ # The default verus daemon local url. Recommended to leave it alone.
RPCUSER="" # The RPC Username located in the vrsc.conf file inside the "~/.komodo/VRSC" folder
RPCPASS="" # The RPC Password located in the vrsc.conf file inside the "~/.komodo/VRSC" folder.
ROSETTAAPI=5500 # Default API Port.
RUN_PRODUCTION=False # Run the APIs in production mode.
```
Changing the ``RUN_PRODUCTION`` to ``True`` runs the APIs in production mode (this applies for both the data and construction APIs) if its kept ``False`` then it would run in development mode.

You will also have to run the latest version of verus daemon, i would recommend to run the verus daemon, allow it to sync with the blockchain fully and then run the APIs.

Install the dependencies required for the APIs \
```pip install -r requirements.txt```

## Running the API

Once you have completed the setup part, all you have to do is run the python files \
```python3 rosettaapi.py```

If you want to run it as a docker image, you have to build the image and run it \
```sudo docker build -t rosettaapi.py .``` \

then run the docker builds \
```sudo docker run -p 5500:5500 --env-file .env rosettaapi.py``` \
- Docker will automatically install the requirements and setup an environment for you so if you are running the APIs using docker then there is no need to install the dependencies and setting up the python virtual environment in the previous step.
- Data API will be running on the public IP of the server on port 5500 (default)
- Construction API will be running on the public IP of the server on port 5600 (default)
- If you are trying to run the APIs in production mode then i would recommend to pass the IPs of both the APIs into cloudflare protection, that would reduce the risk of getting ddos'ed. There are built in rate limiters into the APIs already but just to keep it more safer cloudflare is necessary.

## Testing

- Download the mesh-cli (previously known as rosetta-cli) from the [github page](https://github.com/coinbase/mesh-cli/releases/tag/v0.10.3) on a linux machine.
- Create another json file with the name ``config.json`` in the same directory where the mesh-cli's (rosetta-cli) executable is present. (checks everything except the reconcillation which is not needed)
- As usual copy the json content below, paste it in the ``config.json`` you have created and save it.
```json
{
 "network": {
  "blockchain": "VRSC",
  "network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
  "sub_network_identifier": {
      "network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
    }
 },
 "online_url": "http://127.0.0.1:5500",
 "data_directory": "",
 "http_timeout": 10000,
 "tip_delay": 3000,
 "data": {
  "historical_balance_disabled": true,
  "reconciliation_disabled": true,
  "inactive_discrepancy_search_disabled": false,
  "balance_tracking_disabled": false,
  "end_conditions": {
    "tip": true
  }
 }
}
```
- Run the CLI to test the API (assuming that the API is already running, and make sure that the API is running in development mode ``RUN_PRODUCTION=False`` Run production must be set to false)
- Execute the below commands to test the API with different config files we have created.
```bash
./rosetta-cli check:data --configuration-file config.json
```

- You can also change the data in the config file according to your preference.
- Running the API in development mode and testing is mandatory as it reduces the number of blocks and saves time. (syncing all the blocks in the network by running the CLI tool is not permitted because it consumes a lot of time and needs a very powerful computer to handle multiple requests per second thats being given out to the API, running in development mode also disables the rate limiter so that it will be easy for the CLI tool to communicate)

## Endpoints

### API Endpoints

- ```/network/list``` Retrieve all the networks available.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5500/network/list
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/network/list"
response = requests.post(url)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"network_identifiers": [
		{
			"blockchain": "VRSC",
			"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
			"sub_network_identifier": {
				"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
			}
		}
	]
}
```

- ```/network/status``` Retrieve the current status of the network.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5500/network/status
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/network/status"
response = requests.post(url)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"current_block_identifier": {
		"hash": "3db50b16921a6f3560a6787c6b6db27dbed65213bbc259599b1a85b2754b1a5e",
		"index": 2909994
	},
	"current_block_timestamp": 1707194343,
	"genesis_block_identifier": {
		"hash": "027e3758c3a65b12aa1046462b486d0a63bfa1beae327897f56c5cfb7daaae71",
		"index": 0
	},
	"oldest_block_identifier": {
		"hash": "027e3758c3a65b12aa1046462b486d0a63bfa1beae327897f56c5cfb7daaae71",
		"index": 0
	},
	"peers": [
		{
			"metadata": null,
			"peer_id": "a8157d22-bef8-4cdf-8eb1-49575d54fb71"
		}
	],
	"sync_status": {
		"current_index": 2909994,
		"stage": "Synced",
		"synced": true,
		"target_index": 2909994
	}
}
```

- ```/network/options``` Get the options of the network, including versions and supported features.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5500/network/options
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/network/options"
response = requests.post(url)
print(response.json())
```
Expected endpoint behaviour
```json
{
    "allow": {
        "balance_exemptions": [
            {
                "currency": {
                    "decimals": 8,
                    "metadata": null,
                    "symbol": "VRSC"
                },
                "exemption_type": "dynamic",
                "sub_account_address": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
            }
        ],
        "call_methods": [
            "POST"
        ],
        "errors": [
            {
                "code": 12,
                "description": "This error is returned when the requested AccountIdentifier is improperly formatted.",
                "details": null,
                "message": "Invalid account format",
                "retriable": true
            },
            {
                "code": 14,
                "description": "There was an error while fetching network version from the RPC",
                "details": null,
                "message": "Failed to fetch network version",
                "retriable": true
            },
            {
                "code": 16,
                "description": "There was an error while fetching block information from the RPC",
                "details": null,
                "message": "Failed to fetch block information",
                "retriable": true
            },
            {
                "code": 18,
                "description": "There was an error while fetching transaction information from the RPC",
                "details": null,
                "message": "Failed to fetch transaction information",
                "retriable": true
            },
            {
                "code": 20,
                "description": "There was an error while fetching mempool information from the RPC",
                "details": null,
                "message": "Failed to fetch mempool information",
                "retriable": true
            },
            {
                "code": 22,
                "description": "There was an error while fetching balance information from the API",
                "details": null,
                "message": "Failed to fetch balance information",
                "retriable": true
            },
            {
                "code": 24,
                "description": "There was an error while fetching UTXOs from the API",
                "details": null,
                "message": "Failed to fetch UTXOs",
                "retriable": true
            },
            {
                "code": 26,
                "description": "There was an error while fetching the information from the Local RPC",
                "details": null,
                "message": "Failed to create new verus wallet address",
                "retriable": true
            }
        ],
        "historical_balance_lookup": true,
        "mempool_coins": false,
        "operation_statuses": [
            {
                "status": "confirmed",
                "successful": true
            },
            {
                "status": "unconfirmed",
                "successful": true
            },
            {
                "status": "processing",
                "successful": true
            },
            {
                "status": "pubkey",
                "successful": true
            }
        ],
        "operation_types": [
            "Transfer",
            "mined",
            "minted"
        ],
        "timestamp_start_index": 1231006505
    },
    "version": {
        "metadata": null,
        "middleware_version": "0.2.7",
        "node_version": "2000753",
        "rosetta_version": "1.2.5"
    }
}
```

- ```/block``` Get information about a specific block.
```sh
# Call the endpoint with curl:

# Fetch using a block height as an argument
curl -X POST -H "Content-Type: application/json" -d '{"block_identifier": 2909100}' http://127.0.0.1:5500/block
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/block"

# Fetch using a block height as an argument
payload = {
    "block_identifier": 2909100
}
response = requests.post(url, json=payload)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"block": {
		"block_identifier": {
			"hash": 2909100,
			"index": "000000000001764d6ac1e1a56a546fec795bdac6948867911c18bd7579213e2d"
		},
		"metadata": null,
		"parent_block_identifier": {
			"hash": "31f2b3b007eafbd3ef2756b7077a2d18d8372d727ce9392ede016a7f309986fb",
			"index": 1123941
		},
		"timestamp": 1707138632,
		"transactions": [
			{
				"metadata": null,
				"operations": [
					{
						"account": {
							"address": "iHbTMYB43xqqFVmEqJkqff6GrZDQoaiq6g",
							"metadata": null,
							"sub_account": {
								"address": "RQ55dLQ7uGnLx8scXfkaFV6QS6qVBGyxAG",
								"metadata": null
							}
						},
						"amount": {
							"currency": {
								"decimals": 8,
								"metadata": null,
								"symbol": "VRSC"
							},
							"metadata": null,
							"value": 601136018
						},
						"coin_change": {
							"coin_action": null,
							"coin_identifier": {
								"identifier": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
							}
						},
						"metadata": null,
						"operation_identifier": {
							"index": 5,
							"network_index": 0
						},
						"related_operations": [
							{
								"index": 5,
								"network_index": 0
							}
						],
						"status": "confirmed",
						"type": "mined"
					}
				],
				"related_transactions": [
					{
						"direction": "forward",
						"network_identifier": {
							"blockchain": "VRSC",
							"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
							"sub_network_identifier": {
								"metadata": null,
								"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
							}
						},
						"transaction_identifier": {
							"hash": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
						}
					}
				],
				"transaction_identifier": {
					"hash": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
				}
			}
		]
	},
	"other_transactions": [
		{
			"hash": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
		}
	]
}
```

- ```/block/transaction``` Get information about a specific transaction in a block.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"transaction_id": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"}' http://127.0.0.1:5500/block/transaction
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/block/transaction"
payload = {
    "transaction_id": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
}
response = requests.post(url, json=payload)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"transaction": {
		"metadata": null,
		"operations": [
			{
				"account": {
					"address": [
						"iHbTMYB43xqqFVmEqJkqff6GrZDQoaiq6g"
					],
					"metadata": null,
					"sub_account": {
						"address": [
							"RQ55dLQ7uGnLx8scXfkaFV6QS6qVBGyxAG"
						],
						"metadata": null
					}
				},
				"amount": {
					"currency": {
						"decimals": 8,
						"metadata": null,
						"symbol": "VRSC"
					},
					"metadata": null,
					"value": 6.01136018
				},
				"coin_change": {
					"coin_action": null,
					"coin_identifier": {
						"identifier": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
					}
				},
				"metadata": null,
				"operation_identifier": {
					"index": 5,
					"network_index": 0
				},
				"related_operations": [
					{
						"index": 5,
						"network_index": 0
					}
				],
				"status": "cryptocondition",
				"type": "Transfer"
			}
		],
		"related_transactions": [
			{
				"direction": "forward",
				"network_identifier": {
					"blockchain": "VRSC",
					"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
					"sub_network_identifier": {
						"metadata": null,
						"network": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
					}
				},
				"transaction_identifier": {
					"hash": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
				}
			}
		],
		"transaction_identifier": {
			"hash": "4e55048d2a21805b011985aaef43665c640af0da8b0927c1d57c4b34f67e96b9"
		}
	}
}
```

- ```/mempool``` Get information about transactions currently in the mempool.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5500/mempool
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/mempool"
response = requests.post(url)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"transaction_identifiers": [
		{
			"hash": [
				"3cb19b6eba6c12ee5281d88725c791b7e7d79e72282e48426398646651670a10",
				"f9cd43b934cc3b2a44e219c025a6556564e09e2f248fb6810fdd6f4dddc25337",
				"902dc1ccc22734f06feb0f3dd4005e43b9f281e54fc66676d719be0268c3224b",
				"7c115584b323c2225e388f921f47bacf0373ba509b81d8f43ca3d86f7c4ab35f",
				"8530cb38f72efb72ad0025c33643c65d06661db5655b3ac361939ada802def6a",
				"9424fbcfd9fa395ec3b3ecd7e57f712d6b399ce122aa6ef924d7679b5258f978",
				"5623e869269e16c7c579b5f86ef5961919ddeda733718953c036c292fa714483",
				"5cf73ca8cd48688b37a254f2bfc616fda38ebd2a525f58ec1433c389f626b794",
				"bb6f96379cf350b3b70d8af85574f1e2a00bda0aff4579aac47b637b3beb82a3",
				"e9d125756fa33c817e17377d400174aba15b4c5489a9493037e6c815ba9ac4c4",
				"89b60273f8292490a8d4b4d426abe04f980b9155c53b88741b627de5556e0cc5",
				"b5b509b5e245c5a9ac921fa26f562b616b177f8b235fba9832967c02c447f8c5",
				"d29bbdde1896392457f76ca7585336b01a90336e54f66c1c4bb6476f61a4bde0",
				"b6b87ed4703035782a6087130acb7629b414a58207b9f18457f2dc1fa91954f7"
			]
		}
	]
}
```

- ```/account/balance``` Get the amount of coins that is present in an address.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR"}' http://127.0.0.1:5500/account/balance
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/account/balance"
payload = {
    "address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR"
}
response = requests.post(url, json=payload)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"balances": [
		{
			"currency": {
				"decimals": 8,
				"metadata": null,
				"symbol": "VRSC"
			},
			"metadata": null,
			"value": 9341279
		}
	],
	"block_identifier": {
		"hash": "000000000002f0bb840520805a618ae024801e4c3c66422a87a82253ca65afdd",
		"index": 2910001
	},
	"metadata": null
}
```

- ```/account/coins``` Get the number of unspent transactions present in an address.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR"}' http://127.0.0.1:5500/account/coins
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/account/coins"
payload = {
    "address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR"
}
response = requests.post(url, json=payload)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"block_identifier": {
		"hash": [
			"f5b45f2d1e62b1cc6c8468e4a76e932137e9775f8bebb30a8d60f7db29d043bc",
			"a28e79b0c82ab2277c4ea407d976707c8cf635624ccf128e0f3bfd32fbe41b0e",
			"28d07ce4d33175b3f6e8a85630a80c61e45333f05ac1bbb6632c4a9f8ab990e0",
			"2109b693bda7e1ea9b075a9ce67971b4a109c27aefc2050cafd9ddf8de2f5c21",
			"2961d462b26e96aacf233adec5a6ab8aede7253384fb79f080a6101ef04e461b",
			"1e8b411ab92e61889ec2ac58e2a43cd25c4ffec1f6e9e63b5aed652de2f6a425"
		],
		"index": [
			2880850,
			2882034,
			2883202,
			2884359,
			2885535,
			2886700
		]
	},
	"coins": [
		{
			"amount": {
				"currency": {
					"decimals": 8,
					"metadata": null,
					"symbol": "VRSC"
				},
				"metadata": null,
				"value": [
					1316651,
					3326932,
					1361294,
					1221210,
					1333377,
					781815
				]
			},
			"coin_identifier": {
				"identifier": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"
			}
		}
	],
	"metadata": null
}
```

- ```/call``` Make a network-specific procedure call
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"method": "getblockchaininfo", "parameter": []}' http://127.0.0.1:5500/call
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/call"
payload = {
    "method": "getblockchaininfo",
    "parameter": []
}
response = requests.post(url, json=payload)
print(response.json())
```
Expected endpoint behaviour
```json
{
	"result": {
		"bestblockhash": "00000000000276e2f22281c19597a3184cffbb2355ddb8e25a188e06e1bb232f",
		"blocks": 2910026,
		"chain": "main",
		"chainid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
		"chainstake": "8000000000000000000000000000000000000000000d79a125eb22ac73ff533a",
		"chainwork": "00000000000000000000000000000000000000026e5624a33b64a8dfbdb15d03",
		"commitments": 377270,
		"consensus": {
			"chaintip": "76b809bb",
			"nextblock": "76b809bb"
		},
		"difficulty": 3335841468412.399,
		"headers": 2910026,
		"name": "VRSC",
		"pruned": false,
		"size_on_disk": 10735016132,
		"softforks": [
			{
				"enforce": {
					"found": 4000,
					"required": 750,
					"status": true,
					"window": 4000
				},
				"id": "bip34",
				"reject": {
					"found": 4000,
					"required": 950,
					"status": true,
					"window": 4000
				},
				"version": 2
			},
			{
				"enforce": {
					"found": 4000,
					"required": 750,
					"status": true,
					"window": 4000
				},
				"id": "bip66",
				"reject": {
					"found": 4000,
					"required": 950,
					"status": true,
					"window": 4000
				},
				"version": 3
			},
			{
				"enforce": {
					"found": 4000,
					"required": 750,
					"status": true,
					"window": 4000
				},
				"id": "bip65",
				"reject": {
					"found": 4000,
					"required": 950,
					"status": true,
					"window": 4000
				},
				"version": 4
			}
		],
		"upgrades": {
			"5ba81b19": {
				"activationheight": 227520,
				"info": "See https://z.cash/upgrade/overwinter.html for details.",
				"name": "Overwinter",
				"status": "active"
			},
			"76b809bb": {
				"activationheight": 227520,
				"info": "See https://z.cash/upgrade/sapling.html for details.",
				"name": "Sapling",
				"status": "active"
			}
		},
		"valuePools": [
			{
				"chainValue": 24547.99070065,
				"chainValueZat": 2454799070065,
				"id": "sprout",
				"monitored": true
			},
			{
				"chainValue": 651376.2170615,
				"chainValueZat": 65137621706150,
				"id": "sapling",
				"monitored": true
			}
		],
		"verificationprogress": 1
	}
}
```

- ```/construction/derive``` Create a new wallet address.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5600/construction/derive
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5600/construction/derive"
response = requests.post(url)
print(response.json())
```
- ```/construction/payloads``` Create an unsigned raw transaction.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"txid": "0x2f23fd8cca835af21f3ac375bac601f97ead75f2e79143bdf71fe2c4be043e8f", "vout": 0, "address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR", "amount": 0.01}' http://127.0.0.1:5600/construction/payloads
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5600/construction/payloads"
payload = {
    "txid": "0x2f23fd8cca835af21f3ac375bac601f97ead75f2e79143bdf71fe2c4be043e8f",
    "vout": 0,
    "address": "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR",
     "amount": 0.01
}
response = requests.post(url, json=payload)
print(response.json())
```
- ```/construction/parse``` Parse, verify and sign an unsigned raw transaction.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"unsigned_hex": "f1a35d8b4926c5e6d9a817abe4c3f9027d6f4a6c8e971b26e5cf61d207c3e91a"}' http://127.0.0.1:5600/construction/parse
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5600/construction/parse"
payload = {
    "unsigned_hex": "f1a35d8b4926c5e6d9a817abe4c3f9027d6f4a6c8e971b26e5cf61d207c3e91a"
}
response = requests.post(url, json=payload)
print(response.json())
```
- ```/construction/submit``` Broadcast the signed transaction into the network.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"signed_hex": "a2bf8e074d6cf013ec012cfe2d2f37f68972165cc0a5ed13f4a5a7b234ef87b2"}' http://127.0.0.1:5600/construction/submit
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5600/construction/submit"
payload = {
    "signed_hex": "a2bf8e074d6cf013ec012cfe2d2f37f68972165cc0a5ed13f4a5a7b234ef87b2"
}
response = requests.post(url, json=payload)
print(response.json())
```

## Information
- This is a complete python implementation, there is no use of rosetta-sdks which use golang to implement the same routes into other blockchains. Since python is way more reliable, easy and flexible i have used it.
- Both the python APIs contain commented lines so that anyone who will be contributing to this project can easily understand whats going on in the code.
