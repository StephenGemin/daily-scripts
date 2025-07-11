import sys
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

pd.set_option("display.max_colwidth", None)

root = Path().home() / "Downloads"
fpin = root / "ado_import.csv"
fpmdtemp = root / "ado_exporttest.md"
fpout = root / "ado_import_clean.csv"


def clean_html_keep_br_only(text):
    if not isinstance(text, str):
        return text

    soup = BeautifulSoup(text, "html.parser")

    # Normalize all <br ...> → <br>
    for br in soup.find_all("br"):
        br.attrs = {}  # remove all attributes

    # Remove all other tags, keep their inner content
    for tag in soup.find_all():
        if tag.name.lower() != "br":
            tag.unwrap()

    return str(soup).strip()


def strip_html(text):
    if isinstance(text, str):
        return BeautifulSoup(text, "html.parser").get_text().strip()
    return text


def parse_args():
    parser = ArgumentParser(
        description="utilities to work with Azure DevOps work item imports"
    )
    # parser.add_argument("file_in", help="absolute path to .csv")
    # parser.add_argument("-o", help="absolute path to output file")
    parser.parse_args()
    return parser


def csv2md():
    # df1 = pd.read_csv(fpin, skipinitialspace=True)
    # df1["Description"] = df1["Description"].map(clean_html_keep_br_only)
    # df1["Acceptance Criteria"] = df1["Acceptance Criteria"].map(clean_html_keep_br_only)
    # df1.to_markdown(fpmdtemp, index=False, tablefmt="github")

    # Drop the left-most and right-most null columns
    # Drop the header underline row
    df2 = pd.read_table(fpmdtemp, sep="|").dropna(axis=1, how="all").iloc[1:]
    df2.columns = df2.columns.str.strip()
    for col in df2.select_dtypes(include="object").columns:
        df2[col] = df2[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.reset_index(drop=True)
    df2.to_csv(fpout, index=False)
    # breakpoint()


def main():
    # parser = parse_args()
    try:
        csv2md()
    except Exception:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
