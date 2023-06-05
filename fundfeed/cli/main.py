import click
from eth_utils import keccak
from eth_utils import encode_hex
from fundfeed.cli.utils import RequiredIf
from fundfeed.cli.utils import build_query_data
from chained_accounts import find_accounts
from chained_accounts import ChainedAccount
from fundfeed.tip_all import one_time_tips_funding
from fundfeed.autopay_txn import autopay_transaction
from fundfeed.approve_txn import approve_transtacion
from fundfeed.fund_all import fund_feed
from fundfeed.utils import web3_instance
from fundfeed.constants import CHAINS
from fundfeed.cli.utils import colored_style
from fundfeed.cli.utils import colored_prompt


@click.group()
@click.argument("account_name", type=str)
@click.argument("chain", type=int)
@click.option("--query-data", "-qd", type=str, default=None)
@click.option("-tt", "--transaction-type", type=click.Choice(["0", "2"]), default="2")
@click.option(
    "-amt",
    "--amount",
    type=float,
    required=True,
    confirmation_prompt=True,
    prompt=colored_style("Enter funding amount"),
)
@click.pass_context
def main(
    ctx: click.Context,
    account_name: ChainedAccount,
    chain: int,
    query_data: str,
    transaction_type: int,
    amount: float,
):
    """Fund Autopay!"""
    try:
        account = find_accounts(name=account_name)[0]
    except IndexError:
        click.echo(colored_style("No account found with that name!\n"))
        click.echo(
            colored_style(
                "Consider adding it using chained add <name> <private-key> <chain-ids> command"
            )
        )
        return

    ctx.ensure_object(dict)

    ctx.obj["ACCOUNT"] = account
    ctx.obj["CHAIN_ID"] = chain
    ctx.obj["QUERY_DATA"] = query_data
    ctx.obj["WEB3"] = web3_instance(chain=chain)
    ctx.obj["AUTOPAY_ADDRESS"] = CHAINS[chain].autopay_address
    ctx.obj["TOKEN_ADDRESS"] = CHAINS[chain].token_address
    ctx.obj["TRANSACTION_TYPE"] = int(transaction_type)
    ctx.obj["AMOUNT"] = int(amount * 1e18)


@main.command()
@click.option("--tip-all/--single-tip")
@click.pass_context
def tip(ctx: click.Context, tip_all: bool):
    account = ctx.obj["ACCOUNT"]
    w3 = ctx.obj["WEB3"]
    autopay_address = ctx.obj["AUTOPAY_ADDRESS"]
    token_address = ctx.obj["TOKEN_ADDRESS"]
    transaction_type = ctx.obj["TRANSACTION_TYPE"]

    tip_amount = ctx.obj["AMOUNT"]

    if tip_all:
        one_time_tips_funding(
            w3, account, autopay_address, token_address, transaction_type, tip_amount
        )
    else:
        query_data = ctx.obj["QUERY_DATA"]
        if query_data is None:
            choice = click.confirm(
                colored_style("Build query data? Enter y if query data not available")
            )
            if not choice:
                query_data = colored_prompt("Enter query data", str)
            else:
                query_data = build_query_data()
        query_id = encode_hex(keccak(hexstr=query_data))

        autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            token_address=token_address,
            account=account,
            transaction_type=transaction_type,
            func_name="tip",
            _queryId=query_id,
            _queryData=query_data,
            _amount=tip_amount,
        )


@main.command()
@click.option("--setup-datafeed/--fund-only")
@click.option(
    "--reward", "-rwd", cls=RequiredIf, required_if="setup_datafeed", type=float
)
@click.option(
    "--window", "-win", cls=RequiredIf, required_if="setup_datafeed", type=int
)
@click.option(
    "--start-time", "-st", cls=RequiredIf, required_if="setup_datafeed", type=int
)
@click.option("--interval", cls=RequiredIf, required_if="setup_datafeed", type=int)
@click.option(
    "--price-threshold", "-pt", cls=RequiredIf, required_if="setup_datafeed", type=float
)
@click.option(
    "--reward-increase", "-ri", cls=RequiredIf, required_if="setup_datafeed", type=float
)
@click.option("--feed-id", cls=RequiredIf, required_if="fund_only", type=str)
@click.pass_context
def fundfeed(
    ctx: click.Context,
    setup_datafeed: bool,
    reward: float,
    window: int,
    start_time: int,
    interval: int,
    price_threshold: float,
    reward_increase: int,
    feed_id: str,
):

    query_data = ctx.obj["QUERY_DATA"]
    account = ctx.obj["ACCOUNT"]
    w3 = ctx.obj["WEB3"]
    autopay_address = ctx.obj["AUTOPAY_ADDRESS"]
    token_address = ctx.obj["TOKEN_ADDRESS"]
    amount = ctx.obj["AMOUNT"]
    transaction_type = ctx.obj["TRANSACTION_TYPE"]
    # input float percentage and convert to what autopay expects
    # ie 100 = 1%
    price_threshold = int(price_threshold * 10000)
    if setup_datafeed:
        if query_data is None:
            choice = click.confirm(
                colored_style("Build query data? Enter y if query data not available")
            )
            if not choice:
                query_data = colored_prompt("Enter query data", str)
            else:
                query_data = build_query_data()
        setup_kwargs = {
            "_queryId": encode_hex(keccak(hexstr=query_data)),
            "_reward": int(reward * 1e18),
            "_startTime": start_time,
            "_interval": interval,
            "_window": window,
            "_priceThreshold": price_threshold,
            "_rewardIncreasePerSecond": int(reward_increase * 1e18),
            "_queryData": query_data,
            "_amount": amount,
        }
        autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            token_address=token_address,
            account=account,
            transaction_type=transaction_type,
            func_name="setupDataFeed",
            **setup_kwargs,
        )

    if not setup_datafeed:
        if query_data is None:
            choice = click.confirm(
                colored_style("Build query data? Enter y if query id not available")
            )
            if not choice:
                query_id = colored_prompt("Enter query id", str)
            else:
                query_data = build_query_data()
                query_id = encode_hex(keccak(hexstr=query_data))
        else:
            query_id = encode_hex(keccak(hexstr=query_data))

        autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            token_address=token_address,
            account=account,
            transaction_type=transaction_type,
            func_name="fundFeed",
            _feedId=feed_id,
            _queryId=query_id,
            _amount=amount,
        )


@main.command()
@click.pass_context
def setupdatafeed(ctx: click.Context):
    account = ctx.obj["ACCOUNT"]
    chain = ctx.obj["CHAIN_ID"]
    fund_feed(
        account=account,
        chain=chain,
        amount=ctx.obj["AMOUNT"],
        transaction_type=ctx.obj["TRANSACTION_TYPE"],
    )


@main.command()
@click.pass_context
def approve_autopay(ctx: click.Context):
    account = ctx.obj["ACCOUNT"]
    w3 = ctx.obj["WEB3"]
    autopay_address = ctx.obj["AUTOPAY_ADDRESS"]
    token_address = ctx.obj["TOKEN_ADDRESS"]
    approve_transtacion(
        w3=w3,
        autopay_address=autopay_address,
        token_address=token_address,
        account=account,
        transaction_type=ctx.obj["TRANSACTION_TYPE"],
        amount=ctx.obj["AMOUNT"],
    )


@main.command()
def build_query():
    query_data = build_query_data()
    query_id = encode_hex(keccak(hexstr=query_data))
    click.echo(f"Query data: {query_data}")
    click.echo(f"Query id: {query_id}")
