from .wasm.MsgExecuteContract import airdrop, airdrop_allocation, airdrop_update
from .distribution.MsgWithdrawDelegationReward import withdraw_delegation_reward

def parse_untaxable(*pargs, **kargs):
    #stub parser for untaxable txs
    return "non-taxable"

WASM = {
    "MsgExecuteContract": [
        {
            "type": "airdrop",
            "msg_identity": airdrop.BASE_AIRDROP_MSG_VALUE,
            "log_identity": None,
            "parser": airdrop.parse
        },
        {
            "type": None,
            "msg_identity": airdrop_allocation.BASE_AIRDROP_ALLOCATION_MSG_VALUE,
            "log_identity": None,
            "parser": parse_untaxable
        },
        {
            "type": None,
            "msg_identity": airdrop_update.BASE_AIRDROP_UPDATE_MSG_VALUE,
            "log_identity": None,
            "parser": parse_untaxable
        }
    ]
}

DISTRIBUTION = {
    "MsgWithdrawDelegationReward": [
        {
            "type": "reward",
            "msg_identity": withdraw_delegation_reward.BASE_WITHDRAW_MSG,
            "log_identity": None,
            "parser": withdraw_delegation_reward.parse
        }
    ]
}

__all__ = ["DISTRIBUTION", "WASM"]