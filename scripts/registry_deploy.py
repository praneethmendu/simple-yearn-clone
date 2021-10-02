from brownie import Registry, accounts

def main():
    default = accounts.load('default')
    default.deploy(Registry)