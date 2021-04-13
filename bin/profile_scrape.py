"""Script to scrape steel profile data from thw web"""

# Standard library imports
from pathlib import Path

# Third party imports
import requests
import pandas as pd


if __name__ == "__main__":
    # Read steel profile tables from html
    url = "https://www.prontubeam.com/structural-steelwork-handbook"
    response = requests.get(url)
    dfs = pd.read_html(response.text, header=0, skiprows=4)

    for df in dfs:
        # Delete the first unused column
        del df["Unnamed: 0"]

        # Get the name of the profile
        profile_name = df.loc[1][0].split(" ")[0]

        # Rename columns (NOTE: The SQLite database is case insensitive)
        df = df.rename(columns={df.columns[0]: "name", "iy": "iiy", "iz": "iiz"})

        # Drop row with units
        df = df.drop(0, "index")

        # Remove space in profile name, HEA 100 => HEA100
        df["name"] = df["name"].str.replace(" ", "")

        # Save to file
        save_path = Path(__file__).parent.parent / f"assets/{profile_name}.csv"
        df.to_csv(save_path, index=False)
        print(f'Saved {profile_name} data to "{save_path}"')
