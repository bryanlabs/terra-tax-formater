from .MsgWithdrawDelegationReward import withdraw_delegation_reward

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
