{{ config(materialized='table') }}

WITH initial AS (
    SELECT *
    FROM read_csv_auto(
        'data/fhv/fhv_tripdata_2019-*.csv.gz',
        strict_mode=False,
        ignore_errors=True
    )
)

SELECT
    dispatching_base_num,
    pickup_datetime,
    dropoff_datetime,
    PUlocationID AS pickup_location_id,
    DOlocationID AS dropoff_location_id, 
    SR_Flag,
    affiliated_base_number
FROM initial
WHERE dispatching_base_num IS NOT NULL
