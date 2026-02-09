# DataTalksClub DE Zoomcamp - Homework 2

## Commands for setting up the yellow tripdata files in BigQuery:

### Creating service account
Created service account in project with "Storage Admin" role and then generated key as JSON file, saved as gcs.json

### Downloading the files:
python load_yellow_taxi_data.py

### Setting up BigQuery:
Created an empty dataset in BigQuery

Ran the following SQL commands:
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_external`
OPTIONS (
  FORMAT = 'PARQUET',
  uris = ['gs://dtc-de-course-484308_dezoomcamp_hw3_2025/yellow_tripdata_2024-*.parquet']
)

CREATE OR REPLACE TABLE `dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized`
AS
SELECT * FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_external


## Question 1
### Commands used:

in BigQuery:
SELECT COUNT(*) as total_count
FROM `dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized`

### Answer: 20,332,093

## Question 2
### Commands used:

prepared command in BigQuery:
SELECT (COUNT(DISTINCT PULocationID))
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_external

prepared command in BigQuery:
SELECT (COUNT(DISTINCT PULocationID))
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized

### Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

## Question 3
### Commands used:

prepared command in BigQuery:
SELECT PULocationID
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized

prepared command in BigQuery:
SELECT PULocationID, DOLocationID
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized

### Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

# Question 4
### Commands used:

in BigQuery:
SELECT COUNT(*) as trips_with_no_fare
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized
WHERE fare_amount = 0

### Answer: 8,333

# Question 5
### Commands used:

in BigQuery:
CREATE OR REPLACE TABLE dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT *
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized


### Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

# Question 6
### Commands used:

prepared command in BigQuery:
SELECT DISTINCT VendorID
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_materialized
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

prepared command in BigQuery:
SELECT DISTINCT VendorID
FROM dtc-de-course-484308.DE_zoomcamp_homework3.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

### Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

# Question 7
### Answer: GCP Bucket

# Question 8
### Answer: False

# Question 9
### Answer: The query is estimated to read 0 bytes. This is because COUNT(*) is simply the count of total rows in the table, which is a statistic that is stored in the table's metadata. Hence, instead of needing to query the table itself, BigQuery can simply access the table's metadata to identify how many rows are in the table.
