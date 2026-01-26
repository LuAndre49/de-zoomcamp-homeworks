# DataTalksClub DE Zoomcamp - Homework 1

## Question 1
### Commands used:
docker run -it --entrypoint=bash python:3.13

pip --version
### Answer: 25.3

## Question 2
### Answer: db:5432

## Question 3
### Commands used:
docker-compose up -d

pip install uv

uv init --python=3.13

uv add pandas pyarrow

uv add sqlalchemy psycopg2-binary

docker build -t ingest:v001 .

docker run --rm --network=homework1_default ingest:v001

in pgadmin:
SELECT COUNT(*)
FROM public.green_taxi_data g
WHERE g.lpep_pickup_datetime >= '2025-11-01'
  AND g.lpep_pickup_datetime < '2025-12-01'
  AND g.trip_distance <= 1;

### Answer: 8007

## Question 4
### Commands used:

in pgadmin:
SELECT g.lpep_pickup_datetime
FROM public.green_taxi_data g
WHERE g.trip_distance < 100
ORDER BY g.trip_distance DESC
LIMIT 1

### Answer: 2025-11-14

## Question 5:
### Commands used:

in pgadmin:
SELECT 
    z1."Zone", 
    SUM(g."total_amount") AS total_amount_sum
FROM public.green_taxi_data g
LEFT JOIN zones z1
    ON g."PULocationID" = z1."LocationID"
WHERE g."lpep_pickup_datetime" >= '2025-11-18'
  AND g."lpep_pickup_datetime" < '2025-11-19'
GROUP BY z1."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;

### Answer: East Harlem North

## Question 6:
### Commands used:

in pgadmin:
SELECT z2."Zone", MAX(tip_amount) as max_tip
FROM public.green_taxi_data g
LEFT JOIN zones z1
ON g."PULocationID" = z1."LocationID"
LEFT JOIN zones z2
ON g."DOLocationID" = z2."LocationID"
WHERE z1."Zone" = 'East Harlem North' 
	  AND
	  EXTRACT(YEAR FROM g."lpep_pickup_datetime") = 2025 
	  AND 
	  EXTRACT(MONTH FROM g."lpep_pickup_datetime") = 11
GROUP BY z2."Zone"
ORDER BY max_tip DESC
LIMIT 1;

### Answer: Yorkville West


## Question 7:
### Commands used:

terraform init

terraform apply -auto-approve

terraform destroy

### Answer: terraform init, terraform apply -auto-approve, terraform destroy