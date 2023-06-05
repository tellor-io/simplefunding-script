import json
from web3 import Web3


def contract(w3: Web3, address: str):
    with open("abi/i360.json") as abi:
        abi = json.load(abi)
    return w3.eth.contract(address=address, abi=abi)
