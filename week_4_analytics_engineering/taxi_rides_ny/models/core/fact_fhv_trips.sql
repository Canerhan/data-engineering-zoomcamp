{{ config(materialized='table') }}

with trip_data as (
    select *
    from {{ ref('stg_fhv_tripdata') }}
), 

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)


SELECT
tripid,
dispatching_base_num,
pickup_datetime,
dropOff_datetime,
PUlocationID,
pickup_zone.borough as pickup_borough, 
pickup_zone.zone as pickup_zone, 
DOlocationID,
dropoff_zone.borough as dropoff_borough, 
dropoff_zone.zone as dropoff_zone, 
SR_Flag,
Affiliated_base_number
FROM trip_data
inner join dim_zones as pickup_zone
on trip_data.PUlocationID = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trip_data.DOlocationID = dropoff_zone.locationid