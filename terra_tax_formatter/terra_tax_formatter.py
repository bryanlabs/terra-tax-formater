#!/usr/bin/env python3

import sys
from .files import *
from .arg_parsing import parse_args
from .exceptions import ConverterCaughtError

try:
    import requests
except ImportError:
    print("This script requires the Python requests package, please download it to your PYTHON_PATH and try again")
    sys.exit(1)


def get_mirror_symbol_response():
    try:
        req = requests.post("https://graph.mirror.finance/graphql", data={"query": "{ assets { symbol name } }"})
        req.raise_for_status()
        return req.json()
    except:
        raise ConverterCaughtError(message="There was an error receiving a response from the graph.mirror.finance site, please contact the developer")

def main():
    args = parse_args()
    try:
        pass
    except ConverterCaughtError as error:
        print(error.message)
        return 1
    except Exception as error:
        print(error)
        print("An unknown error occurred, please contact the developer for assistance")
        return 1

    return 0
