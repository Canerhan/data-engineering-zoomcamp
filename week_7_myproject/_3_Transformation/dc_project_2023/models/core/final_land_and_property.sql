with source as (

    select * from {{ ref('land_and_property_transform') }}

)
SELECT
*
FROM source