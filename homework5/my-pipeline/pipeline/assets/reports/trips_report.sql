/* @bruin

# Docs:
# - SQL assets: https://getbruin.com/docs/bruin/assets/sql
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks: https://getbruin.com/docs/bruin/quality/available_checks

# TODO: Set the asset name (recommended: reports.trips_report).
name: reports.trips_report

# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: duckdb.sql

# TODO: Declare dependency on the staging asset(s) this report reads from.
depends:
  - staging.trips

# TODO: Choose materialization strategy.
# For reports, `time_interval` is a good choice to rebuild only the relevant time window.
# Important: Use the same `incremental_key` as staging (e.g., pickup_datetime) for consistency.
materialization:
  type: table
  # suggested strategy: time_interval
  strategy: time_interval
  # TODO: set to your report's date column
  incremental_key: pickup_datetime
  # TODO: set to `date` or `timestamp`
  time_granularity: timestamp

# TODO: Define report columns + primary key(s) at your chosen level of aggregation.
columns:
  - name: vendor_id
    type: integer
    description: Vendor identifier
    primary_key: true
  - name: pickup_datetime
    type: timestamp
    description: Date and time of pickup
    primary_key: true
  - name: taxi_type
    type: string
    description: Type of taxi
    primary_key: true
  - name: avg_passengers
    type: float
    description: Average number of passengers
    checks:
      - name: non_negative
  - name: avg_fare
    type: float
    description: Average fare collected
    checks:
      - name: non_negative
  - name: avg_tip
    type: float
    description: Average amount of tips collected
    checks:
      - name: non_negative
  - name: total_daily_passengers
    type: integer
    description: Total number of passengers
    checks:
      - name: non_negative
  - name: total_trips
    type: integer
    description: Total number of trips
    checks:
      - name: non_negative
@bruin */

-- Purpose of reports:
-- - Aggregate staging data for dashboards and analytics
-- Required Bruin concepts:
-- - Filter using `{{ start_datetime }}` / `{{ end_datetime }}` for incremental runs
-- - GROUP BY your dimension + date columns

SELECT t.vendor_id, 
       t.pickup_datetime, 
       t.taxi_type,
       AVG(t.passenger_count) AS avg_passengers,
       AVG(t.fare_amount) AS avg_fare,
       AVG(t.tip_amount) AS avg_tip,
       SUM(t.passenger_count) AS total_daily_passengers,
       COUNT(*) AS total_trips
FROM staging.trips t
WHERE t.pickup_datetime >= '{{ start_datetime }}'
  AND t.pickup_datetime < '{{ end_datetime }}'
GROUP BY t.vendor_id, t.pickup_datetime, t.taxi_type