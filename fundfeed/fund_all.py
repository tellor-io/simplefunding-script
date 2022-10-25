import os
import datetime

from fundfeed.catalog import catalog
from fundfeed.catalog import generate_feed
from fundfeed.transaction import constants
from fundfeed.transaction import autopay_transaction
from fundfeed.transaction import check_allowance

def fund_feed(account, chain, amount):
    w3, autopay_address, token_address = constants(chain)
    query_data = catalog()

    check_allowance_amount = int(amount * sum(1 for _ in catalog()))
    _ = check_allowance(w3=w3, token_address=token_address, autopay_address=autopay_address, amount=check_allowance_amount, account=account)

    EIGHT_EASTERN = datetime.datetime.today().replace(hour=8, minute=00, second=0, microsecond=0).timestamp()
    print(EIGHT_EASTERN, "EIGHT_EASTERN")
    query_data = catalog()
    for qdata in query_data:
        reward = os.getenv("REWARD", int(1e18))
        start_time = os.getenv("START_TIME", int(EIGHT_EASTERN))
        interval = os.getenv("INTERVAL", 21600)
        window = os.getenv("WINDOW", 3600)
        price_threshold = os.getenv("THRESHOLD", 0)
        _, feed_id = generate_feed(qdata.queryIdBytes, reward, start_time, interval, window, price_threshold)
        setup_feed_txn = autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            account=account,
            func_name="setupDataFeed",
            _queryId=qdata.queryId,
            _reward=reward,
            _startTime=start_time,
            _interval=interval,
            _window=window,
            _priceThreshold=price_threshold,
            _rewardIncreasePerSecond=0,
            _queryData=qdata.queryDataHex,
            _amount=int(amount)
        )

        if setup_feed_txn["status"] == 0:
            msg = f"Feed setup transaction failed for feed_id: {feed_id}"
            print(msg)
            continue

# if __name__ == "main":
#     fund_feed()