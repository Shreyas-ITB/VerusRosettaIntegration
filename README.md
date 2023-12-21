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
```

```
- ```/network/options``` Get the options of the network, including versions and supported features.
- ```/network/rosetta/version``` Retrieve the Rosetta API version information.
- ```/block``` Get information about a specific block.
- ```/block/transaction``` Get information about a specific transaction in a block.
- ```/mempool``` Get information about transactions currently in the mempool.
- ```/account/balance``` Get the amount of coins that is present in an address.
- ```/account/coins``` Get the number of unspent transactions present in an address.

### Construction API Endpoints

- ```/construction/payloads``` Create an unsigned raw transaction.
- ```/construction/parse``` Parse, verify and sign an unsigned raw transaction.
- ```/construction/submit``` Broadcast the signed transaction into the network.

## Information

