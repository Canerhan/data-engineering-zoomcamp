import json

from airflow import DAG
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator


# Libraries
import json
import os
from datetime import datetime, timedelta
import pendulum

# Airflow
from airflow.models import DAG, Variable
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.decorators import task

# Default Airflow operators 
# https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

# Contributed Airflow operators (providers) 
# https://airflow.apache.org/docs/apache-airflow-providers/operators-and-hooks-ref/index.html

#from airflow.providers.amazon.aws.transfers.gcs_to_s3 import GCSToS3Operator
#from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

############################################################
# DAG settings
############################################################

LOCAL_TZ = pendulum.timezone("Europe/Amsterdam")

DAG_NAME = "stacktonic_example_dag" # DAG name (proposed format: lowercase underscore). Should be unique.
DAG_DESCRIPTION = "Example DAG by Krisjan Oldekamp / stacktonic.com"
DAG_START_DATE = datetime(2021, 10, 15, tzinfo=LOCAL_TZ) # Startdate. When setting the "catchup" parameter to True, you can perform a backfill when you insert a specific date here like datetime(2021, 6, 20)
DAG_SCHEDULE_INTERVAL = "@daily" # Cron notation -> see https://airflow.apache.org/scheduler.html#dag-runs
DAG_CATCHUP = False # When set to true, DAG will start running from DAG_START_DATE instead of current date
DAG_PAUSED_UPON_CREATION = True # Defaults to False. When set to True, uploading a DAG for the first time, the DAG doesn't start directly 
DAG_MAX_ACTIVE_RUNS = 5 # Configure efficiency: Max. number of active runs for this DAG. Scheduler will not create new active DAG runs once this limit is hit. 

############################################################
# Default DAG arguments
############################################################

default_args = {
    "owner": "airflow",
    "start_date": DAG_START_DATE,
    "depends_on_past": False,
    "email": Variable.get("email_monitoring", default_var="<FALLBACK-EMAIL>"), # Make sure you create the "email_monitoring" variable in the Airflow interface
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2, # Max. number of retries before failing
    "retry_delay": timedelta(minutes=60) # Retry delay
}

############################################################
# DAG configuration (custom)
############################################################

with DAG(
    DAG_NAME,
    description=DAG_DESCRIPTION,
    schedule_interval=DAG_SCHEDULE_INTERVAL,
    catchup=DAG_CATCHUP,
    max_active_runs=DAG_MAX_ACTIVE_RUNS,
    is_paused_upon_creation=DAG_PAUSED_UPON_CREATION,
    default_args=default_args) as dag:


mv_local_gcs = LocalFilesystemToGCSOperator(
       task_id="local_to_gcs",
       src=comp_local_path+"/yourfilename.csv",# PATH_TO_UPLOAD_FILE
       dst="somefolder/yournewfilename.csv",# BUCKET_FILE_LOCATION
       bucket="yourproject",#using NO 'gs://' nor '/' at the end, only the project, folders, if any, in dst
       gcp_conn_id = "gcp_connection"
       dag=dag
   )

start = DummyOperator(task_id='Starting', dag=dag)

start >> mv_local_gcs
