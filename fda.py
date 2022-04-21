"""
Download FDA list of drugs
"""
import os
import re
import dotenv
import requests
import requests_cache
import zipfile
import io
import pandas as pd

if __name__ == "__main__":
    print("Downloading FDA list of drugs...")

    dotenv.load_dotenv()

    prefix = "debug" if (os.getenv("DEBUG", "True") == "True") else "prod"
    os.makedirs(f"data/{prefix}", exist_ok=True)

    print("Downloading data...")
    session = requests_cache.CachedSession(f"data/{prefix}/http_cache")
    r = session.get("https://www.fda.gov/media/89850/download")
    r.raise_for_status()

    print("Extracting data...")
    with zipfile.ZipFile(io.BytesIO(r.content), "r") as zf:
        with zf.open("Products.txt") as f:
            df = pd.read_csv(f, sep="\t", on_bad_lines="skip")

    drug_names = set([i.lower() for d in df.DrugName.values
                      for i in re.findall("[A-Z]+", d)])
    active_ingredients = set([i.lower() for d in df.ActiveIngredient.values
                              for i in re.findall("[A-Z]+", d)])
    terms = set([i.lower()
                for i in drug_names.union(active_ingredients)
                if len(i) >= int(os.getenv("MIN_TERM_LENGTH", "5"))])
    print(f"Extracted {len(terms)} terms...")

    print("Writing data...")
    with open(f"data/{prefix}/fda.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(terms))

    print("Done!")
