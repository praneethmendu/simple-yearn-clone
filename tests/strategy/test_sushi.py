import pytest;
from brownie import Strategy, Vault, Registry, Token, Wei, accounts, network, interface ;

PID = 3



@pytest.fixture
def dai():
    yield Token.at('0x8f3cf7ad23cd3cadbd9735aff958023239c6a063')

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
def sushi_router():
    yield interface.SushiRouter('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')


def test_strategy_accepts_dai( dai, pickle_token, pickle_jar, sushi_router):
    assert network.show_active() == 'polygon-main-fork'

    print(sushi_router.getAmountsOut(Wei("1 ether"), [pickle_token.address, dai.address]))
    # dai.approve(vault.address, Wei("0.02 ether"), {'from':dev})
    # vault.deposit(Wei("0.02 ether"), {'from':dev})
    # strategy.tend({'from':dev})
    # strategy.harvest({'from':dev})
    # print(pickle_jar.balanceOf(strategy.address))
    # assert pickle_jar.balanceOf(strategy.address) > 0
    # vault.withdraw(vault.balanceOf(dev), {'from':dev})

    # print(pickle_jar.balanceOf(strategy.address))