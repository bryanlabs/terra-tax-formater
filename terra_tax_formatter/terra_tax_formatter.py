#!/usr/bin/env python3

import csv
import argparse
import os
import sys
try:
    import requests
except ImportError:
    print("This script requires the Python requests package, please download it to your PYTHON_PATH and try again")
    sys.exit(1)


class ConverterCaughtError(Exception):
    def __init__(self, message):
        self.message = message

def get_mirror_symbol_response():
    try:
        req = requests.post("https://graph.mirror.finance/graphql", data={"query": "{ assets { symbol name } }"})
        req.raise_for_status()
        return req.json()
    except:
        raise ConverterCaughtError(message="There was an error receiving a response from the graph.mirror.finance site, please contact the developer")

#parses the keyword arguments from the CLI
#handles complex parsing, no need to rely on catching errors due to bad input formats later
def parse_args():
    arg_parser = argparse.ArgumentParser(description='Convert various CSV file formats to different formats', allow_abbrev=True)
    arg_parser.add_argument("--old-format", type=str, help="The old format to convert from", required=True, choices=["track-terra"])
    arg_parser.add_argument("--new-format", type=str, help="The new format to convert to", required=True, choices=["accointing"])
    arg_parser.add_argument("--old", type=str, help="The file to convert from", required=True)
    arg_parser.add_argument("--new", type=str, help="The file to output to", required=True)

    args = arg_parser.parse_args()

    input_file = args.old
    output_file = args.new
    old_format = args.old_format
    new_format = args.new_format

    return {"old_format": old_format, "new_format": new_format,"input_file": input_file, "output_file": output_file}

def open_file(fname):
    return open(os.path.realpath(os.path.join(os.getcwd(), fname)), "r")

def write_csv(fname, data_rows):
    with open(os.path.realpath(os.path.join(os.getcwd(), fname)), "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator="\n")
        for line in data_rows:
            writer.writerow(line)


def parse_track_terra_to_accointing(fname):
    #get the mirror assets and pull all the symbols out of the response into a single list
    mirror_symbol_response = get_mirror_symbol_response()
    mirror_symbol_names = list(map(lambda symbol: symbol["symbol"], mirror_symbol_response["data"]["assets"]))

    #these keys of this object point to columns in track-terra
    #the values point to the output for accointing
    column_conversions = {
        "Date": "date",
        "Sent Amount": "outSellAmount",
        "Sent Currency": "outSellAsset",
        "Received Amount": "inBuyAmount",
        "Received Currency": "inBuyAsset",
        "Fee Amount": "feeAmount (optional)",
        "Fee Currency": "feeAsset (optional)",
        "TxHash": "operationId (optional)"
    }

    #this is the ordering the columns should be parsed into
    new_column_ordering = ["transactionType", "date", "outSellAmount", "outSellAsset", "inBuyAmount", "inBuyAsset", "feeAmount (optional)", "feeAsset (optional)", "operationId (optional)", "classification (optional)"]
    new_rows = [new_column_ordering]

    with open_file(fname) as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            new_row_list = []

            #ignore the rows that dont have the proper Tx Type
            if row["Tx Type"] not in ["nativeSendReceive", "additionalFee", "tsSwap"]:
                continue
            else:
                new_row = {}
                transaction_type = ""
                #parse the transaction type out on the rules
                if row["Received Amount"] and not row["Sent Currency"] and not row["Sent Token Address"]:
                    transaction_type = "deposit"
                elif row["Sent Currency"] and not row["Received Amount"]:
                    transaction_type = "withdraw"
                elif row["Sent Currency"] and row["Received Amount"]:
                    transaction_type = "order"
                
                new_row["transactionType"] = transaction_type

                #use the column conversions to pull the data out and transfer it
                for key in column_conversions.keys():
                    if key in row.keys():
                        new_row[column_conversions[key]] = row[key]
                    else:
                        new_row[column_conversions[key]] = ""
                
                #convert the mirror symbols if found
                if new_row["inBuyAsset"].startswith("m") and new_row["inBuyAsset"] in mirror_symbol_names:
                    #split the m off the front of a mirrored symbol
                    new_row["inBuyAsset"] = new_row["inBuyAsset"][1:]

                if new_row["outSellAsset"].startswith("m") and new_row["outSellAsset"] in mirror_symbol_names:
                    #split the m off the front of a mirrored symbol
                    new_row["outSellAsset"] = new_row["outSellAsset"][1:]

                #parse out the new row's dictionary columns into an ordered list
                for col in new_column_ordering:
                    if col in new_row.keys():
                        new_row_list.append(new_row[col])
                    else:
                        new_row_list.append("")

            new_rows.append(new_row_list)
            
    return new_rows 

def parse_data(fname, formatFrom, formatTo):
    parser = parsers[formatFrom][formatTo]

    try:
        return parser(fname)
    except FileNotFoundError:
        raise ConverterCaughtError(message=f"The specified input file \"{fname}\" was not found")

#parser function mapping for parsing specific formats
parsers = {
    "track-terra": {
        "accointing": parse_track_terra_to_accointing
    }
}

def main():

    args = parse_args()
    try:
        parsed_data = parse_data(args["input_file"], args["old_format"], args["new_format"])
        write_csv(args["output_file"], parsed_data)

    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
