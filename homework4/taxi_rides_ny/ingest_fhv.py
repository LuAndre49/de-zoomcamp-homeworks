import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv"
DATA_DIR = Path("data/fhv")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_fhv():
    for year in range(2019, 2022):
        for month in range(1, 13):
            if year == 2021 and month > 7:
                continue  # FHV ends at 2021-07

            filename = f"fhv_tripdata_{year}-{month:02d}.csv.gz"
            filepath = DATA_DIR / filename

            if filepath.exists():
                print(f"Skipping {filename}, already exists.")
                continue

            url = f"{BASE_URL}/{filename}"
            print(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Completed download: {filename}")

if __name__ == "__main__":
    download_fhv()
