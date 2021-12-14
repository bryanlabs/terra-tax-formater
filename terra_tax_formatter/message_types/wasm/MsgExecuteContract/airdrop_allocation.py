BASE_AIRDROP_ALLOCATION_MSG_VALUE = {
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
                        "allocate": {
                            "type": dict,
                            "keys": {
                                "recipient": {
                                    "type": str
                                },
                                "airdrop_id": {
                                    "type": int
                                },
                                "allocate_amount": {
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