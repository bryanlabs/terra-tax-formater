import csv, codecs
from .base import BaseFormatter

class Cointracker(BaseFormatter):
    def __init__(self):
        super().__init__(
            headers=[
                "Date",
                "Received Quantity",
                "Received Currency",
                "Sent Quantity",
                "Sent Currency",
                "Fee Amount",
                "Fee Currency",
                "Tag",
                "Transaction ID"
            ],
            headers_to_data_keys = {
                "Date": "date",
                "Transaction ID": "txhash",
                "Received Quantity": "received quantity",
                "Received Currency": "received currency",
                "Tag": "type"
            }
        )

        self.missing_file_headers = [
            "Finder URL"
        ]

        self.stake_tax_endpoint = "/cointracker.csv"
        self.read_file_mode = "r"

    def parse_response_data(self, file_obj):
        return list(
            csv.DictReader(
                codecs.iterdecode(file_obj.iter_lines(), 'utf-8')
            )
        )

    def parse_file_data(self, file_obj):
        return list(
            csv.DictReader(file_obj)
        )

    def write_data(self, data, fname, headers=None):
        if not headers:
            headers = self.headers
        with open(fname, "w", newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, restval="")
            writer.writeheader()
            for line in data:
                writer.writerow(line)

    def get_unique_tx_hashes(self, stake_tax_csv_list):
        return list(set([tx["Transaction ID"] for tx in stake_tax_csv_list]))

    def format_date(self, date_obj):
        return date_obj.strftime("%m/%d/%Y %H:%M:%S")

