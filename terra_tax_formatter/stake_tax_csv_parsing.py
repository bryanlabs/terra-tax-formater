
def get_unique_tx_hashes(stake_tax_csv_list):
    return list(set([tx["Transaction ID"] for tx in stake_tax_csv_list]))