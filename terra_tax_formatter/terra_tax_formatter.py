#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map

def main():
    args = parse_args()
    validate_args(args)
    terra_address = args["terra_address"]

    try:
        tx_map = make_txhash_map(get_all_tx_for_address(terra_address))
        txhashes = tx_map.keys()
    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
