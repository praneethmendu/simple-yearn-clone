import pytest
from brownie import Strategy, Vault, Registry, Token, Wei, accounts, network, interface 

PID = 3

@pytest.fixture
def dev():
    yield accounts.load('default')

@pytest.fixture
def vault():
    yield Vault.at('0x3Bf166d03A9C2894f047d025F2bce7cc72fD00c2')

@pytest.fixture
def dai(vault):
    yield Token.at(vault.token())

@pytest.fixture
def pickle_token():
    yield Token.at('0x2b88ad57897a8b496595925f43048301c37615da')

@pytest.fixture
def pickle_jar():
    yield Token.at('0x0519848e57Ba0469AA5275283ec0712c91e20D8E')

@pytest.fixture
def pickle_farm():
    yield interface.PickleFarm('0x20B2a3fc7B13cA0cCf7AF81A68a14CB3116E8749')

@pytest.fixture
def strategy(vault, dev):
    strategy = Strategy.deploy(vault, {"from": dev})
    vault.addStrategy(strategy, 9500, Wei("0.01 ether"), Wei("1 ether"), 0, {"from": dev})
    yield strategy

def test_strategy_accepts_dai(dev, dai, vault, strategy, pickle_jar, pickle_farm):
    assert network.show_active() == 'polygon-main-fork'
    dai.approve(vault.address, Wei("0.02 ether"), {'from':dev})
    vault.deposit(Wei("0.02 ether"), {'from':dev})
    # strategy.tend({'from':dev})
    strategy.harvest({'from':dev})

    print(pickle_farm.userInfo(PID, strategy))
    vault.withdraw(vault.balanceOf(dev), {'from':dev})

    print(pickle_jar.balanceOf(strategy.address))