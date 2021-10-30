import requests
from .exceptions import ConverterCaughtError

def get_mirror_symbol_response():
    try:
        req = requests.post("https://graph.mirror.finance/graphql", data={"query": "{ assets { symbol name } }"})
        req.raise_for_status()
        return req.json()
    except:
        raise ConverterCaughtError(message="There was an error receiving a response from the graph.mirror.finance site, please contact the developer")
