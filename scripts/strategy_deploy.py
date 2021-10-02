from pathlib import Path

from brownie import Strategy, accounts, config, network, project, web3, Vault, Wei
from eth_utils import is_checksum_address
import click
DEFAULT_VAULT = '0x7445cd06B0Dd9A31448d4DE163A80731F4D8589e'
# DEFAULT_VAULT = '0x3Bf166d03A9C2894f047d025F2bce7cc72fD00c2'


def get_address(msg: str, default: str = None) -> str:
    val = click.prompt(msg, default=default)

    # Keep asking user for click.prompt until it passes
    while True:

        if is_checksum_address(val):
            return val
        elif addr := web3.ens.address(val):
            click.echo(f"Found ENS '{val}' [{addr}]")
            return addr

        click.echo(
            f"I'm sorry, but '{val}' is not a checksummed address or valid ENS record"
        )
        # NOTE: Only display default once
        val = click.prompt(msg)


def main():
    print(f"You are using the '{network.show_active()}' network")
    dev = accounts.load('default')
    print(f"You are using: 'dev' [{dev.address}]")

    if input("Is there a Vault for this strategy already? y/[N]: ").lower() == "y":
        vault = Vault.at(get_address("Deployed Vault:", DEFAULT_VAULT))
    else:
        print("You should deploy one vault using scripts from Vault project")
        return  # TODO: Deploy one using scripts from Vault project

    # print(
    #     f"""
    # Strategy Parameters

    #  token: {vault.token()}
    #   name: '{vault.name()}'
    # symbol: '{vault.symbol()}'
    # """
    # )
    publish_source = False
    
    if network.show_active() != 'polygon-main-fork':
        if input("publish_source? y/[N]: ").lower() == "y":
            publish_source = True

    if input("Deploy Strategy? y/[N]: ").lower() != "y":
        return

    strategy = Strategy.deploy(vault.address, {"from": dev}, publish_source=publish_source)

    minDebtPerHarvest = click.prompt('minDebtPerHarvest', default=Wei("0.01 ether"))
    maxDebtPerHarvest = click.prompt('maxDebtPerHarvest', default=Wei("1 ether"))

    # vault.addStrategy(strategy, 9500, minDebtPerHarvest, maxDebtPerHarvest, 0, {"from": dev})
    