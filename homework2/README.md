# DataTalksClub DE Zoomcamp - Homework 2

## Commands for setting up and running the Kestra flows:
### Launching the containers
docker compose up -d

### Log in to kestra
username: "admin@kestra.io"

password: Admin1234!

### Execute Flows

execute homework_2_gcp_kv

execute homework_2_gcp_setup

execute homework_2_gcp_taxi_mainflow

## Question 1
### Answer: 128.3 MiB

## Question 2
### Answer: green_tripdata_2020-04.csv

## Question 3
### Commands used:
in bigquery:
SELECT COUNT(*) AS total_rows
FROM `dtc-de-course-484308.zoomcamp.yellow_tripdata`
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020;

### Answer: 24,648,499

## Question 4
### Commands used:
in bigquery:
SELECT COUNT(*) AS total_rows
FROM `dtc-de-course-484308.zoomcamp.green_tripdata`
WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2020;

### Answer: 1,734,051

## Question 5
### Commands used:
in bigquery:
SELECT COUNT(*) AS total_rows
FROM `dtc-de-course-484308.zoomcamp.yellow_tripdata`
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2021 AND EXTRACT(MONTH FROM tpep_pickup_datetime) = 3;

### Answer: 1,925,152

## Question 6
### Answer: Add a timezone property set to America/New_York in the Schedule trigger configuration