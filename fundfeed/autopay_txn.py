from web3 import Web3
from typing import Any
from chained_accounts import ChainedAccount
from fundfeed.contract import contract
from fundfeed.transaction import transaction
from fundfeed.check_allowance import check_allowance


def autopay_transaction(
    w3: Web3,
    autopay_address: str,
    func_name: str,
    account: ChainedAccount,
    transaction_type: int,
    token_address=None,
    **kwargs: Any
):
    """Send transaction to autopay contract"""
    autopay_contract = contract(w3=w3, address=autopay_address)
    if token_address is not None:
        amount = kwargs["_amount"]
        _ = check_allowance(
            w3=w3,
            token_address=token_address,
            autopay_address=autopay_address,
            amount=amount,
            account=account,
            transaction_type=transaction_type,
        )

    return transaction(
        contract=autopay_contract,
        func_name=func_name,
        w3=w3,
        account=account,
        eip_1559=transaction_type,
        **kwargs
    )
