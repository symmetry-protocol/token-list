import json
import requests
from time import sleep
from pprint import pprint

def _get_coins_gecko():
    # response = [ {'id': '01coin', 'name': '01coin', 'symbol': 'zoc'}, ...]
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = json.loads(requests.get(url).text)
    return response

def _get_coins_solana_registry():
    """ [{
            'address': 'cjZmbt8sJgaoyWYUttomAu5LJYU44ZrcKTbzTSEPDVw',
            'chainId': 101,
            'decimals': 9,
            'extensions': {'website': 'https://raydium.io/'},
            'logoURI': 'https://raw.githubusercontent.com/solana-labs/ ...',
            'name': 'Raydium LP Token V4 (LIKE-USDC)',
            'symbol': 'LIKE-USDC',
            'tags': ['lp-token']
        }, ... ]
    """
    with open('./solana.tokenlist.json', encoding='utf-8') as f:
        data = json.loads(f.read())
    token_list = data['tokens']
    return token_list

def _get_description_gecko(gecko_id):
    url = "https://api.coingecko.com/api/v3/coins/{}?tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false".format(gecko_id)
    response = json.loads(requests.get(url).text)
    description = ""
    if 'description' in response and 'en' in response['description']:
        description = response['description']['en']
    return description


counter = 0
def _get_descriptions(tokens):
    global counter

    descriptions = {}
    for token in tokens:
        counter += 1
        print("#{}".format(counter))

        if 'extensions' not in token or 'coingeckoId' not in token['extensions']: 
            print('\t\ttoken {} did not have a gecko id, skipping it ...'.format(counter))
            continue
        gecko_id = token['extensions']['coingeckoId']
        symbol = token['symbol']
        description = _get_description_gecko(gecko_id)

        if len(description) > 0: 
            descriptions[symbol] = description
        sleep(60/50)

        print('--->', symbol, ':')
        pprint(description)
        print('---------')

    return descriptions

def _update_descriptions(descriptions):
    """ descriptions = {
            'BTC': <description str>, ...
        }
    """
    token_descriptions_filepath = './token_descriptions.json'
    with open(token_descriptions_filepath, encoding='utf-8') as f:
        data = json.loads(f.read())

    for k,v in descriptions.items():
        data[k] = v

    with open(token_descriptions_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)



def auto_update_descriptions():
    tokens = _get_coins_solana_registry()
    descriptions = _get_descriptions(tokens)
    _update_descriptions(descriptions)

def manual_update_descriptions(descriptions):
    """ descriptions = {
            'BTC': <description str>, ...
        }
    """
    _update_descriptions(descriptions)

if __name__ == "__main__":
    # auto_update_descriptions()

    solana_description = """Solana is building the architecture of their blockchain based on Proof of History (PoH); a proof for verifying order and passage of time between events. The purpose of PoH is used to encode the trustless passage of time into a ledger. A Proof of Stake (PoS) consensus mechanism is then leveraged for confirmation of the current sequence produced by the Proof of History generator. PoS is also used for voting and selecting the next Proof of History generator node and for punishing any validators that act against the interest of the network.

Up to 710k transactions/second on a 1gb network without data partitioning

Proof of History
Encoding time as data in the replicated state allows for simple and efficient proofs and protocols.

Performant System Architecture
The network is arranged for maximum throughput and high availability. Our smart contracts bytecode is based on Berkeley Packet Filter designed for fast execution.

Fast Proof of Replication
A fast streaming Proof of Replication is designed for storing a large distributed ledger.

Consensus independent from transaction flow
Transactions flow through the network independent of consensus and are limited only by hardware."""
    manual_update_descriptions({'SOL': solana_description})
