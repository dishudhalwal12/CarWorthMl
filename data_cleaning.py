from pathlib import Path

import numpy as np
import pandas as pd


REPO_DIR = Path(__file__).resolve().parent
KAGGLE_FILE = REPO_DIR / "used_cars_dataset_v2.csv"
LOCAL_FILE = REPO_DIR / "car data.csv"
OUTPUT_FILE = REPO_DIR / "Cleaned_Car_data.csv"
REFERENCE_YEAR = 2026
ASK_PRICE_TO_MARKET_FACTOR = 0.95


OWNER_MAP = {
    "first": "first",
    "1st": "first",
    "second": "second",
    "2nd": "second",
    "third": "third",
    "3rd": "third",
    "fourth": "fourth+",
    "fourth+": "fourth+",
    "4th": "fourth+",
    "test": "unknown",
}

OWNER_MAP_NUMERIC = {
    0: "first",
    1: "second",
    2: "third",
    3: "fourth+",
}


def clean_price(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(r"[^0-9.]", "", regex=True)
        .replace("", np.nan)
        .astype(float)
    )


def clean_kms(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(r"[^0-9.]", "", regex=True)
        .replace("", np.nan)
        .astype(float)
    )


def normalize_owner(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.strip().str.lower()
    return cleaned.map(OWNER_MAP).fillna(cleaned)


def build_name(company: pd.Series, model: pd.Series) -> pd.Series:
    return (company.astype(str).str.strip() + " " + model.astype(str).str.strip()).str.strip()


def load_kaggle_source() -> pd.DataFrame:
    if not KAGGLE_FILE.exists():
        raise FileNotFoundError(
            "used_cars_dataset_v2.csv not found. Run generate_dataset.py first."
        )

    raw = pd.read_csv(KAGGLE_FILE)

    df = pd.DataFrame(
        {
            "company": raw["Brand"].astype(str).str.strip().str.title(),
            "model_name": raw["model"].astype(str).str.strip().str.title(),
            "year": pd.to_numeric(raw["Year"], errors="coerce"),
            "age": REFERENCE_YEAR - pd.to_numeric(raw["Year"], errors="coerce"),
            "kms_driven": clean_kms(raw["kmDriven"]),
            "fuel_type": raw["FuelType"].astype(str).str.strip().str.title(),
            "transmission": raw["Transmission"].astype(str).str.strip().str.title(),
            "owner": normalize_owner(raw["Owner"]),
            "Price": clean_price(raw["AskPrice"]) * ASK_PRICE_TO_MARKET_FACTOR,
        }
    )

    df["name"] = build_name(df["company"], df["model_name"])
    df["source"] = "kaggle_market"
    return df


def load_local_source() -> pd.DataFrame:
    if not LOCAL_FILE.exists():
        raise FileNotFoundError("car data.csv not found.")

    raw = pd.read_csv(LOCAL_FILE)
    split_names = raw["Car_Name"].astype(str).str.strip().str.split()

    company = split_names.str[0].fillna("Unknown").str.title()
    model_name = split_names.str[1:].str.join(" ").replace("", "Base").str.title()

    df = pd.DataFrame(
        {
            "company": company,
            "model_name": model_name,
            "year": pd.to_numeric(raw["Year"], errors="coerce"),
            "age": REFERENCE_YEAR - pd.to_numeric(raw["Year"], errors="coerce"),
            "kms_driven": pd.to_numeric(raw["Kms_Driven"], errors="coerce"),
            "fuel_type": raw["Fuel_Type"].astype(str).str.strip().str.title(),
            "transmission": raw["Transmission"].astype(str).str.strip().str.title(),
            "owner": raw["Owner"].map(OWNER_MAP_NUMERIC).fillna("unknown"),
            "Price": pd.to_numeric(raw["Selling_Price"], errors="coerce") * 100000,
        }
    )

    df["name"] = build_name(df["company"], df["model_name"])
    df["source"] = "cardekho_sales"
    return df


def finalize(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in ["company", "model_name", "name", "fuel_type", "transmission", "owner", "source"]:
        cleaned[column] = cleaned[column].astype(str).str.strip()

    cleaned = cleaned.replace({"": np.nan, "Nan": np.nan, "None": np.nan})
    cleaned = cleaned.dropna(
        subset=[
            "company",
            "model_name",
            "name",
            "year",
            "age",
            "kms_driven",
            "fuel_type",
            "transmission",
            "owner",
            "Price",
        ]
    )

    cleaned["year"] = cleaned["year"].astype(int)
    cleaned["age"] = cleaned["age"].astype(int)
    cleaned["kms_driven"] = cleaned["kms_driven"].round().astype(int)
    cleaned["Price"] = cleaned["Price"].round().astype(int)

    cleaned = cleaned[
        cleaned["year"].between(1998, 2025)
        & cleaned["age"].between(0, 30)
        & cleaned["kms_driven"].between(100, 500000)
        & cleaned["Price"].between(50000, 10000000)
        & cleaned["fuel_type"].isin(["Petrol", "Diesel", "Cng", "Lpg", "Electric"])
        & cleaned["transmission"].isin(["Manual", "Automatic"])
    ].copy()

    cleaned.loc[cleaned["fuel_type"] == "Cng", "fuel_type"] = "CNG"
    cleaned.loc[cleaned["fuel_type"] == "Lpg", "fuel_type"] = "LPG"

    cleaned["owner"] = normalize_owner(cleaned["owner"]).replace("", "unknown")
    cleaned["model_name"] = cleaned["model_name"].str.replace("  ", " ", regex=False)
    cleaned["name"] = build_name(cleaned["company"], cleaned["model_name"])
    cleaned["price_lakh"] = (cleaned["Price"] / 100000).round(2)

    cleaned = cleaned.drop_duplicates(
        subset=[
            "company",
            "model_name",
            "year",
            "kms_driven",
            "fuel_type",
            "transmission",
            "owner",
            "Price",
            "source",
        ]
    ).reset_index(drop=True)

    return cleaned


def main() -> None:
    kaggle_df = load_kaggle_source()
    local_df = load_local_source()
    combined = pd.concat([kaggle_df, local_df], ignore_index=True)
    cleaned = finalize(combined)

    cleaned.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {OUTPUT_FILE.name} with {len(cleaned)} rows")
    print(f"Brands: {cleaned['company'].nunique()} | Models: {cleaned['name'].nunique()}")
    print(f"Sources: {cleaned['source'].value_counts().to_dict()}")
    print(
        "Price range: "
        f"₹{cleaned['Price'].min():,} to ₹{cleaned['Price'].max():,}"
    )


if __name__ == "__main__":
    main()
