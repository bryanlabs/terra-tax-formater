import argparse

def parse_args():

    """
    Parses a set of keyword arguments for use in the script

    --old-format str: The old format to parse from
    --new-format str: The new format to parse to
    --old str: The old filename to gather data from
    --new str: A new filename to output data to
    
    """
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