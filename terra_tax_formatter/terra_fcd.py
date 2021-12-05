import requests
from time import sleep

from .exceptions import ConverterCaughtError

base_api_url = "https://fcd.terra.dev/v1"
tx_endpoint = "/txs"
base_wasm_url = "https://fcd.terra.dev/terra/wasm/v1beta1"
contract_endpoint = "/contracts/<contract_address>"
base_ibc_url = "https://fcd.terra.dev/ibc/apps/transfer/v1"
denom_trace_endpoint = "/denom_traces/<hash>"
base_cosmos_url = "https://fcd.terra.dev/cosmos/bank/v1beta1"
denom_metadata_endpoint = "/denoms_metadata/<denom>"

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
                sleep(default_wait_time)
                offset = data["next"]
            else:
                break
        return txs
    except Exception as err:
        raise ConverterCaughtError("There was an error reaching out to the Terra FCD API for getting all transactions, please try again later")

def make_txhash_map(txs):
    return  {tx["txhash"]: tx for tx in txs}

def get_contract_info(contract_address):
    try:
        contract_info = requests.get(base_wasm_url + contract_endpoint.replace("<contract_address>", contract_address))
        contract_info.raise_for_status()
        sleep(default_wait_time)
        return contract_info.json()
    except:
        raise ConverterCaughtError(f"There was an error reaching out to the Terra FCD API for the contract address {contract_address} data, please try again later")

def get_ibc_denom_trace(hash):
    try:
        denom_trace = requests.get(base_ibc_url + denom_trace_endpoint.replace("<hash>", hash))
        denom_trace.raise_for_status()
        sleep(default_wait_time)
        return denom_trace.json()
    except:
        raise NameError(f"There was an error reaching out to the Terra FCD API for the IBC denom trace {hash} data, please try again later")

def get_denom_metadata(denom):
    try:
        denom_metadata = requests.get(base_cosmos_url + denom_metadata_endpoint.replace("<denom>", denom))
        denom_metadata.raise_for_status()
        sleep(default_wait_time)
        return denom_metadata.json()
    except:
        raise NameError(f"There was an error reaching out to the Terra FCD API for the denom metadata {denom} data, please try again later")