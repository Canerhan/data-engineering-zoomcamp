## Week 2 Homework

The goal of this homework is to familiarise users with workflow orchestration and observation. 


## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

* 447,770
* 766,792
* 299,234
* 822,132


### Solution Question 1

We take the etl_web_to_gcs Python file, and edit the 3 parameters:   
~~~py
color="green"
year=2020
month=1
~~~

We also have to rename thee columns from the clean function,   
the date columns name are "lpep...."

~~~py
df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
~~~

After that editing, we can execute the python file.
The file is in [week_2_workflow_orchestration/my_notes/etl_web_to_gcs_green_taxi.py](data-engineering-zoomcamp/week_2_workflow_orchestration/my_notes/etl_web_to_gcs_green_taxi.py)

The dataset has **447.770 rows**.  

---

## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows. 

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

- `0 5 1 * *`
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`

### Solution Question 2

The first parmeter is the minute (=0), the second the hour (=5),  
and the third is the day of the month (=1).

So the result is `0 5 1 * *`


[crontab](https://crontab.guru/) is a good source.  

---

## Question 3. Loading data to BigQuery 

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color. 

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- 14,851,920
- 12,282,990
- 27,235,753
- 11,338,483


### Solution Question 3

The parameterized Python file is [here](data-engineering-zoomcamp/week_2_workflow_orchestration/my_notes/parameterized_flow_web_to_gcs_homework.py)

The "etl_web_to_gcs" function is part of the parent flow.  
With this part of the funtion it can take multiple parameters:  

~~~python
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
~~~

To create a deployment, we execute:

~~~shell
prefect deployment build ./parameterized_flow_web_to_gcs_homework.py:etl_parent_main_flow -n "Parameterized EL_gcs_to_bq"
~~~

The name of the python file is `parameterized_flow_web_to_gcs_homework_question3.py`,   
the name of the parent flow is `etl_parent_main_flow`,  
and the name of the deployment will be 

The result of the execution is:  
~~~bash
prefect deployment build ./parameterized_flow_web_to_gcs_homework_question3.py:etl_parent_main_flow -n "Parameterized EL_gcs_to_bq"
Found flow 'etl-parent-main-flow'
Deployment YAML created at 
'/home/linux_dev_env/data-engineering-zoomcamp/week_2_workflow_orchestration/my_notes/etl_parent_main_f
low-deployment.yaml'.
Deployment storage None does not have upload capabilities; no files uploaded.  Pass --skip-upload to 
suppress this warning.
~~~

Now we can edit the `prefect deployment apply etl_parent_main_flow-deployment.yaml` Yaml file.  
We replace `parameters: {}` with `parameters: { "color": "yellow", "months" :[2, 3], "year": 2019}`
Now we can apply the new deployment with `prefect deployment apply etl_parent_main_flow-deployment.yaml`

For a deployment to be execcutabel,   
we havbe to start the prefect agent within a termminal:  
`prefect agent start -q 'default'`

The yellow_tripdata_2019-02 table has 7.019.375 rows,  
yellow_tripdata_2019-03 has 7.832.545 rows.
So **14,851,920** is the correct answer.
---

## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image. 

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- 88,019
- 192,297
- 88,605
- 190,225



## Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur. 

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up. 

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook. 

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days. 

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create. 


How many rows were processed by the script?

- `125,268`
- `377,922`
- `728,390`
- `514,392`


## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- 5
- 6
- 8
- 10


## Submitting the solutions

* Form for submitting: https://forms.gle/PY8mBEGXJ1RvmTM97
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 6 February (Monday), 22:00 CET


## Solution

We will publish the solution here