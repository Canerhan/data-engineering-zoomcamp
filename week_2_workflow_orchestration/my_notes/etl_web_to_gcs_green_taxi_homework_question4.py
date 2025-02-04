"""
2.3: ETL with GCP & Prefect
Flow : Putting data to Google Cloud Storage

"""
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.filesystems import GitHub
# from prefect.storage import GitHub

@task(retries=3)
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
    df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
    df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
    print(df.head(2))
    print(F"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

# @task()
# def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
#     """Write DataFrame out locally as parquet file"""
#     path = Path(f"./data/{color}/{dataset_file}.parquet")
#     df.to_parquet(path, compression="gzip")
#     return path


@task()
def write_gcs(path: Path, path_gcp) -> None:
    """Upload local parquet FIle """
    gcp_cloud_storage_bucket_block = GcsBucket.load("gcs-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path = f"{path}",
        to_path=f"{path_gcp}"
    )
    return


@flow()
def etl_web_to_gcs() -> None:
    """The Main ETL function """
    color="green"
    year=2019
    month=4

    # url of the datasets github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow

    dataset_file =f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    # path = write_local(df_clean, color, dataset_file)
    write_gcs(dataset_url,dataset_file)

    flow.storage = GitHub(
        repo="https://github.com/Canerhan/data-engineering-zoomcamp",                            # name of repo
        path="week_2_workflow_orchestration/my_notes/etl_web_to_gcs_green_taxi_homework_question4.py",                    # location of flow file in repo
        access_token_secret="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"   # name of personal access token secret
    )
if __name__ == '__main__':
    etl_web_to_gcs()