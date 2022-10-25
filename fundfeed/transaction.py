import json
from web3 import Web3
from web3.contract import Contract
from chained_accounts import ChainedAccount
from eth_utils import to_checksum_address
from fundfeed.constants import CHAINS
from fundfeed.constants import fallback_input

import getpass


def lazy_unlock_account(account: ChainedAccount) -> None:
    if account.is_unlocked:
        return
    else:
        # Try unlocking with no password
        try:
            account.unlock("")
        except ValueError:
            try:
                password = getpass.getpass(f"Enter encryption password for {account.name}: ")
                account.unlock(password)
            except ValueError:
                raise Exception(f"Invalid password for {account.name}")

def contract(w3, address):
    with open('abi/i360.json') as abi:
        abi = json.load(abi)
    return w3.eth.contract(address=address, abi=abi)

def constants(chain: int):
    provider = fallback_input(CHAINS[chain].node)
    autopay_address = CHAINS[chain].autopay_address
    token_address = CHAINS[chain].token_address

    w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=provider))
    return w3, to_checksum_address(autopay_address), to_checksum_address(token_address)

def autopay_transaction(
    w3,
    autopay_address,
    func_name,
    account,
    token_address=None,
    **kwargs
):
    # w3, autopay_address, token_address = constants(chain=chain)
    autopay_contract = contract(w3=w3, address=autopay_address)
    if token_address is not None:
        amount = kwargs["_amount"]
        _ = check_allowance(w3=w3, token_address=token_address, autopay_address=autopay_address, amount=amount, account=account)

    return transaction(
        contract=autopay_contract,
        func_name=func_name,
        w3=w3,
        account=account,
        **kwargs
    )

def approve_transtacion(w3, autopay_address, token_address, account, amount: int, token_contract: Contract = None):
    if token_contract == None:
        token_contract = contract(w3=w3, address=token_address)
    approval_txn_receipt = transaction(
            contract=token_contract,
            func_name="approve",
            w3=w3,
            account=account,
            _spender=autopay_address,
            _amount=amount
        )
    if approval_txn_receipt["status"] == 0:
        msg = f"Transaction failed. {approval_txn_receipt}"
        raise Exception(msg)
    return approval_txn_receipt
    
def check_allowance(w3: Web3, token_address: str, autopay_address: str, amount: int, account: ChainedAccount):
    token_contract = contract(w3=w3, address=token_address)
    allowance = token_contract.functions.allowance(_owner=to_checksum_address(account.address), _spender=autopay_address).call()
    print(f"Allowance: {allowance}")

    if allowance < amount:
        print("Approving token spend...")
        return approve_transtacion(account=account, amount=amount, token_contract=token_contract)
    return allowance

def transaction(contract:  Contract, func_name: str, w3: Web3, account: ChainedAccount, **kwargs):
    from fundfeed.constants import GAS, GAS_MULTIPLIER
    lazy_unlock_account(account=account)
    transaction_success = False
    while not transaction_success:
        try:
            wallet_nonce = w3.eth.get_transaction_count(to_checksum_address(account.address))
            txn_build = contract.get_function_by_name(func_name)(**kwargs).buildTransaction(dict(
                                        nonce=int(wallet_nonce),
                                        gasPrice=int(w3.eth.gas_price * GAS_MULTIPLIER),
                                        gas = GAS
                                    ))
            local_account = account.local_account
            signed_txn = local_account.sign_transaction(txn_build)
            # Send the transaction
            transaction_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            transaction_success = True
        except ValueError as e:
            if 'replacement transaction underpriced' in str(e):
                GAS_MULTIPLIER += 1
                continue
            elif 'nonce too low' in str(e):
                continue
            else:
                raise
    
    transaction_hash = transaction_hash.hex()
    print(f"{func_name} txn: {transaction_hash}")
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash, timeout=520)
    return receipt
