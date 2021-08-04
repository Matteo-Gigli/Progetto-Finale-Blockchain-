from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/81f5128aaaea4a319edd86d4c420c54b'))

account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address : {address} \n Your key: {privateKey}")