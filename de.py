"""
Scrape German Formulary
"""
import os
import re
import dotenv
import requests_cache

import tabula

import pandas as pd

if __name__ == "__main__":
    print("Scraping German Formulary")

    dotenv.load_dotenv()
    os.makedirs("data", exist_ok=True)

    print("Downloading data...")
    session = requests_cache.CachedSession("data/http_cache")
    r = session.get(
        "https://www.bfarm.de/SharedDocs/Downloads/DE/Arzneimittel/Zulassung/amInformationen/Festbetraege/2022/festbetraege-20220401.pdf?__blob=publicationFile",
        stream=True)
    r.raise_for_status()

    pages = "1-3" if (os.getenv("DEBUG", "True") == "True") else "all"
    print(f"Extracting {pages} pages...")
    tables = tabula.read_pdf(r.raw, pages=pages)

    print("Extracting terms...")
    drugs = pd.concat([t.iloc[:, 0] for t in tables]) \
        .dropna() \
        .drop_duplicates()
    names = pd.concat([t.iloc[:, 10] for t in tables]) \
        .dropna() \
        .drop_duplicates()
    terms = set([i.lower()
                for dn in pd.concat([drugs, names]).values
                for i in re.findall("[A-Za-z]+", dn)
                if len(i) >= int(os.getenv("MIN_TERM_LENGTH", "5"))])
    print(f"Extracted {len(terms)} terms...")

    print("Writing data...")
    with open("data/de.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(terms))

    print("Done!")
