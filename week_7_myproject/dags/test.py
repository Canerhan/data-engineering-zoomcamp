import pandas as pd
import io
import os
import requests

file_name = "test"

request_url =r"https://use-land-property-data.service.gov.uk/datasets/td/download/history/February%202023/Number-and-types-of-applications-by-all-account-customers-2023-02.csv"
r = requests.get(request_url)
pd.DataFrame(io.StringIO(r.text)).to_csv(file_name)
print(f"Local: {file_name}")

# read it back into a parquet file
df = pd.read_csv(file_name)
file_name = file_name.replace('.csv', '.parquet')
df.to_parquet(file_name, engine='pyarrow')
print(f"Parquet: {file_name}")
