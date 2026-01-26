import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@db:5432/ny_taxi')
green_taxi_df = pd.read_parquet("green_tripdata_2025-11.parquet", engine='pyarrow')
zones_df = pd.read_csv("taxi_zone_lookup.csv")

green_taxi_df.to_sql(name="green_taxi_data", con=engine, if_exists='replace')

zones_df.to_sql(name="zones", con=engine, if_exists='replace')