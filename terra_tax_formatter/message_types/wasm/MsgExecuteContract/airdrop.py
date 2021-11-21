from ....terra_fcd import get_contract_info

BASE_AIRDROP_MSG_VALUE = {
    "type": "wasm/MsgExecuteContract",
    "value": {
        "coins": {
            "type": list
        },
        "sender": {
            "type": str
        },
        "contract": {
            "type": str
        },
        "execute_msg": {
            "type": dict,
            "keys": {
                "claim": {
                    "type": dict,
                    "keys": {
                        "proof": {
                            "type": list
                        },
                        "stage": {
                            "type": int
                        },
                        "amount": {
                            "type": str
                        }
                    }
                }
            }
        }
    }
}

def parse(msg, log, data_cache):
    contract = msg["value"]["contract"]
    amount = int(msg["value"]["execute_msg"]["claim"]["amount"]) / 1000000

    #get the airdrop contract
    contract_info = None
    try:
        contract_info = data_cache["contracts"][contract]
    except:
        contract_info = get_contract_info(contract)
        data_cache["contracts"][contract] = contract_info

    #get the airdrop token symbol from the token address stored
    #in the airdrop contract info
    token_contract = get_contract_token_address(contract_info)
    token_info = None
    try:
        token_info = data_cache["contracts"][token_contract]
    except:
        token_info = get_contract_info(token_contract)
        data_cache["contracts"][token_contract] = token_info

    symbol = token_info["contract_info"]["symbol"]

    return {"Received Quantity": amount, "Received Currency": symbol, "Tag": "airdrop"}


def get_contract_token_address(contract_info):
    #token address seems to be stored in "*_token" key in init_msg
    init_msg = contract_info["contract_info"]["init_msg"]
    for key in init_msg.keys():
        if key.endswith("_token"):
            return init_msg[key]
