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
    os.makedirs("data", exist_ok=True)

    session = requests_cache.CachedSession("data/http_cache")
    r = session.get("https://www.fda.gov/media/89850/download")
    r.raise_for_status()

    print("Extracting data...")
    with zipfile.ZipFile(io.BytesIO(r.content), "r") as zf:
        with zf.open("Products.txt") as f:
            df = pd.read_csv(f, sep="\t", on_bad_lines="skip")

    drug_names = list([i.lower() for d in df.DrugName.values
                       for i in re.findall("[A-Z]+", d)])

    active_ingredients = list([i.lower() for d in df.ActiveIngredient.values
                               for i in re.findall("[A-Z]+", d)])

    names = drug_names + active_ingredients

    print(f"Extracted {len(names)} drugs...")

    print("Writing data...")
    with open("data/fda.txt", "w") as f:
        f.write("\n".join(names))

    print("Done!")
