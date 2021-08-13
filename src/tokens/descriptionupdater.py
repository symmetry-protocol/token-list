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
    url = "https://api.coingecko.com/api/v3/coins/{}?tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false".format(
        gecko_id)
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

    for k, v in descriptions.items():
        data[k] = v

    with open(token_descriptions_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print('done')


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

    solana_description = """SAIL is the first ever utility token build on Solana blockchain and fully distributed to the community.
SAIL is the main utility token for the SAIL ecosystem which will provide Governance, DeFi, Vault and NFT marketplace.
Four additional tokens will be added to the SAIL ecosystem :

gSAIL (Governance)
dSAIL (DeFi)
vSAIL (Vault)
nSAIL (Opensail NFT Marketplace)"""
    symbol = 'SAIL'
    print(symbol)
    print('---')
    manual_update_descriptions({symbol: solana_description})
