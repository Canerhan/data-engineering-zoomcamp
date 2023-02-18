"""
2.4: From Google Cloud Storage to Big Query
Flow : From GCS to BigQuery

"""

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block=GcsBucket.load("gcs-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./")
    return Path(f"./{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Creating a Dataframe"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame, color: str, year: int, month: int) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("gcp-block")
    df.to_gbq(
        destination_table=f"trips_data_all.{color}_tripdata_{year}-{month:02}", # Dataset.TableName
        project_id="dtc-de-course-2023",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500.000,
        if_exists="replace",
    )

@flow()
def etl_gcs_to_bq(year: int, month: int, color: str) -> None:
    """Main ETL flow to load data into Big Query"""


    path = extract_from_gcs(color, year, month) 
    df = transform(path)
    write_bq(df, color, year, month)
    print(len(df))


@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], year: int = 2019, color: str = "yellow"
):
    for month in months:
        etl_gcs_to_bq(year, month, color)

if __name__=="__main__":
    
    color="yellow"
    year=2019
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    
    etl_parent_flow(months, year, color)