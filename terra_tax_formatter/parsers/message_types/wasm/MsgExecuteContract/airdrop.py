
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

def parse(msg, log):
    pass
