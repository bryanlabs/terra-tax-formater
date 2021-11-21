BASE_WITHDRAW_MSG = {
    "type": "distribution/MsgWithdrawDelegationReward",
    "value": {
        "delegator_address": {
            "type": str
        },
        "validator_address": {
            "type": str
        }
    }
}

def parse(msg, log, data_cache):
    pass