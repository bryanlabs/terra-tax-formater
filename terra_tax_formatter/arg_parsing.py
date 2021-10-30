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
    arg_parser = argparse.ArgumentParser(description='Convert various CSV file formats to different formats', allow_abbrev=True)
    arg_parser.add_argument("--terra-address", type=str, help="The terra address to gather data for", required=True)
    arg_parser.add_argument("--old", type=str, help="The file to convert from", required=True)
    arg_parser.add_argument("--new", type=str, help="The file to output to", required=True)

    args = arg_parser.parse_args()

    terra_address = args.terra_address
    input_file = args.old
    output_file = args.new

    return {"terra_address": terra_address, "input_file": input_file, "output_file": output_file}

def validate_args(args):
    """
    Validates the args passed in.
    """

    input_file = args["input_file"]
    output_file = args["output_file"]
    errors = []

    if not os.path.isfile(get_file_realpath(input_file)):
        print('Specified input "--old" file does not exist')
        sys.exit(1)

    if os.path.isfile(get_file_realpath(output_file)):
        uin = input(f"The specified output file {output_file} already exists, would you like to overwrite it? (Y/n) ")
        if(uin != "Y"):
            print("Cancelled")
            sys.exit(1)