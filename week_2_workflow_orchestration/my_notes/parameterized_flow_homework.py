"""
2.5: Parametrizing Flow & Deployments
- Parametrizing the script from your flow
- Parameter validation with Pydantic
- Creating a deployment locally
- Setting up Prefect Agent
- Running the flow
- Notifications
"""

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta 

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:  # Input is the dataset_url variable, who is a string. We are returning a Pandas Dataframe
    """Read taxi data from web into pandas DataFrame"""  

    ## Test retries 
    # if randint(0,1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(df.head(2))
    print(F"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"/home/linux_dev_env/data-engineering-zoomcamp/week_2_workflow_orchestration/data/{color}/{dataset_file}.parquet")
    gcp_path = Path(f"./data/{color}/{dataset_file}")
    df.to_parquet(path, compression="gzip")
    return path, gcp_path


@task()
def write_gcs(path: Path, gcp_path: Path) -> None:
    """Upload local parquet FIle """
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path = f"{path}",
        to_path=f"{gcp_path}"
    )
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The Main ETL function """
    # color="yellow"
    # year=2021
    # month=1

    # url of the datasets github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow

    dataset_file =f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path, gcp_path = write_local(df_clean, color, dataset_file)
    write_gcs(path, gcp_path)

@flow()
def etl_parent_flow(
    months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"
):
    for month in months:
        etl_web_to_gcs(year, month, color)

if __name__ == '__main__':
    color="yellow"
    year=2019
    months=[2,3]
    etl_parent_flow(months, year, color) 