import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

@dlt.resource(write_disposition="replace")
def nyc_taxi_data():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        paginator=PageNumberPaginator(
            base_page=1,
            page_param="page",
            stop_after_empty_page=True,
            total_path=None,  # ← API returns a plain list, no total field
        ),
    )
    for page in client.paginate("/"):
        yield from page

pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="taxi_data",
)

if __name__ == "__main__":
    try:
        load_info = pipeline.run(nyc_taxi_data())
        with open("debug_log.txt", "w") as f:
            f.write(str(load_info))
        print("SUCCESS - check debug_log.txt")
    except Exception as e:
        with open("debug_log.txt", "w") as f:
            f.write(f"ERROR: {type(e).__name__}\n{str(e)}")
        print("FAILED - check debug_log.txt")