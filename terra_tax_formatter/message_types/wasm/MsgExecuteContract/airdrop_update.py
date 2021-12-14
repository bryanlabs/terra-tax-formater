BASE_AIRDROP_UPDATE_MSG_VALUE = {
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
                "airdrop": {
                    "type": dict,
                    "keys": {
                        "update": {
                            "type": dict,
                            "keys": {
                                "target": {
                                    "type": str
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}