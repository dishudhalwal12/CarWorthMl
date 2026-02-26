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
car = car[car["kms_driven"].str.isnumeric()]
car["kms_driven"] = car["kms_driven"].astype(int)

# 4. Clean year — cast to int, drop non-numeric / NaN
car["year"] = car["year"].astype(str).str.replace(".0", "", regex=False).str.strip()
car = car[car["year"].str.isnumeric()]
car["year"] = car["year"].astype(int)
car = car[(car["year"] >= 1995) & (car["year"] <= 2024)]

# 5. Drop NaN fuel_type
car = car[~car["fuel_type"].isna()]
car = car[car["fuel_type"].isin(["Petrol", "Diesel", "LPG"])]

# 6. Clean name — keep first 3 words
car["name"] = car["name"].str.split().str[:3].str.join(" ")

# 7. Reset index
car = car.reset_index(drop=True)

car.to_csv("Cleaned_Car_data.csv", index=False)
print(f"✅ Cleaned_Car_data.csv — {len(car)} rows, {car.shape[1]} columns")
print(f"   Columns dtypes:\n{car.dtypes}")
print(f"   NaN check:\n{car.isnull().sum()}")
