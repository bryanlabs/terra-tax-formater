import requests
from .exceptions import ConverterCaughtError
import sys
from time import sleep
import codecs
import csv

API_URL = "https://prodapi.stake.tax"
CSV_URL = "https://prodcsv.stake.tax/csv/<job_id><format>"
TX_ENDPOINT = "/txs"

def start_csv_process(address_id):
    try:
        post_response = requests.post(API_URL + TX_ENDPOINT, json={"ticker":"LUNA", "wallet_address": address_id, "options":{"optionreward":True}})
        post_response.raise_for_status()
        resp = post_response.json()

        if "success" in resp.keys() and resp["success"]:
            return resp
        else:
            raise ConverterCaughtError(f"stake.tax was unable to process the address ID {address_id}")
    except ConverterCaughtError as err:
        raise err
    except Exception as err:
        print("There was an error gathering data from stake.tax, please try again later")
        sys.exit(1)

def track_job(job_id):
    try:
        while True:
            get_response = requests.get(f"{API_URL}{TX_ENDPOINT}/{job_id}")
            get_response.raise_for_status()
            resp = get_response.json()

            if resp["progress"]["is_done"]:
                return
            else:
                sleep(5)
    except Exception as err:
        print(f"Error while tracking stake.tax job id {job_id}")
        sys.exit(1)

def download_csv(job_id, format):
    try:
        download_resp = requests.get(CSV_URL.replace("<job_id>", job_id).replace("<format>", format.stake_tax_endpoint), stream=True)
        download_resp.raise_for_status()
        return download_resp
    except Exception as err:
        print(f"Error while downloading stake.tax output file for job id {job_id}")
        sys.exit(1)

def parse_csv_file_object(file_obj):
    #return list to allow multiple methods to iter
    #inefficient for large files memory-wise, but better for multi iteration
    return list(
            csv.DictReader(
                codecs.iterdecode(file_obj.iter_lines(), 'utf-8')
            )
        )