#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .stake_tax_csv_parsing import get_unique_tx_hashes
import json, csv

def main():
    args = parse_args()
    validate_args(args)
    terra_address = args["terra_address"]
    input_file = args["input_file"]

    try:
        tx_map = make_txhash_map(get_all_tx_for_address(terra_address))
        txhashes = tx_map.keys()

        with open_file(input_file) as infile:
            reader = list(csv.DictReader(infile))
            unique_txs = get_unique_tx_hashes(reader)
            unique_txs = dict.fromkeys(unique_txs, True)

            not_found = []
            for txhash in txhashes:
                try:
                    unique_txs[txhash]
                except KeyError:
                    not_found.append(txhash)

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
