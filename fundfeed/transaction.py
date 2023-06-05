import os
from web3 import Web3
from web3.contract import Contract
from chained_accounts import ChainedAccount
from eth_utils import to_checksum_address
from fundfeed.utils import lazy_unlock_account
from fundfeed.utils import get_fee_info


def transaction(
    contract: Contract,
    func_name: str,
    w3: Web3,
    account: ChainedAccount,
    eip_1559: int,
    **kwargs,
):
    """Send transaction to contract"""
    txn = contract.get_function_by_name(func_name)(**kwargs)
    gas = os.getenv("GAS")
    gas_multiplier = int(os.getenv("GAS_MULTIPLIER", 1))
    if gas is None:
        try:
            gas = txn.estimateGas({"from": to_checksum_address(account.address)})
        except Exception as e:
            print(f"Error estimating gas: {e}")
            raise e

    lazy_unlock_account(account=account)
    transaction_success = False
    while not transaction_success:
        if eip_1559:
            priority_fee, max_fee = get_fee_info(w3)
            if priority_fee is None or max_fee is None:
                raise Exception(
                    "Error in calculating gas fees for EIP-1559 type transaction"
                )
            gas_fees = {
                "maxPriorityFeePerGas": w3.toWei(priority_fee, "gwei"),
                "maxFeePerGas": w3.toWei(max_fee, "gwei"),
            }
        else:
            gas_fees = {"gasPrice": int(w3.eth.gas_price * gas_multiplier)}
        try:
            wallet_nonce = w3.eth.get_transaction_count(
                to_checksum_address(account.address)
            )
            txn_build = contract.get_function_by_name(func_name)(
                **kwargs
            ).buildTransaction(dict(nonce=int(wallet_nonce), gas=gas, **gas_fees))
            local_account = account.local_account
            signed_txn = local_account.sign_transaction(txn_build)
            # Send the transaction
            transaction_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            transaction_success = True
        except ValueError as e:
            if "replacement transaction underpriced" in str(e):
                GAS_MULTIPLIER += 1
                continue
            elif "nonce too low" in str(e):
                continue
            else:
                raise

    transaction_hash = transaction_hash.hex()
    print(f"{func_name} txn: {transaction_hash}")
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash, timeout=520)
    return receipt
