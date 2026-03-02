 DataTalksClub DE Zoomcamp - Homework 6
### Command:
python taxi_pipeline.py

marimo edit my_notebook.py

in marimo:
import marimo as mo
import dlt
import ibis

pipeline = dlt.attach(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="taxi_data"
)

con = pipeline.dataset().ibis()

## Question 1
### Ran query in marimo:
with pipeline.sql_client() as client:
    with client.execute_query("SELECT MIN(trip_pickup_date_time), MAX(trip_dropoff_date_time) FROM nyc_taxi_data") as cursor:
        data = cursor.df()

data

### Answer: 2009-06-01 to 2009-07-01


## Question 2
### Ran query in marimo:
with pipeline.sql_client() as client:
    with client.execute_query("SELECT SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END)/COUNT(payment_type)*100 AS proportion FROM nyc_taxi_data") as cursor:
        data = cursor.df()

data

### Answer: 26.66%

## Question 3
### Ran query in marimo:
with pipeline.sql_client() as client:
    with client.execute_query("SELECT SUM(tip_amt) FROM nyc_taxi_data LIMIT 1") as cursor:
        data = cursor.df()

data

### Answer: $6,063.41