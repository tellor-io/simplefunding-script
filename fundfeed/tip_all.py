from web3 import Web3
from chained_accounts import ChainedAccount
from fundfeed.check_allowance import check_allowance
from fundfeed.autopay_txn import autopay_transaction
from fundfeed.catalog import catalog


def one_time_tips_funding(
    w3: Web3,
    account: ChainedAccount,
    autopay_address: str,
    token_address: str,
    transaction_type: int,
    amount: int,
):
    query_data = list(catalog())

    check_allowance_amount = int(amount * len(query_data))
    receipt = check_allowance(
        w3=w3,
        token_address=token_address,
        autopay_address=autopay_address,
        amount=check_allowance_amount,
        account=account,
        transaction_type=transaction_type,
    )
    print("Tipping all query ids...")
    for qdata in query_data:
        receipt = autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            account=account,
            transaction_type=transaction_type,
            func_name="tip",
            _queryId=qdata.queryId,
            _amount=amount,
            _queryData=qdata.queryDataHex,
        )
        if receipt["status"] == 0:
            msg = f"Transaction reverted. {receipt}"
            print(msg)
