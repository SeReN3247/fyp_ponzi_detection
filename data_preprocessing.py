# data_preprocessing.py

import pandas as pd

def preprocess_data():
    external = pd.read_csv("ponzi_external_transactions.csv")
    internal = pd.read_csv("ponzi_internal_transactions.csv")

    # Transforming values to integers
    external['value'] = external['value'].astype(float) / 10**18
    internal['value'] = internal['value'].astype(float) / 10**18
    external['transaction_cost'] = external['gasPrice'] * external['gasUsed'] / 10**18  # transaction fee in ETH

    # Convert timestamps to datetime
    external['Date'] = pd.to_datetime(external['timeStamp'], unit='s')
    internal['Date'] = pd.to_datetime(internal['timeStamp'], unit='s')

    # Save cleaned data
    external.to_csv('cleaned_external_transactions.csv', index=False)
    internal.to_csv('cleaned_internal_transactions.csv', index=False)

if __name__ == "__main__":
    preprocess_data()
