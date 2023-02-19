{{ config(materialized='view') }}

with trip_data AS (

SELECT 
*,
ROW_NUMBER() OVER (PARTITION BY dispatching_base_num, pickup_datetime) AS rn
FROM {{ source('staging', 'fhv_2019_native_partitioned')  }}
--WHERE dispatching_base_num IS NOT NULL

)

SELECT
{{ dbt_utils.surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} AS tripid,
dispatching_base_num,
pickup_datetime,
dropOff_datetime,
PUlocationID,
DOlocationID,
SR_Flag,
Affiliated_base_number
FROM trip_data
--where rn = 1


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}