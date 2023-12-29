import asyncio
import random
import time

import aiohttp
import csv
from web3 import Web3

#введи сети анализа на транзакции
chains = ['polygon']

#если True смотрит по адресам, если False по приватникам
ADDRESSA = False

# меняем рпс на свои
DATA = {
    'ethereum':     {'rpc': ['https://rpc.ankr.com/eth'],       'scan': 'https://etherscan.io/tx',              'token': 'ETH', 'chain_id': 1},
    'optimism':     {'rpc': ['https://rpc.ankr.com/optimism'],  'scan': 'https://optimistic.etherscan.io/tx',   'token': 'ETH', 'chain_id': 10},
    'bsc':          {'rpc': ['https://rpc.ankr.com/bsc'],       'scan': 'https://bscscan.com/tx',               'token': 'BNB', 'chain_id': 56},
    'polygon':      {'rpc': ['https://endpoints.omniatech.io/v1/matic/mainnet/public'],   'scan': 'https://polygonscan.com/tx',           'token': 'MATIC','chain_id': 137},
    'polygon_zkevm':{'rpc': ['https://zkevm-rpc.com'],          'scan': 'https://zkevm.polygonscan.com/tx',     'token': 'ETH', 'chain_id': 1101},
    'arbitrum':     {'rpc': ['https://rpc.ankr.com/arbitrum'],  'scan': 'https://arbiscan.io/tx',               'token': 'ETH', 'chain_id': 42161},
    'avalanche':    {'rpc': ['https://rpc.ankr.com/avalanche'], 'scan': 'https://snowtrace.io/tx',              'token': 'AVAX','chain_id': 43114},
    'fantom':       {'rpc': ['https://rpc.ankr.com/fantom'],    'scan': 'https://ftmscan.com/tx',               'token': 'FTM', 'chain_id': 250},
    'nova':         {'rpc': ['https://nova.arbitrum.io/rpc'],   'scan': 'https://nova.arbiscan.io/tx',          'token': 'ETH', 'chain_id': 42170},
    'zksync':       {'rpc': ['https://mainnet.era.zksync.io'],  'scan': 'https://explorer.zksync.io/tx',        'token': 'ETH', 'chain_id': 324},
    'celo':         {'rpc': ['https://1rpc.io/celo'],           'scan': 'https://celoscan.io/tx',               'token': 'CELO','chain_id': 42220},
    'gnosis':       {'rpc': ['https://1rpc.io/gnosis'],         'scan': 'https://gnosisscan.io/tx',             'token': 'xDAI','chain_id': 100},
    'core':         {'rpc': ['https://rpc.coredao.org'],        'scan': 'https://scan.coredao.org/tx',          'token': 'CORE','chain_id': 1116},
    'harmony':      {'rpc': ['https://api.harmony.one'],        'scan': 'https://explorer.harmony.one/tx',      'token': 'ONE', 'chain_id': 1666600000},
    'klaytn':       {'rpc': ['https://klaytn.blockpi.network/v1/rpc/public'], 'scan': 'https://klaytnscope.com/tx/',      'token': 'KLAY', 'chain_id': 1666600000},
    'moonbeam':     {'rpc': ['https://moonbeam.public.blastapi.io'],  'scan': 'https://moonscan.io/tx',               'token': 'GLMR','chain_id': 1284},
    'moonriver':    {'rpc': ['https://moonriver.public.blastapi.io'],'scan': 'https://moonriver.moonscan.io/tx','token': 'MOVR','chain_id': 1285},
    'linea':        {'rpc': ['https://rpc.linea.build'],        'scan': 'https://lineascan.build/tx',           'token': 'ETH', 'chain_id': 59144},
    'base':         {'rpc': ['https://mainnet.base.org'],       'scan': 'https://basescan.org/tx',              'token': 'ETH', 'chain_id': 8453},
}


def main():
    with open('addresses.txt', 'r') as file:
        wallet_addresses = [line.strip() for line in file if line.strip()]
    with open('keys.txt', 'r') as file:
        keys = [line.strip() for line in file if line.strip()]

    blak_list = []

    if ADDRESSA:
        max_acc = len(wallet_addresses)
        for current_account, address in enumerate(wallet_addresses):
            count = 0
            for chain in chains:
                w3 = Web3(Web3.HTTPProvider(random.choice(DATA[chain]['rpc'])))
                transaction_count = w3.eth.get_transaction_count(w3.to_checksum_address(address))
                if transaction_count > 0:
                    count = transaction_count
                    chain_ = chain
                    print(f'[{current_account + 1}/{max_acc}]{address}: {chain_}: {count}')

            time.sleep(2)

            if count == 0:
                blak_list.append(address)
        print(f'\n\n\nНи одной транзакции у {len(blak_list)} кошельков:')

        for add in blak_list:
            print(add)

    else:
        max_acc = len(keys)
        for current_account, key in enumerate(keys):
            count = 0
            for chain in chains:
                w3 = Web3(Web3.HTTPProvider(random.choice(DATA[chain]['rpc'])))
                account = w3.eth.account.from_key(key)
                address = account.address
                transaction_count = w3.eth.get_transaction_count(w3.to_checksum_address(address))
                if transaction_count > 0:
                    count = transaction_count
                    chain_ = chain
                    print(f'[{current_account + 1}/{max_acc}]{address}: {chain_}: {count}')

            time.sleep(2)

            if count == 0:
                blak_list.append(key)
        print(f'\n\n\nНи одной транзакции у {len(blak_list)} приватников:')
        for add in blak_list:
            print(add)


if __name__ == "__main__":
    main()
    print("All done")
