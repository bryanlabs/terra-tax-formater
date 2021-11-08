#!/usr/bin/env python3

from .files import *
from .arg_parsing import parse_args, validate_args
from .exceptions import ConverterCaughtError
from .terra_fcd import get_all_tx_for_address, make_txhash_map
from .terra_lcd import get_tx_info_by_txhash
from .stake_tax_csv_parsing import get_unique_tx_hashes, start_csv_process, track_job, download_csv, parse_csv_file_object
import csv
from datetime import datetime

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
                write_csv_dict(output_file + "-stake-tax-output", list(staketax_reader[0].keys()), staketax_reader, restval="")
            else:
                print("No transactions found for the stake.tax output")

            stake_tax_txs = get_unique_tx_hashes(staketax_reader)
            stake_tax_unique_txs = dict.fromkeys(stake_tax_txs, True)

        #upload file from system
        elif mode == "file_upload":
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
        for tx in not_found:
            tx_info = tx["tx"]
            messages = tx_info["value"]["msg"]
            date = datetime.strptime(tx["timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%d/%Y %H:%M:%S")

            #add a new row per message in the TX (might need to change if messages don't correspond directly to all actions)
            for message in messages:
                url = f"{base_finder_url}{tx['chainId']}/tx/{tx['txhash']}"
                new_rows.append({"Date": date, "Transaction ID": tx['txhash'], "Finder URL": url})

        headers = ["Date", "Received Quantity", "Received Currency", "Sent Quantity", "Sent Currency" ,"Fee Amount", "Fee Currency", "Tag", "Transaction ID", "Finder URL"]

        write_csv_dict(output_file, headers, new_rows, restval="")

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
