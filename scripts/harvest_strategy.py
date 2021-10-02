from brownie import Strategy, accounts
STRATEGY_ADDRESS = '0xABE502E5029B3738251d77AAb3519f8F64dA5500'

def main():
    dev = accounts.load('default')
    strategy = Strategy.at(STRATEGY_ADDRESS)
    harvest_tx = strategy.harvest({"from": dev})