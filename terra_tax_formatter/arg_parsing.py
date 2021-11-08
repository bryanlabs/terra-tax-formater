import argparse
import os
import sys
from .files import get_file_realpath

def parse_args():

    """
    Parses a set of keyword arguments for use in the script

    --old-format str: The old format to parse from
    --new-format str: The new format to parse to
    --old str: The old filename to gather data from
    --new str: A new filename to output data to
    
    """
    arg_parser = argparse.ArgumentParser(description='Extend output from stake.tax, verify presence of all transactions for the address and output a file with the missing values', allow_abbrev=True)
    arg_parser.add_argument("--terra-address", type=str, help="The terra address to gather data for", required=True)
    arg_parser.add_argument("--new", type=str, help="The file to output to", required=True)
    arg_parser.add_argument("--old", type=str, help="The stake.tax downloaded CSV file, if provided will use the file specified from the system instead of reaching out to stake.tax", required=False)

    args = arg_parser.parse_args()

    terra_address = args.terra_address
    input_file = args.old
    output_file = args.new

    #mode for determining script run: download file from stake.tax or upload from system
    mode = "file_download"
    if input_file:
        mode = "file_input"

    if mode == "file_download":
        uin = input(f"No input file specified, would you like to reach out to stake.tax directly? (Y/n) ")
        if(uin != "Y"):
            print("Cancelled")
            sys.exit(1)

    return {"terra_address": terra_address, "input_file": input_file, "output_file": output_file, "mode": mode}

def validate_args(args):
    """
    Validates the args passed in.
    """

    input_file = args["input_file"]
    output_file = args["output_file"]

    if input_file and not os.path.isfile(get_file_realpath(input_file)):
        print('Specified input "--old" file does not exist')
        sys.exit(1)

    if os.path.isfile(get_file_realpath(output_file)):
        uin = input(f"The specified output file {output_file} already exists, would you like to overwrite it? (Y/n) ")
        if(uin != "Y"):
            print("Cancelled")
            sys.exit(1)