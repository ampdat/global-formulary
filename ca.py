import requests
import requests_cache

if __name__ == "__main__":
    session = requests_cache.CachedSession()
    print("Downloading data...")
    # MEDICINES NOT REIMBURSED THROUGH NATIONAL PRICES AND
    # DIRECTLY COMMISSIONED BY NHS ENGLAND
    r = session.get(
        "https://www.england.nhs.uk/wp-content/uploads/2017/04/NHS-England-drugs-list-v16.1-Oct-2021-March-2022.pdf",
        stream=True)
    r.raise_for_status()
    print("Extracting data...")
    pages = read_pdf(r.raw, pages="all",
                     multiple_tables=True, pandas_options={"header": None})
    print("Merging data...")
