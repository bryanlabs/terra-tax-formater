import re
from ....terra_fcd import get_ibc_denom_trace

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
    delegator_address = msg["value"]["delegator_address"]
    coins_received_string = ""
    for event in log["events"]:
        #try the coin_recieved log first
        if event["type"] == "coin_received":
            receiver = None
            amount = None
            for attribute in event["attributes"]:
                if attribute["key"] == "receiver":
                    receiver = attribute["value"]
                elif attribute["key"] == "amount":
                    amount = attribute["value"]
            if receiver == delegator_address:
                coins_received_string = amount
                break

        #try the transfer log second
        if event["type"] == "transfer":
            receiver = None
            amount = None
            for attribute in event["attributes"]:
                if attribute["key"] == "recipient":
                    receiver = attribute["value"]
                elif attribute["key"] == "amount":
                    amount = attribute["value"]
            if receiver == delegator_address:
                coins_received_string = amount
                break

    
    if not coins_received_string:
        raise ValueError("Could not determine coins received")

    coins_received = coins_received_string.split(",")
    coins_parsed = []
    for coin in coins_received:
        if "ibc/" in coin:
            amount, hash = coin.split("ibc/")
            #10 decimal precision enough?
            amount = f"{int(amount)/1000000:.10f}"
            denom_trace = None
            try:
                denom_trace = data_cache["ibc_denom_traces"][hash]
            except:
                denom_trace = get_ibc_denom_trace(hash)
                data_cache["ibc_denom_traces"][hash] = denom_trace
            
            utoken = denom_trace["denom_trace"]["base_denom"]

            #this is how Terra Station currently does it, valid?
            #see https://github.com/terra-money/station/blob/main/src/utils/format.ts#L38
            symbol = utoken.replace("u", "").upper()
            coins_parsed.append((amount, symbol))
        else:
            regex = re.compile("(\d+)(\w+)")
            match = regex.match(coin)
            amount, utoken = match.group(1), match.group(2)
            #10 decimal precision enough?
            amount = f"{int(amount)/1000000:.10f}"
            #see above comment
            symbol = utoken.replace("u", "").upper()
            coins_parsed.append((amount, symbol))

    txs = []
    for coin in coins_parsed:
        txs.append({"Received Quantity": coin[0], "Received Currency": coin[1]})
    
    return txs
            


    
    