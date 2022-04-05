"""
Rate drugs by number of ex-us OECD formularies they appear in.
"""
import os
import re
import dotenv

if __name__ == "__main__":
    print("Rating drugs...")

    print("Reading data...")

    formularies = [
        open(path).read().splitlines() for path in [
            "data/fda.txt",
            "data/ca.txt",
            "data/uk.txt",
        ]
    ]

    common = set.intersection(*[set(list) for list in formularies])
    print(f"Found {len(common)} common drugs...")
