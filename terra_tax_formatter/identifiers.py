from .message_types import WASM
from .message_types import DISTRIBUTION

identifiers = {
    "wasm": WASM,
    "distribution": DISTRIBUTION
}


def identify(msg, log):
    """
    Determines the base and message type of the message,
    finds the identity of the message from its structure.
    
    Searches the msg and log of the message (if required) to determine the type.

    Returns a list of possible identities for the message, includes a parser function
    to attempt to parse the message.
    """
    base_type, message_type = msg["type"].split("/")

    identifier_class = None
    try:
        identifier_class = identifiers[base_type][message_type]
    except KeyError:
        return None

    possible_identities = []
    for identifier in identifier_class:
        msg_identified = identify_message_type(msg, log, identifier["msg_identity"], identifier["log_identity"])
        if msg_identified:
            possible_identities.append(identifier)
    
    return possible_identities

def identify_message_type(msg, log, msg_identifier, log_identifier):
    """
    Determines the message type based on a possible message identifier
    and optional log identifier (WIP)
    """

    msg_type = msg["type"]
    msg_value = msg["value"]

    if msg_type != msg_identifier["type"]:
        return False

    for key in msg_value.keys():
        value_validator = None
        try:
            #if the validator does not contain the key in the msg, not identified
            value_validator = msg_identifier["value"][key]
        except KeyError:
            return False

        if not value_validate(msg_value[key], value_validator):
            return False

    return True

def value_validate(value, value_validator):
    """
    Takes in a value and a key parser to determine if it matches
    the format specified in the key parser for that item
    """
    if not isinstance(value, value_validator["type"]):
        return False

    #recursive dict validation
    if isinstance(value, dict):
        for key in value_validator["keys"].keys():
            if key not in value.keys():
                return False
            valid = value_validate(value[key], value_validator["keys"][key])
            if not valid:
                return False

    return True
