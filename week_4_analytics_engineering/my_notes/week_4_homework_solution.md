## Week 4 Homework 

In this homework, we'll use the models developed during the week 4 videos and enhance the already presented dbt project using the already loaded Taxi data for fhv vehicles for year 2019 in our DWH.

We will use the data loaded for:

* Building a source table: `stg_fhv_tripdata`
* Building a fact table: `fact_fhv_trips`
* Create a dashboard 

If you don't have access to GCP, you can do this locally using the ingested data from your Postgres database
instead. If you have access to GCP, you don't need to do it for local Postgres -
only if you want to.

### Question 1: 

**What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)** 

You'll need to have completed the "Build the first dbt models" video and have been able to run the models via the CLI. 
You should find the views and models for querying in your DWH.

- 61635151
- 61635418
- 61666551
- 41856543


#### Question 1 Solution 

In the staging Models is a Macro:


~~~jionja
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
~~~

so we have to run dbt with this command:  
`dbt run --var 'is_test_run: false'`


~~~sql
SELECT 
COUNT(*)
FROM `dtc-de-course-2023`.trips_data_all.fact_trips;
~~~

What is the count of records **61.580.709**



### Question 2: 

**What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos**

You will need to complete "Visualising the data" videos, either using data studio or metabase. 

- 89.9/10.1
- 94/6
- 76.3/23.7
- 99.1/0.9



#### Question 2 Solution 

~~~sql
SELECT 
COUNT(*) AS all_rows,
COUNT (CASE WHEN service_type = 'Green' THEN 1 END) / COUNT(*) AS green_perc,
COUNT (CASE WHEN service_type = 'Yellow' THEN 1 END) / COUNT(*) AS yellow_perc,
FROM `dtc-de-course-2023`.trips_data_all.fact_trips;
~~~

all_rows 61.580.709  
green_perc 0,1  
yellow_perc 0,9


**89.9/10.1**
![viz](2023-02-18-19-30-03.png)

### Question 3: 

**What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)**  

Create a staging model for the fhv data for 2019 and do not add a deduplication step. Run it via the CLI without limits (is_test_run: false).
Filter records with pickup time in year 2019.

- 33.244.696
- 43.244.696
- 53.244.696
- 63.244.696

#### Question 3 Solution
We create the staging model for fhv and with test disabled,  
with this comman:  
`  dbt run --m +stg_fhv_tripdata --var 'is_test_run: false'  `

~~~sql
SELECT 
*
FROM `dtc-de-course-2023`.trips_data_all.stg_fhv_tripdata
WHERE EXTRACT(YEAR FROM pickup_datetime ) = 2019
~~~

**- 43.244.696**

### Question 4: 

**What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)**  

Create a core model for the stg_fhv_tripdata joining with dim_zones.
Similar to what we've done in fact_trips, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. 
Run it via the CLI without limits (is_test_run: false) and filter records with pickup time in year 2019.

- 12.998.722
- 22.998.722
- 32.998.722
- 42.998.722


#### Question 4 Solution

[Here](data-engineering-zoomcamp/week_4_analytics_engineering/taxi_rides_ny/models/core/fact_fhv_trips.sql) is the model

`  dbt run --m fact_fhv_trips --var 'is_test_run: false'  `

~~~sql
SELECT 
COUNT(*)
FROM `dtc-de-course-2023`.trips_data_all.fact_fhv_trips
WHERE EXTRACT(YEAR FROM pickup_datetime) = 2019
~~~

**- 22.998.722**


### Question 5: 

**What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table**
Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, based on the fact_fhv_trips table.

- March
- April
- January
- December


#### Question 5 Solution

~~~sql
SELECT DISTINCT 
EXTRACT(MONTH FROM pickup_datetime) AS month_number,
COUNT(*) OVER (PARTITION BY EXTRACT(MONTH FROM pickup_datetime)) AS row_numbers
FROM `dtc-de-course-2023`.trips_data_all.fact_fhv_trips
WHERE EXTRACT(YEAR FROM pickup_datetime) = 2019
ORDER BY month_number ASC
~~~


![viz_q5](2023-02-19-11-42-57.png)

## Submitting the solutions

* Form for submitting: https://forms.gle/6A94GPutZJTuT5Y16
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 25 February (Saturday), 22:00 CET


## Solution

We will publish the solution here
