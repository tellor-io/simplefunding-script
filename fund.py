from web3 import Web3
from web3.contract import Contract
import json
from dotenv import find_dotenv, load_dotenv
import os
from eth_abi import encode_single

def fallback_input(_key: str):
    val = os.getenv(_key, None)
    if not val:
        return input(f"{_key}:\n")
    print(f"{_key} set!")
    return val

print(f"env loaded: {load_dotenv(find_dotenv())}")

autopay_address = Web3.toChecksumAddress(fallback_input("AUTOPAY_ADDRESS"))
wallet_address = Web3.toChecksumAddress(fallback_input("WALLET_ADDRESS"))
private_key = fallback_input("PRIVATE_KEY")
token_address = Web3.toChecksumAddress(fallback_input("TOKEN_ADDRESS"))
node_uri = fallback_input("NODE_URI")
spending_amount: int = fallback_input("AMOUNT")


with open('abi/autopay.json') as autopay_abi:
    autopay_abi = json.load(autopay_abi)

with open('abi/token.json') as token_abi:
    token_abi = json.load(token_abi)

w3 = Web3(Web3.HTTPProvider(node_uri))

autopay_contract_factory = w3.eth.contract(address=autopay_address,abi=autopay_abi)
# only used for spending approval
token_contract_factory = w3.eth.contract(address=token_address,abi=token_abi)

gas = int(os.getenv("GAS",400000))
gas_multiplier = int(os.getenv("GAS_MULTIPLIER", 30))
def evm_transaction(contract_factory: Contract, func_name: str, **kwargs):
    wallet_nonce = w3.eth.get_transaction_count(wallet_address)
    txn_build = contract_factory.get_function_by_name(func_name)(**kwargs).buildTransaction(dict(
                                nonce=int(wallet_nonce),
                                gasPrice=int(w3.eth.gas_price * gas_multiplier),
                                gas = gas
                              ))
    signed_txn = w3.eth.account.signTransaction(txn_build, private_key)
    # Send the transaction
    transaction_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    transaction_hash = transaction_hash.hex()
    print(f"{func_name} txn: {transaction_hash}")
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return receipt

q1 = input("Do you want to approve spending first?  [ENTER] y/n\n")
if q1 == 'y':
    approval_txn_receipt = evm_transaction(token_contract_factory, "approve", _spender=autopay_address, _value=int(spending_amount))
    if approval_txn_receipt["status"] == 0:
        msg = f"Transaction reverted. {approval_txn_receipt}"
        raise Exception(msg)
# setup datafeed
# datafeed constants
# setupDataFeed
query_id = None
feed_id = None

q2 = input("Do you want to setup a feed?  [ENTER] y/n\n")
if q2 == 'y':

    query_data = bytes.fromhex(input("Query data(hex string, w/out 0x):\n"))
    query_id = Web3.keccak(query_data).hex()
    reward_amount = int(input("Reward amount:\n"))
    start_time = int(input("Start time timestamp:\n"))
    interval = int(input("Interval in seconds:\n"))
    window = int(input("Window in seconds:\n"))
    price_threshold = int(input("Price threshold:\n"))
    feed_data = encode_single("(bytes32,uint256,uint256,uint256,uint256,uint256)",[bytes.fromhex(query_id[2:]), reward_amount, start_time, interval, window, price_threshold])
    feed_id = Web3.keccak(feed_data).hex()

    setup_feed_txn = evm_transaction(autopay_contract_factory, "setupDataFeed", _queryId=query_id, _reward=reward_amount,_startTime=start_time, _interval=interval, _window=window, _priceThreshold=price_threshold,_queryData=query_data.hex())
    if setup_feed_txn["status"] == 0:
        msg = f"Transaction reverted. {setup_feed_txn}"
        raise Exception(msg)
# fund feed
# fundFeed
print("Feed funding step ...")
if query_id is None:
    query_id = input("Enter query id (hex string):\n")

if feed_id is None:
    feed_id = input("Enter feed id (hex string):\n")

fund_feed_txn = evm_transaction(autopay_contract_factory, "fundFeed", _feedId=feed_id, _queryId=query_id, _amount=int(spending_amount))
if fund_feed_txn["status"] == 0:
    msg = f"Transaction reverted. {fund_feed_txn}"
    raise Exception(msg)

print("Funding was successful!")