import requests
from time import sleep

from .exceptions import ConverterCaughtError

base_api_url = "https://fcd.terra.dev/v1"
tx_endpoint = "/txs"
default_wait_time = 5


def get_paged_response(terra_address, offset=None):
    offset_str = ""
    if(offset):
        offset_str = f"&offset={offset}"
    resp = requests.get(f"{base_api_url}{tx_endpoint}?account={terra_address}&limit=100{offset_str}")
    resp.raise_for_status()
    return resp.json()
    

def get_all_tx_for_address(terra_address):
    txs = []
    offset = None
    try:

        while True:
            data = get_paged_response(terra_address, offset=offset)
            txs += data["txs"]
            
            if "next" in data.keys() and data["next"]:
                sleep(5)
                offset = data["next"]
            else:
                break
        return txs
    except Exception as err:
        print(err)
        raise ConverterCaughtError("There was an error reaching out to the Terra FCD API, please try again later")

def make_txhash_map(txs):
    return  {tx["txhash"]: tx for tx in txs}
        