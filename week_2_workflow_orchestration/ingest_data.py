#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time
from datetime import timedelta
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector



@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data (url: str):


    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")


    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df


@task(log_prints=True)
def transform_data(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

# we are using the connection block from prefect ui
# the connection is based on sqlalchemy
@task(log_prints=True, retries=3)
def main(table_name, url,  data):

    connection_block = SqlAlchemyConnector.load("postgres-block")
    with connection_block.get_connection(begin=False) as engine:
        data.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        data.to_sql(name=table_name, con=engine, if_exists='append')


@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"logging Subflow for: {table_name}")


@flow(name="Ingest Flow")
def main_flow():

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    table_name = args.table_name
    url = args.url

    log_subflow(table_name)
    raw_data = extract_data(url)
    data = transform_data(raw_data)
    main(table_name, url,  data)


if __name__ == '__main__':
    main_flow()


