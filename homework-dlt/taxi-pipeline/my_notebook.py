import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import dlt
    import ibis

    pipeline = dlt.attach(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data"
    )

    con = pipeline.dataset().ibis()
    return (pipeline,)


@app.cell
def _(pipeline):
    with pipeline.sql_client() as client:
        with client.execute_query("SELECT SUM(tip_amt) FROM nyc_taxi_data LIMIT 1") as cursor:
            data = cursor.df()

    data
    return


if __name__ == "__main__":
    app.run()
