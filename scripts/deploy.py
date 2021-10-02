from pathlib import Path
import yaml
import click

from brownie import Token, Vault, Registry, accounts, network, web3, Wei
from eth_utils import is_checksum_address
from semantic_version import Version


DEFAULT_VAULT_NAME = lambda token: f"{token.symbol()} yVault"
DEFAULT_VAULT_SYMBOL = lambda token: f"yv{token.symbol()}"
DEFAULT_ACCOUNT = '0xf0e3fF0255cd62C86E96Ba5dE097325E91f49245'
REGISTRY_ADDRESS = '0x5a539A5CfA70f3f6DB4D0ab42FB5C609CF9B6763'
# dai
TOKEN_ADDRESS = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
# tst TOKEN_ADDRESS = "0x5a539A5CfA70f3f6DB4D0ab42FB5C609CF9B6763"
PACKAGE_VERSION = yaml.safe_load(
    (Path(__file__).parent.parent / "ethpm-config.yaml").read_text()
)["version"]


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
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")

    registry = Registry.at(
        get_address("Vault Registry", default=REGISTRY_ADDRESS)
    )
    try:
        latest_release = Version(registry.latestRelease())
    except:
        latest_release = Version('0.0.1')
    
    num_releases = registry.numReleases() - 1
    target_release_index = num_releases
    release_delta = 0
    click.echo(
        f"""
        Release Information

        latest release version: {latest_release}
          latest release index: {num_releases}
         local package version: {PACKAGE_VERSION}
        """
    )
    use_proxy = False  # NOTE: Use a proxy to save on gas for experimental Vaults
    if Version(PACKAGE_VERSION) <= latest_release:
        click.echo(
            f"""
        Recommended Releases

        DO NOT USE => 0-2
        0.3.2 => 3
        0.3.3 => 4
        0.3.4 => 5 (DO NOT USE) 
        0.3.5 => 6
        0.4.0 => 7 (DO NOT USE)
        0.4.1 => 8
        """
        )

        target_release_index = click.prompt(
            "Please select a target release index from options or press enter for latest release:",
            type=click.Choice([str(i) for i in range(num_releases + 1)]),
            default=num_releases,
            )
        # if click.confirm("Deploy a Proxy Vault"):
        #     use_proxy = True
    elif Version(PACKAGE_VERSION) > latest_release:
        target_release_index = num_releases + 1
        if not click.confirm(f"Deploy {PACKAGE_VERSION} as new release"):
            return

    token = Token.at(get_address('Token address', TOKEN_ADDRESS ))

    if use_proxy:
        gov_default = (
            "0x16388463d60FFE0661Cf7F1f31a7D658aC790ff7"  # strategist msig, no ENS
        )
    else:
        gov_default = DEFAULT_ACCOUNT
    gov = get_address("Yearn Governance", default=gov_default)

    rewards = get_address("Rewards contract", default=DEFAULT_ACCOUNT)   
    # guardian = gov
    # if use_proxy == False:
    #     guardian = get_address("Vault Guardian", default=DEFAULT_ACCOUNT)
    # management = get_address("Vault Management", default=DEFAULT_ACCOUNT)
    name = click.prompt(f"Set description", default=DEFAULT_VAULT_NAME(token))
    symbol = click.prompt(f"Set symbol", default=DEFAULT_VAULT_SYMBOL(token))
    release_delta = num_releases - target_release_index
    click.echo()
    # target_release = (
    #     Vault.at(registry.releases(target_release_index)).apiVersion()
    #     if release_delta >= 0
    #     else PACKAGE_VERSION
    # )

    click.echo(
        f"""
    Vault Deployment Parameters

         use proxy: {use_proxy}
     release delta: {release_delta}
     token address: {token.address}
      token symbol: {DEFAULT_VAULT_SYMBOL(token)}
        governance: {gov}
           rewards: {rewards}
              name: '{name}'
            symbol: '{symbol}'
    """
    )
    # removed from list
    # target release: {target_release}
    # management: {management}
    # guardian: {guardian}

    if click.confirm("Deploy New Vault"):
        args = [
            token,
            gov,
            rewards,
            # NOTE: Empty string `""` means no override (don't use click default tho)
            name if name != DEFAULT_VAULT_NAME(token) else "",
            symbol if symbol != DEFAULT_VAULT_SYMBOL(token) else "",
        ]
        if use_proxy:
            # NOTE: Must always include guardian, even if default
            # args.insert(2, guardian)
            args.append(release_delta)
            txn_receipt = registry.newExperimentalVault(*args, {"from": dev})
            vault = Vault.at(txn_receipt.events["NewExperimentalVault"]["vault"])
            click.echo(f"Experimental Vault deployed [{vault.address}]")
            click.echo("    NOTE: Vault is not registered in Registry!")
        else:
            # args.append(guardian)
            # args.append(management)
            vault = dev.deploy(Vault)
            vault.initialize(*args)
            click.echo(f"New Vault Release deployed [{vault.address}]")
            val = click.prompt('set deposit limit', default='5')
            if ( not val.isnumeric() ):
                val = '100'
            vault.setDepositLimit(Wei("{} ether".format(val)), {'from': dev})

            click.echo(f"New deposit limit [{vault.depositLimit()}] {vault.address}")
            # newReleaseReceipt = registry.newRelease(vault.address, {'from': dev})  
            # click.echo(
            #     f"added to registery! err: {newReleaseReceipt.revert_msg}"
            # )
