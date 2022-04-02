"""
Scrape UK Formulary
"""
import os
import re
import dotenv
import requests_cache

import tabula

import pandas as pd

if __name__ == "__main__":
    print("Scraping UK Formulary")

    dotenv.load_dotenv()
    os.makedirs("data", exist_ok=True)

    session = requests_cache.CachedSession("data/http_cache")
    print("Downloading data...")
    # MEDICINES NOT REIMBURSED THROUGH NATIONAL PRICES AND
    # DIRECTLY COMMISSIONED BY NHS ENGLAND
    r = session.get(
        "https://www.england.nhs.uk/wp-content/uploads/2017/04/NHS-England-drugs-list-v16.1-Oct-2021-March-2022.pdf",
        stream=True)
    r.raise_for_status()

    pages = "1-3" if (os.getenv("DEBUG", "True") == "True") else "all"
    print(f"Extracting {pages} pages...")
    tables = tabula.read_pdf(r.raw, pages=pages)

    print("Merging data...")

    drugs = pd.concat([t.iloc[:, 0] for t in tables]) \
        .dropna() \
        .drop_duplicates() \
        .drop(0).values
    names = list([i.lower() for d in drugs for i in re.findall("[A-Z]+", d)])
    print(f"Extracted {len(drugs)} drugs...")

    print("Writing data...")
    with open("data/uk.txt", "w") as f:
        f.write("\n".join(names))

    print("Done!")
