# DataTalksClub DE Zoomcamp - Homework 6
### Command:
jupyter notebook

then accessed the homework6.ipynb file

## Question 1

### Commands used:
spark.version

### Answer: '4.1.1'

## Question 2

### Commands used:

df = spark.read \
     .parquet("yellow_tripdata_2025-11.parquet")

df.repartition(4).write.parquet("output/yellow_repartitioned")

### Answer: 25MB

## Question 3

### Commands used:

from pyspark.sql.functions import col, day, month

num_trips = df \
    .filter((day(col("tpep_pickup_datetime")) == 15) & (month(col("tpep_pickup_datetime")) == 11)) \
    .count()

print(num_trips)

### Answer: 162,604

## Question 4

### Commands used:

from pyspark.sql.functions import unix_timestamp

df.withColumn("duration_hours", 
    (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 3600
).orderBy("duration_hours", ascending=False) \
 .select("tpep_pickup_datetime", "tpep_dropoff_datetime", "duration_hours") \
 .limit(1).show()

### Answer: 90.6

## Question 5

### Answer: 4040

## Question 6

### Commands Used:

df.registerTempTable("taxis")
df_zones.registerTempTable("zones")
result = spark.sql(
    """
    SELECT t.PULocationID, z.Zone, COUNT(*)
    FROM taxis t
    JOIN zones z
    ON t.PULocationID = z.LocationID
    GROUP BY t.PULocationID, z.Zone
    ORDER BY COUNT(*)
    """
).show()

### Answer: Governor's Island/Ellis Island/Liberty Island
