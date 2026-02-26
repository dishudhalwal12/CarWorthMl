import pandas as pd

car = pd.read_csv("quikr_car.csv")
print(f"Raw rows: {len(car)}")

# 1. Drop "Ask For Price"
car = car[car["Price"] != "Ask For Price"].copy()

# 2. Clean Price — remove commas, cast to int
car["Price"] = car["Price"].astype(str).str.replace(",", "").str.strip()
car = car[car["Price"].str.isnumeric()]
car["Price"] = car["Price"].astype(int)
car = car[car["Price"] > 10000]          # sanity floor

# 3. Clean kms_driven — extract numeric part
car["kms_driven"] = (
    car["kms_driven"]
    .astype(str)
    .str.split().str[0]
    .str.replace(",", "")
    .str.strip()
)
car = car[car["kms_driven"].str.isnumeric().fillna(False)]
car["kms_driven"] = car["kms_driven"].astype(int)

# 4. Clean year — cast to int, drop non-numeric / NaN
car["year"] = car["year"].astype(str).str.replace(".0", "", regex=False).str.strip()
car = car[car["year"].str.isnumeric()]
car["year"] = car["year"].astype(int)
car = car[(car["year"] >= 1995) & (car["year"] <= 2026)]

# 5. Drop NaN fuel_type
car = car[~car["fuel_type"].isna()]
car = car[car["fuel_type"].isin(["Petrol", "Diesel", "LPG"])]

# 6. Clean name — keep first 3 words
car["name"] = car["name"].str.split().str[:3].str.join(" ")

# 7. Apply 2026 market inflation multiplier
# Original Quikr data is from ~2019-2020. Indian used car prices have risen
# ~50% since then due to post-COVID demand surge and supply constraints.
INFLATION_FACTOR = 1.55
car["Price"] = (car["Price"] * INFLATION_FACTOR).astype(int)

# 8. Reset index, drop any stale index columns
car = car.reset_index(drop=True)
if "Unnamed: 0" in car.columns:
    car = car.drop(columns=["Unnamed: 0"])

car.to_csv("Cleaned_Car_data.csv", index=False)
print(f"✅ Cleaned_Car_data.csv — {len(car)} rows, {car.shape[1]} columns")
print(f"   Price range: ₹{car['Price'].min():,} – ₹{car['Price'].max():,}")
print(f"   Median price: ₹{car['Price'].median():,.0f}")
print(f"   Columns dtypes:\n{car.dtypes}")
print(f"   NaN check:\n{car.isnull().sum()}")
