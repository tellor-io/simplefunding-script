from fundfeed.transaction import check_allowance, autopay_transaction
from fundfeed.catalog import catalog


def one_time_tips_funding(w3, account, autopay_address, token_address, amount):
    query_data = list(catalog())

    check_allowance_amount = int(amount * len(query_data))
    receipt = check_allowance(w3=w3, token_address=token_address, autopay_address=autopay_address, amount=check_allowance_amount, account=account)
    print("Tipping all query ids...")
    for qdata in query_data:
        receipt = autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            account=account,
            func_name="tip",
            _queryId=qdata.queryId,
            _amount=amount,
            _queryData=qdata.queryDataHex

        )
        if receipt["status"] == 0:
            msg = f"Transaction reverted. {receipt}"
            print(msg)

if __name__ == "main":
    print(__name__)