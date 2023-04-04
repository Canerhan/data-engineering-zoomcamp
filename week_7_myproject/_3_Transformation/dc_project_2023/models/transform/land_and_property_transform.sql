with source AS (

    select * from {{ ref('land_and_property_optimized_raw') }}

),

renamed as (
    select
        {{ adapter.quote("Account_Customer") }} AS customer,
        {{ adapter.quote("FR") }},
        {{ adapter.quote("DFL") }},
        {{ adapter.quote("TP") }},
        {{ adapter.quote("DLG") }},
        {{ adapter.quote("OS_W_") }},
        {{ adapter.quote("OS_NPW_") }},
        {{ adapter.quote("OS_P_") }},
        {{ adapter.quote("OS_NPP_") }},
        {{ adapter.quote("SIMS") }},
        {{ adapter.quote("OC1") }},
        {{ adapter.quote("OC2") }},
        {{ adapter.quote("date_added") }}

    from source
)
select * from renamed