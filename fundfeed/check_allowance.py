from web3 import Web3
from fundfeed.contract import contract
from chained_accounts import ChainedAccount
from fundfeed.approve_txn import approve_transtacion
from eth_utils import to_checksum_address


def check_allowance(
    w3: Web3,
    token_address: str,
    autopay_address: str,
    amount: int,
    account: ChainedAccount,
    transaction_type: int,
):
    """Check if autopay contract is approved to spend tokens on behalf of account
    to avoid wasting gas on approving tokens if already approved"""
    # create token contract instance
    token_contract = contract(w3=w3, address=token_address)
    # get current allowance
    allowance = token_contract.functions.allowance(
        _owner=to_checksum_address(account.address), _spender=autopay_address
    ).call()
    print(f"Allowance: {allowance}")

    if allowance < amount:
        print("Approving token spend...")
        return approve_transtacion(
            w3=w3,
            autopay_address=autopay_address,
            token_address=token_address,
            account=account,
            amount=amount,
            transaction_type=transaction_type,
            token_contract=token_contract,
        )
    return allowance
