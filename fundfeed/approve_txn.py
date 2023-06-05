from chained_accounts import ChainedAccount
from fundfeed.contract import contract
from fundfeed.transaction import transaction
from web3.contract import Contract
from web3 import Web3


def approve_transtacion(
    w3: Web3,
    autopay_address: str,
    token_address: str,
    account: ChainedAccount,
    amount: int,
    transaction_type: int,
    token_contract: Contract = None,
):
    """Approve autopay contract to spend tokens on behalf of account"""
    # if token contract instance is not provided, create one
    if token_contract == None:
        token_contract = contract(w3=w3, address=token_address)
    # send transaction to approve autopay contract to spend tokens on behalf of account
    approval_txn_receipt = transaction(
        contract=token_contract,
        func_name="approve",
        w3=w3,
        account=account,
        eip_1559=transaction_type,
        _spender=autopay_address,
        _amount=amount,
    )
    if approval_txn_receipt["status"] == 0:
        msg = f"Transaction failed. {approval_txn_receipt}"
        raise Exception(msg)
    return approval_txn_receipt
