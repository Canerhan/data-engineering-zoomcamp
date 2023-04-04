with source as (
      select * from {{ source('project_dwh', 'land_and_property_optimized') }}
)
select * from source
  