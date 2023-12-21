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
RPCURL=VERUS RPC URL # Replace this with actual verusd rpc url.
DATAPIPORT=5500 # This is the default port on which the Data API runs on, edit it as per your needs.
CONSTAPIPORT=5600 # This is the default port on which the Construction API runs on, edit it as per your needs.
RUN_PRODUCTION=False # Change this to True if you are running the APIs in production mode.
```
Changing the ``RUN_PRODUCTION`` to ``True`` runs the APIs in production mode (this applies for both the data and construction APIs) if its kept ``False`` then it would run in development mode. 

Install the dependencies required for the APIs \
```pip install -r requirements.txt```

## Running the API

Once you have completed the setup part, all you have to do is run the python files \
```python3 dataapi.py```
```python3 constructionapi.py```

If you want to run it as a docker image, you have to build the image and run it \
```sudo docker build -t dataapi.py .``` \
```sudo docker build -t constructionapi.py .```

then run the docker builds \
```sudo docker run -p 5500:5500 --env-file .env dataapi.py``` \
```sudo docker run -p 5500:5600 --env-file .env constructionapi.py```
- Docker will automatically install the requirements and setup an environment for you so if you are running the APIs using docker then there is no need to install the dependencies and setting up the python virtual environment in the previous step.
- Data API will be running on the public IP of the server on port 5500 (default)
- Construction API will be running on the public IP of the server on port 5600 (default)

## Endpoints

### Data API Endpoints

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

- ```/network/rosetta/version``` Retrieve the Rosetta API version information.
```sh
# Call the endpoint with curl:
curl -X POST http://127.0.0.1:5500/network/rosetta/version
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/network/rosetta/version"
response = requests.post(url)
print(response.json())
```

- ```/block``` Get information about a specific block.
```sh
# Call the endpoint with curl:

# Fetch using a hash as an argument
curl -X POST -H "Content-Type: application/json" -d '{"block_identifier": "0x1f2cc6c5027d2f201a5453ad1119574d2aed23a392654742ac3c78783c071f85"}' http://127.0.0.1:5500/block

# Fetch using a block height as an argument
curl -X POST -H "Content-Type: application/json" -d '{"block_identifier": "12800"}' http://127.0.0.1:5500/block
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/block"

# Fetch using a hash as an argument
payload = {
    "block_identifier": "0x1f2cc6c5027d2f201a5453ad1119574d2aed23a392654742ac3c78783c071f85"
}
response = requests.post(url, json=payload)
print(response.json())

# Fetch using a block height as an argument
payload = {
    "block_identifier": "12800"
}
response = requests.post(url, json=payload)
print(response.json())
```

- ```/block/transaction``` Get information about a specific transaction in a block.
```sh
# Call the endpoint with curl:
curl -X POST -H "Content-Type: application/json" -d '{"transaction_id": "0x2f23fd8cca835af21f3ac375bac601f97ead75f2e79143bdf71fe2c4be043e8f"}' http://127.0.0.1:5500/block/transaction
```
```py
# Make a request using python:
import requests

url = "http://127.0.0.1:5500/block/transaction"
payload = {
    "transaction_id": "0x2f23fd8cca835af21f3ac375bac601f97ead75f2e79143bdf71fe2c4be043e8f"
}
response = requests.post(url, json=payload)
print(response.json())
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

### Construction API Endpoints

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

