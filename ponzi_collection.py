# data_collection.py

import pandas as pd
from etherscan import Etherscan
import time
import random
from tqdm import tqdm

def collect_data(ponzi_addresses, key):
    eth = Etherscan(key)
    internal = pd.DataFrame()
    external = pd.DataFrame()

    for i in tqdm(range(len(ponzi_addresses))):
        address = ponzi_addresses[i]

        # Gathering internal transactions
        try:
            internal_txs = eth.get_internal_txs_by_address(address, startblock=0, endblock=99999999, sort='asc')
            internal_current = pd.DataFrame(internal_txs)
            internal_current['ponzi_name'] = address
            internal = pd.concat([internal, internal_current], axis=0)
        except Exception as e:
            print(f"Error fetching internal transactions for {address}: {e}")

        time.sleep(1 + random.random())

        # Gathering external transactions
        try:
            external_txs = eth.get_normal_txs_by_address(address, startblock=0, endblock=99999999, sort='asc')
            external_current = pd.DataFrame(external_txs)
            external_current['ponzi_name'] = address
            external = pd.concat([external, external_current], axis=0)
        except Exception as e:
            print(f"Error fetching external transactions for {address}: {e}")

        time.sleep(1 + random.random())

    return internal, external

def main():
    # Load Ponzi addresses
    ponzi_data = pd.read_csv("Ponzi_label.csv")
    ponzi_addresses = ponzi_data[ponzi_data['Ponzi'] == '1']['Contract'].tolist()

    key = "WZW9TFNTB2SUK963BDGM9XT87CIVFM1GEF"  # Your Etherscan API key
    internal, external = collect_data(ponzi_addresses, key)

    # Save the collected data
    internal.to_csv('ponzi_internal_transactions.csv', index=False)
    external.to_csv('ponzi_external_transactions.csv', index=False)

if __name__ == "__main__":
    main()
