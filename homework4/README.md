# DataTalksClub DE Zoomcamp - Homework 4

## Commands for setting up DBT:

### Downloading tripdata
python ingest.py

### Build models
dbt build --target prod


## Question 1

### Answer: stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)

## Question 2

### Answer: dbt will fail the test, returning a non-zero exit code

## Question 3

ran query in duckdb:
select
	COUNT(*)
from taxi_rides_ny.prod.fct_monthly_zone_revenue

### Answer: 12,998

## Question 4

ran query in duckdb:
SELECT
    pickup_zone,
    SUM(revenue_monthly_total_amount) AS total_revenue
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND EXTRACT(year FROM revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;

### Answer: East Harlem North

## Question 5

ran query in duckdb:
SELECT SUM(total_monthly_trips)
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND EXTRACT(year FROM revenue_month) = 2019 AND EXTRACT(month FROM revenue_month) = 10

### Answer: 384,624

## Question 6

ran ingest_fhv.py

ran command:
dbt run -s stg_fhv_tripdata

ran query in duckdb:
select
	COUNT(*)
from taxi_rides_ny.dev.stg_fhv_tripdata

### Answer: 43,244,693