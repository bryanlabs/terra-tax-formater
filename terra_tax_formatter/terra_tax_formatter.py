#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .stake_tax_csv_parsing import start_csv_process, track_job, download_csv
import csv
from datetime import datetime
from .identifiers import identify
from .formatters import FORMATS


import sys, traceback


base_finder_url = "https://finder.terra.money/"

def main():
    args = parse_args()
    validate_args(args)

    terra_address = args["terra_address"]
    input_file = args["input_file"]
    output_file = args["output_file"]
    mode = args["mode"]
    formatter = FORMATS[args["format"]]()

    try:
        stake_tax_txs = []
        stake_tax_unique_txs = {}

        #download file directly from stake.tax
        if mode == "file_download":
            job_start = start_csv_process(terra_address)
            track_job(job_start["job_id"])
            in_mem_csv = download_csv(job_start["job_id"], formatter)

            values = formatter.parse_response_data(in_mem_csv)
            
            if len(values) > 0:
                #save the file if it has rows
                formatter.write_data(values, get_file_realpath(output_file))
            else:
                print("No transactions found for the stake.tax output")

            stake_tax_txs = formatter.get_unique_tx_hashes(values)
            stake_tax_unique_txs = dict.fromkeys(stake_tax_txs, True)

        #upload file from system
        elif mode == "file_input":
            with open_file(get_file_realpath(input_file), file_mode=formatter.read_file_mode) as infile:
                values = formatter.parse_file_data(infile)
                stake_tax_txs = formatter.get_unique_tx_hashes(values)
                stake_tax_unique_txs = dict.fromkeys(stake_tax_txs, True)

        all_fcd_txs = get_all_tx_for_address(terra_address)
        tx_map = make_txhash_map(all_fcd_txs)
        txhashes = tx_map.keys()

        not_found = []

        #get unique list of transactions that dont exist from stake.tax
        for txhash in txhashes:
            try:
                stake_tax_unique_txs[txhash]
            except KeyError:
                not_found.append(tx_map[txhash])

        #for all of the txs not found in stake.tax output, build rows for each
        new_rows = []

        fcd_data_cache = {
            "contracts": {},
            "ibc_denom_traces": {},
            "denoms": {}
        }

        for tx in not_found:
            #skip failed txs
            if "code" in tx.keys() and tx["code"] != 0:
                continue

            tx_info = tx["tx"]
            messages = tx_info["value"]["msg"]
            logs = tx["logs"]

            date = formatter.format_date(datetime.strptime(tx["timestamp"], "%Y-%m-%dT%H:%M:%SZ"))

            #add a new row per message in the TX (might need to change if messages don't correspond directly to all actions)
            for index, (message, log) in enumerate(zip(messages, logs)):
                url = f"{base_finder_url}{tx['chainId']}/tx/{tx['txhash']}"

                #get a list of possible message identities by identifying the message
                possible_identities = identify(message, log)

                # #attempt to parse out the data for the message
                parsed_value = None
                for identity in possible_identities:
                    try:
                        parsed_value = identity["parser"](message, log, fcd_data_cache)
                    except Exception as err:
                        #skip this identity parser if parsing fails
                        pass
                
                new_data = {"date": date, "txhash": tx['txhash'], "finder_url": url}

                #dict merge, let parsed values overwrite new data if needed
                if parsed_value and not isinstance(parsed_value, list):
                    new_data = {**new_data, **parsed_value}
                    new_rows.append(new_data)
                #list returns from parsed, loop through and dict merge
                elif parsed_value and isinstance(parsed_value, list):
                    for parsed in parsed_value:
                        new_data = {**new_data, **parsed}
                        new_rows.append(new_data)
                else:
                    new_rows.append(new_data)

                new_rows.append(new_data)

        formatted_data = formatter.format_data(new_rows)
        formatter.write_data(formatted_data, get_file_realpath(output_file + "-missing"))


    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(traceback.format_exc())
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
