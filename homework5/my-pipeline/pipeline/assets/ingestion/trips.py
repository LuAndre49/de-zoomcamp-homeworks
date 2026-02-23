"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# TODO: Set the connection.
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
columns:
  - name: VendorID
    type: integer
  - name: pickup_datetime
    type: timestamp
  - name: dropoff_datetime
    type: timestamp
  - name: passenger_count
    type: integer
  - name: trip_distance
    type: float
  - name: RatecodeID
    type: integer
  - name: store_and_fwd_flag
    type: string
  - name: PULocationID
    type: integer
  - name: DOLocationID
    type: integer
  - name: payment_type
    type: string
  - name: fare_amount
    type: float
  - name: extra
    type: float
  - name: mta_tax
    type: float
  - name: tip_amount
    type: float
  - name: tolls_amount
    type: float
  - name: improvement_surcharge
    type: float
  - name: total_amount
    type: float
  - name: congestion_surcharge
    type: float
  - name: taxi_type
    type: string
  - name: extracted_at
    type: timestamp
@bruin"""

# TODO: Add imports needed for your ingestion (e.g., pandas, requests).
# - Put dependencies in the nearest `requirements.txt` (this template has one at the pipeline root).
# Docs: https://getbruin.com/docs/bruin/assets/python
import os
import json
import pandas as pd

# TODO: Only implement `materialize()` if you are using Bruin Python materialization.
# If you choose the manual-write approach (no `materialization:` block), remove this function and implement ingestion
# as a standard Python script instead.
def materialize():
    """
    TODO: Implement ingestion using Bruin runtime context.

    Required Bruin concepts to use here:
    - Built-in date window variables:
      - BRUIN_START_DATE / BRUIN_END_DATE (YYYY-MM-DD)
      - BRUIN_START_DATETIME / BRUIN_END_DATETIME (ISO datetime)
      Docs: https://getbruin.com/docs/bruin/assets/python#environment-variables
    - Pipeline variables:
      - Read JSON from BRUIN_VARS, e.g. `taxi_types`
      Docs: https://getbruin.com/docs/bruin/getting-started/pipeline-variables

    Design TODOs (keep logic minimal, focus on architecture):
    - Use start/end dates + `taxi_types` to generate a list of source endpoints for the run window.
    - Fetch data for each endpoint, parse into DataFrames, and concatenate.
    - Add a column like `extracted_at` for lineage/debugging (timestamp of extraction).
    - Prefer append-only in ingestion; handle duplicates in staging.
    """
    vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = vars["taxi_types"]

    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]

    dates = pd.date_range(start=start_date, end=end_date, freq="MS")
    
    dfs = []
    for taxi_type in taxi_types:
        for date in dates:
            month_str = f"{date.month:02d}"
            year = date.year

            url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/{taxi_type}_tripdata_{year}-{month_str}.csv.gz"
            
            try:
                df = pd.read_csv(url)
                df["taxi_type"] = taxi_type
                df["extracted_at"] = pd.Timestamp.utcnow()
                
                if taxi_type == "green":
                  df.rename(
                      columns={
                          "lpep_pickup_datetime": "pickup_datetime",
                          "lpep_dropoff_datetime": "dropoff_datetime",
                      },
                      inplace=True,
                  )
                elif taxi_type == "yellow":
                  df.rename(
                      columns={
                          "tpep_pickup_datetime": "pickup_datetime",
                          "tpep_dropoff_datetime": "dropoff_datetime",
                      },
                      inplace=True,
                  )
                dfs.append(df)
            except Exception as e:
                print(f"Skipping {url}: {e}")

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)