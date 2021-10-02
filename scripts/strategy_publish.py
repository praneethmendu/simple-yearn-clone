from brownie import Strategy, accounts, config, network, project, web3, Vault, Wei

def main():
    # Strategy.publish_source(
    # Strategy.at('0x7CBA8B272B9DA3cABB583dD1497Df84d415768d5'))


    file1 = open("myfile.txt","w")

    file1.write(Strategy.get_verification_info()['flattened_source'])
    file1.close() 