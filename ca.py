"""
Scrape Canadian Formulary
"""
import os
import re
import dotenv
import requests
import requests_cache

from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("Scraping Canadian Formulary")

    dotenv.load_dotenv()
    prefix = "debug" if (os.getenv("DEBUG", "True") == "True") else "prod"
    os.makedirs(f"data/{prefix}", exist_ok=True)

    # https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

    session = requests_cache.CachedSession(f"data/{prefix}/http_cache")
    r = session.get(
        "https://www.health.gov.on.ca/en/pro/programs/drugs/data_extract.xml",
        verify=False,
        stream=True)
    r.raise_for_status()

    print("Extracting data...")
    soup = BeautifulSoup(r.content, "html.parser")
    drugs = [d.text for d in soup.select("genericName > name")]
    names = list([i.lower() for d in drugs for i in re.findall("[A-Z]+", d)])
    print(f"Extracted {len(drugs)} drugs...")

    print("Writing data...")
    with open(f"data/{prefix}/ca.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(names))

    print("Done!")
