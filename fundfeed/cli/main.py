import click
from eth_utils import keccak
from eth_utils import encode_hex
from fundfeed.cli.utils import RequiredIf
from fundfeed.cli.utils import build_query_data
from chained_accounts import find_accounts
from chained_accounts import ChainedAccount
from fundfeed.tip_all import one_time_tips_funding
from fundfeed.transaction import autopay_transaction
from fundfeed.transaction import approve_transtacion
from fundfeed.fund_all import fund_feed
from fundfeed.transaction import constants
from fundfeed.cli.utils import colored_style
from fundfeed.cli.utils import colored_prompt


@click.group()
@click.argument('account_name', type=str)
@click.argument('chain', type=int)
@click.option('--query-data', '-qd', type=str, default=None)
@click.pass_context
def main(
    ctx: click.Context,
    account_name: ChainedAccount,
    chain: int,
    query_data: str,
):
    """Fund Autopay!"""
    try:
        account = find_accounts(name=account_name)[0]
    except IndexError:
        click.echo(colored_style("No account found with that name!\n"))
        click.echo(colored_style("Consider adding it using chained add <name> <private-key> <chain-ids> command"))
        return

    w3, autopay_address, token_address = constants(chain=chain)

    ctx.ensure_object(dict)

    ctx.obj["ACCOUNT"] = account
    ctx.obj["CHAIN_ID"] = chain
    ctx.obj["QUERY_DATA"] = query_data
    ctx.obj["WEB3"] = w3
    ctx.obj["AUTOPAY_ADDRESS"] = autopay_address
    ctx.obj["TOKEN_ADDRESS"] = token_address


@main.command()
@click.option('--amount', '-amt', type=int, required=True, prompt=colored_style("Enter tip amount"), confirmation_prompt=True)
@click.option('--tip-all/--single-tip')
@click.pass_context
def tip(ctx: click.Context, amount: int, tip_all: bool):
    account = ctx.obj["ACCOUNT"]
    w3 = ctx.obj["WEB3"]
    autopay_address=ctx.obj["AUTOPAY_ADDRESS"]
    token_address=ctx.obj["TOKEN_ADDRESS"]

    tip_amount = int(amount * 1e18)

    if tip_all:
        one_time_tips_funding(w3, account, autopay_address, token_address, tip_amount)
    else:
        query_data = ctx.obj['QUERY_DATA']
        if query_data is None:
            choice = click.confirm(colored_style("Build query data? Enter y if query data not available"))
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
            func_name="tip",
            _queryId=query_id,
            _queryData=query_data,
            _amount=tip_amount
        )


@main.command()
@click.option('--setup-datafeed/--fund-only')
@click.option('--reward', '-rwd', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--window', '-win', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--start-time', '-st', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--interval', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--price-threshold', '-pt', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--reward-increase', '-ri', cls=RequiredIf, required_if='setup_datafeed', type=int)
@click.option('--feed-id', cls=RequiredIf, required_if='fund_only', type=str)
@click.option('--amount', '-amt', required=True, type=int, prompt=colored_style("Enter funding amount"))
@click.pass_context
def fundfeed(
    ctx: click.Context,
    setup_datafeed: bool,
    reward: int,
    window: int,
    start_time: int,
    interval: int,
    price_threshold: int,
    reward_increase: int,
    feed_id: str,
    amount: int
):

    query_data = ctx.obj["QUERY_DATA"]
    account = ctx.obj["ACCOUNT"]
    chain = ctx.obj["CHAIN_ID"]
    w3 = ctx.obj["WEB3"]
    autopay_address=ctx.obj["AUTOPAY_ADDRESS"]
    token_address=ctx.obj["TOKEN_ADDRESS"]

    if setup_datafeed:
        if query_data is None:
            choice = click.confirm(colored_style("Build query data? Enter y if query data not available"))
            if not choice:
                query_data = colored_prompt("Enter query data", str)
            else:
                query_data = build_query_data()
        setup_kwargs = {
            "_queryId": encode_hex(keccak(hexstr=query_data)),
            "_reward": reward,
            "_startTime": start_time,
            "_interval": interval,
            "_window": window,
            "_priceThreshold": price_threshold,
            "_rewardIncreasePerSecond": reward_increase,
            "_queryData": query_data,
            "_amount": int(amount*1e18)
        }
        autopay_transaction(
            w3=w3,
            autopay_address=autopay_address,
            token_address=token_address,
            account=account,
            func_name="setupDataFeed",
            **setup_kwargs,
        )

    if not setup_datafeed:
        if query_data is None:
            choice = click.confirm(colored_style("Build query data? Enter y if query id not available"))
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
            func_name="fundFeed",
            _feedId=feed_id,
            _queryId=query_id,
            _amount=int(amount*1e18),
        )


@main.command()
@click.option('--amount', '-amt', required=True, type=int, prompt=colored_style("Enter funding amount"))
@click.pass_context
def setupdatafeed(ctx: click.Context, amount):
    account = ctx.obj["ACCOUNT"]
    chain = ctx.obj["CHAIN_ID"]
    fund_feed(account=account, chain=chain, amount=int(amount * 1e18))


@main.command()
@click.option('--amount', '-amt', required=True, type=int, prompt=colored_style("Enter approve amount"))
@click.pass_context
def approve_autopay(ctx: click.Context, amount: int):
    account = ctx.obj["ACCOUNT"]
    w3=ctx.obj["WEB3"]
    autopay_address=ctx.obj["AUTOPAY_ADDRESS"]
    token_address=ctx.obj["TOKEN_ADDRESS"]
    approve_transtacion(
        w3=w3,
        autopay_address=autopay_address,
        token_address=token_address,
        account=account,
        amount=int(amount * 1e18)
    )

@main.command()
def build_query():
    query_data = build_query_data()
    query_id = encode_hex(keccak(hexstr=query_data))
    click.echo(f"Query data: {query_data}")
    click.echo(f"Query id: {query_id}")
