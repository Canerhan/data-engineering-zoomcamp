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


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"./data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet FIle """
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path = f"{path}",
        to_path=f"{path}"
    )
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The Main EL function """

    dataset_file =f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    path = write_local(df, color, dataset_file)
    write_gcs(path)
    print(f"rows fetch: {len(df)}")

@flow()
def etl_parent_main_flow(
    months: list[int] = [1, 2], year: int = 2019, color: str = "yellow"
):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2019
    etl_parent_main_flow(months, year, color)