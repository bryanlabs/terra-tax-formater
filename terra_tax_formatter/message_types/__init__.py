from .wasm.MsgExecuteContract import airdrop
from .distribution.MsgWithdrawDelegationReward import withdraw_delegation_reward

WASM = {
    "MsgExecuteContract": [
        {
            "type": "airdrop",
            "msg_identity": airdrop.BASE_AIRDROP_MSG_VALUE,
            "log_identity": None,
            "parser": airdrop.parse
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