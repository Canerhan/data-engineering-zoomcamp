## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`
- `--idimage string`
- `--idfile string`

**--iidfile string          Write the image ID to the file**

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

### Solution  
After building the image,  
get the ID of the container,
and with that container ID start a interactive shell terminal:    

~~~docker
docker ps 
# the first column is the container ID
# c9b36c1e7921 is the ID
docker exec -it c9b36c1e7921 sh

# now we are inside the container with a shell terminal,  
# anw well execute

pip list package
~~~
The result is 6.

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

In Postgres you can change the type of a column with **'::' **  
and then the datatype you want to convert to.  


~~~sql
SELECT 
COUNT (*)
FROM public.green_taxi_data
WHERE lpep_pickup_datetime::date = '2019-01-15'
	AND lpep_dropoff_datetime ::date = '2019-01-15'
~~~

**Result:   20530**

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

We order the dataset after the 'trip_distance' column, but descending  
and Limit to only 1 row, so we only get the highest trip distance row.  

~~~sql
SELECT 
lpep_pickup_datetime
FROM public.green_taxi_data
ORDER BY trip_distance DESC 
LIMIT 1
~~~

**2019-01-15**

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

~~~sql
SELECT 
COUNT(CASE WHEN passenger_count = 2 THEN 1 END) as "2_passengers",
COUNT(CASE WHEN passenger_count = 3 THEN 1 END) as "3_passengers"
FROM public.green_taxi_data
WHERE lpep_pickup_datetime::date = '2019-01-01'
~~~

**2: 1282 ; 3: 254**

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

First we get the Dropoff Location ID from teh largest trip,  
where the Pickup Location Zone was "Astoria".  
Then we lookup for the name of the Zone with the DropoffLocation ID

~~~sql
WITH largest_tip AS (
SELECT 
gta."DOLocationID"
FROM public.green_taxi_data gta
LEFT JOIN public.taxi_zone_lookup tzl 
ON gta."PULocationID" = tzl."LocationID" 
WHERE "PULocationID" = 7
ORDER BY tip_amount DESC 
LIMIT 1
)
SELECT
"DOLocationID",
tzl."Zone" 
FROM largest_tip
LEFT JOIN public.taxi_zone_lookup tzl 
ON largest_tip."DOLocationID" = tzl."LocationID" 
~~~


**Long Island City/Queens Plaza**

## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET



## Week 1 Homework Terraform

In this homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP install Terraform. Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 1. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.



~~~
google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/dtc-de-course-2023/datasets/trips_data_all]
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc_data_lake_dtc-de-course-2023]
~~~


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/S57Xs3HL9nB3YTzj9)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET


