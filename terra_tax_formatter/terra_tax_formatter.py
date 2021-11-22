#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .stake_tax_csv_parsing import get_unique_tx_hashes, start_csv_process, track_job, download_csv, parse_csv_file_object
import csv
from datetime import datetime
from .identifiers import identify

base_finder_url = "https://finder.terra.money/"

def main():
    args = parse_args()
    validate_args(args)

    terra_address = args["terra_address"]
    input_file = args["input_file"]
    output_file = args["output_file"]
    mode = args["mode"]

    try:
        stake_tax_txs = []
        stake_tax_unique_txs = {}
        staketax_reader = None

        #download file directly from stake.tax
        if mode == "file_download":
            job_start = start_csv_process(terra_address)
            track_job(job_start["job_id"])
            in_mem_csv = download_csv(job_start["job_id"])

            staketax_reader = parse_csv_file_object(in_mem_csv)
            if len(staketax_reader) > 0:
                #save the file if it has rows
                write_csv_dict(output_file, list(staketax_reader[0].keys()), staketax_reader, restval="")
            else:
                print("No transactions found for the stake.tax output")

            stake_tax_txs = get_unique_tx_hashes(staketax_reader)
            stake_tax_unique_txs = dict.fromkeys(stake_tax_txs, True)

        #upload file from system
        elif mode == "file_input":
            with open_file(input_file) as infile:
                staketax_reader = list(csv.DictReader(infile))
                stake_tax_txs = get_unique_tx_hashes(staketax_reader)
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
            "ibc_denom_traces": {}
        }

        for tx in not_found:
            #skip failed txs
            if "code" in tx.keys() and tx["code"] != 0:
                continue

            tx_info = tx["tx"]
            messages = tx_info["value"]["msg"]
            logs = tx["logs"]
            date = datetime.strptime(tx["timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%d/%Y %H:%M:%S")

            #add a new row per message in the TX (might need to change if messages don't correspond directly to all actions)
            for index, (message, log) in enumerate(zip(messages, logs)):
                url = f"{base_finder_url}{tx['chainId']}/tx/{tx['txhash']}"

                #get a list of possible message identities by identifying the message
                possible_identities = identify(message, log)

                #attempt to parse out the data for the message
                parsed_value = None
                for identity in possible_identities:
                    try:
                        parsed_value = identity["parser"](message, log, fcd_data_cache)
                    except Exception as err:
                        #skip this identity parser if parsing fails
                        pass
                
                new_data = {"Date": date, "Transaction ID": tx['txhash'], "Finder URL": url}

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

        headers = ["Date", "Received Quantity", "Received Currency", "Sent Quantity", "Sent Currency" ,"Fee Amount", "Fee Currency", "Tag", "Transaction ID", "Finder URL"]

        write_csv_dict(output_file + "-missing", headers, new_rows, restval="")

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
