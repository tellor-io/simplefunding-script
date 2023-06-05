import os
import getpass
from web3 import Web3
from chained_accounts import ChainedAccount
from web3.types import FeeHistory
from web3.types import Wei
from fundfeed.constants import CHAINS


def fallback_input(_key: str):
    """Prompt input if no .env setup"""
    val = os.getenv(_key, None)
    if not val:
        return input(f"Enter {_key}:\n")
    print(f"{_key} set!")
    return val


def web3_instance(chain: int) -> Web3:
    return Web3(
        provider=Web3.HTTPProvider(endpoint_uri=fallback_input(CHAINS[chain].node))
    )


def lazy_unlock_account(account: ChainedAccount) -> None:
    """Unlock account if it is locked (borrowed from telliotfeeds)"""
    if account.is_unlocked:
        return
    else:
        # Try unlocking with no password
        try:
            account.unlock("")
        except ValueError:
            try:
                password = getpass.getpass(
                    f"Enter encryption password for {account.name}: "
                )
                account.unlock(password)
            except ValueError:
                raise Exception(f"Invalid password for {account.name}")


def fee_history_priority_fee_estimate(
    fee_history: FeeHistory, priority_fee_max: int
) -> int:
    """Estimate priority fee based on a percentile of the fee history.

    Adapted from web3.py fee_utils.py

    Args:
        fee_history: Fee history object returned by web3.eth.fee_history
        priority_fee_max: Maximum priority fee willing to pay

    Returns:
        Estimated priority fee in wei
    """
    priority_fee_min = 1_000_000_000  # 1 gwei
    # grab only non-zero fees and average against only that list
    non_empty_block_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

    # prevent division by zero in the extremely unlikely case that all fees within the polled fee
    # history range for the specified percentile are 0
    divisor = len(non_empty_block_fees) if len(non_empty_block_fees) != 0 else 1

    priority_fee_average_for_percentile = Wei(
        round(sum(non_empty_block_fees) / divisor)
    )

    if priority_fee_average_for_percentile > priority_fee_max:
        return priority_fee_max
    elif priority_fee_average_for_percentile < priority_fee_min:
        return priority_fee_min
    else:
        return priority_fee_average_for_percentile


def get_fee_info(w3, max_priority_fee_range=80):
    """Calculate max fee and priority fee if not set
    for more info:
        https://web3py.readthedocs.io/en/v5/web3.eth.html?highlight=fee%20history#web3.eth.Eth.fee_history
    """
    try:
        fee_history = w3.eth.fee_history(
            block_count=5, newest_block="latest", reward_percentiles=[25, 50, 75]
        )
        # "base fee for the next block after the newest of the returned range"
        base_fee = fee_history.baseFeePerGas[-1] / 1e9
        # estimate priority fee from fee history
        priority_fee_max = int(max_priority_fee_range * 1e9)  # convert to wei
        priority_fee = (
            fee_history_priority_fee_estimate(
                fee_history, priority_fee_max=priority_fee_max
            )
            / 1e9
        )
        max_fee = base_fee + priority_fee
        return priority_fee, max_fee
    except Exception as e:
        print(f"Error in calculating gas fees: {e}")
        return None, None
