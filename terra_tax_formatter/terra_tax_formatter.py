#!/usr/bin/env python3

from os import write
from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .terra_lcd import get_tx_info_by_txhash
from .stake_tax_csv_parsing import get_unique_tx_hashes
import csv, json, base64

def main():
    args = parse_args()
    validate_args(args)
    terra_address = args["terra_address"]
    input_file = args["input_file"]
    output_file = args["output_file"]

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

        headers = ["timestamp", "txhash", "type", "value"]
        new_rows = [headers]
        for tx in not_found:
            tx_info = tx["tx"]
            messages = tx_info["value"]["msg"]
            for message in messages:
                message_type = message["type"]
                message_value = message["value"]

                #convert legacy columbus-4 execute_msg from base64 encoded json to regular json
                if "execute_msg" in message_value.keys() and isinstance(message_value["execute_msg"], str):
                    message_value["execute_msg"] = json.loads(base64.b64decode(message_value["execute_msg"]))
            
                message_value = json.dumps(message_value)
                new_rows.append([tx["timestamp"], tx["txhash"], message_type, message_value])

        write_csv(output_file, new_rows)

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
