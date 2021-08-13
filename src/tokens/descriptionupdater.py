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

    solana_description = """Hedget is a non-custodial options trading platform built on Ethereum and Chromia. Chromia is a relational blockchain database which allows complex transactions to be executed while maintaining decentralization and transparency. 

Users can buy and sell options products on Hedget by providing collateral in the form of cryptocurrencies (both stablecoins and traditional cryptocurrencies). It also allows users to protect against downside risk for their crypto holdings as well as their debt positions on other lending protocols such as Compound and Aave.

how hedget works
 

What are HGET tokens?
HGET is the platform’s native token for governance and utility. HGET is used to propose updates to the protocol. Besides that, HGET tokens need to be staked to create and trade option products. 

In the future, HGET tokens will also be used as a security measure for leveraged options. Option sellers who want to provide options without a 1:1 collateral will need to stake HGET tokens.

How does Hedget work?
The Hedget platform runs on three main components:

ESC: Ethereum smart contract which handles token deposit, withdrawals and physical settlement.

CTD: Chromia-based dApp which handles trade, contract ownership and acts as a bridge to interact with the ESC.

CSW: Client wallet and trading UI which carries out commands using ESC and CTD.
 

hedget architecture

Users will be required to put up collateral as they create different option products in order to guarantee the possibility of exercising the option. In the first version, 100% collateral is required. Physical and cash settlement is available. However, the platform would only allow certain combinations of expiry dates and strike prices to ensure that sufficient liquidity is available.

Hedget will also incorporate a decentralized exchange for trading option tokens. Options would be priced in stablecoins such as DAI, USDC and BUSD.

Option tokens are stored in a non-custodial manner, which means users are in control of their own funds. Assets are only transferred when option contracts are traded or exercised.
 

There is a 0.02% maker fee and 0.04% taker fee on the underlying assets. The difference between the two fees would be locked for 2 years in a special reserve governed by Hedget’s DAO. In the first 3 to 4 years, 0.02% settlement fees would be paid via the liquidity mining pool.

More details regarding the inner workings of Hedget can be found in their whitepaper.

 

How do I get HGET?
You can obtain HGET by purchasing them from an exchange such as FTX or Uniswap. Besides the two exchanges,you can find HGET trading on other various centralized and decentralized cryptocurrency exchanges."""
    symbol = 'HGET'
    print(symbol)
    print('---')
    manual_update_descriptions({symbol: solana_description})
