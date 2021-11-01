#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .terra_lcd import get_tx_info_by_txhash
from .stake_tax_csv_parsing import get_unique_tx_hashes
import csv

def main():
    args = parse_args()
    validate_args(args)
    terra_address = args["terra_address"]
    input_file = args["input_file"]

    try:
        all_fcd_txs = get_all_tx_for_address(terra_address)
        tx_map = make_txhash_map(all_fcd_txs)
        txhashes = tx_map.keys()

        not_found = []
        stake_tax_txs = []
        unique_txs = []
        with open_file(input_file) as infile:
            reader = list(csv.DictReader(infile))
            stake_tax_txs = get_unique_tx_hashes(reader)
            unique_txs = dict.fromkeys(stake_tax_txs, True)

        for txhash in txhashes:
            try:
                unique_txs[txhash]
            except KeyError:
                not_found.append(tx_map[txhash])

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
