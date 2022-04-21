"""
Rate drugs by number of ex-us OECD formularies they appear in.
"""
import os
import re
import dotenv

if __name__ == "__main__":
    print("Rating drugs...")

    print("Reading data...")

    prefix = "debug" if (os.getenv("DEBUG", "True") == "True") else "prod"

    fda = set(open(f"data/{prefix}/fda.txt").read().splitlines())
    print(f"Found {len(fda)} FDA terms...")

    formularies = {
        country_code: set(
            open(f"data/{prefix}/{country_code}.txt").read().splitlines())
        for country_code in ["ca", "de", "uk"]
    }

    print("Gross intersections with FDA:")
    for key, values in formularies.items():
        print(f"{key}: {len(fda.intersection(values)) / len(fda):.2f}")
