from terra_sdk.client.lcd import LCDClient

terra_lcd_client = LCDClient("https://lcd.terra.dev", "columbus-5")

def get_tx_info_by_txhash(tx_hash):
    return terra_lcd_client.tx.tx_info(tx_hash)
