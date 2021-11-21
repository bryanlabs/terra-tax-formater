from .MsgExecuteContract import airdrop

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
