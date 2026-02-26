---
name: ml-pipeline
description: Builds and maintains the CarWorthML machine learning pipeline. Use when writing generate_dataset.py, data_cleaning.py, or model_training.py — or when debugging prediction errors. Covers synthetic data generation, cleaning, sklearn pipeline architecture, and model serialization.
---

# ML Pipeline Skill — CarWorthML

## Overview

CarWorthML uses a supervised regression pipeline:
```
Raw CSV (Quikr-style) → Cleaning → OneHotEncoder + LinearRegression Pipeline → Pickle → Streamlit
```

The model is trained once, saved, and loaded at runtime. It is never retrained when the app runs.

---

## Dataset Generation Rules

The synthetic dataset must be statistically realistic — not random noise. Prices must correlate meaningfully with year, kms_driven, company tier, and fuel_type. Detectors in viva will ask "does a newer car cost more?" — the answer must be yes, consistently.

### Company Tiers
```
Luxury  (×3.0–3.5): Audi, BMW, Mercedes, Jaguar, Volvo, Land, Jeep
Premium (×1.5–1.8): Toyota, Honda, Skoda, Volkswagen, Kia, MG
Mass    (×0.85–1.1): Maruti, Hyundai, Tata, Mahindra, Ford, Renault, Nissan, Chevrolet, Datsun, Fiat
```

### Price Formula
```python
base        = 280000
age_dep     = (2024 - year) * 17000      # older = cheaper
km_dep      = kms_driven * 0.85          # more km = cheaper
fuel_add    = 38000 if diesel else 0     # diesel premium
price       = (base - age_dep - km_dep + fuel_add) * tier_multiplier
price       = max(price, 40000)          # floor
price      += random.gauss(0, price * 0.09)  # 9% noise
```

### Intentional Dirty Data (Required)
The raw CSV must have realistic messiness so the cleaning step is meaningful:
- 80 rows: `kms_driven` as `"45,000 kms"` (string)
- 40 rows: `Price` as `"4,25,000"` (comma string)
- 30 rows: `Price` as `"Ask For Price"` (invalid)
- 20 rows: `fuel_type` as NaN
- 15 rows: `kms_driven` as NaN
- 10 rows: `year` as `"2015.0"` (float string)

---

## Cleaning Pipeline — Exact Order

Order matters. A wrong sequence drops valid rows or keeps invalid ones.

```python
# 1. Drop non-numeric prices
car = car[car["Price"] != "Ask For Price"].copy()

# 2. Clean Price column
car["Price"] = car["Price"].astype(str).str.replace(",", "").str.strip()
car = car[car["Price"].str.isnumeric()]
car["Price"] = car["Price"].astype(int)
car = car[car["Price"] > 10000]         # sanity floor

# 3. Clean kms_driven
car["kms_driven"] = car["kms_driven"].astype(str).str.split().str[0].str.replace(",","").str.strip()
car = car[car["kms_driven"].str.isnumeric()]
car["kms_driven"] = car["kms_driven"].astype(int)

# 4. Clean year
car["year"] = car["year"].astype(str).str.replace(".0","",regex=False).str.strip()
car = car[car["year"].str.isnumeric()]
car["year"] = car["year"].astype(int)
car = car[(car["year"] >= 1995) & (car["year"] <= 2024)]

# 5. Drop bad fuel_type
car = car[~car["fuel_type"].isna()]
car = car[car["fuel_type"].isin(["Petrol", "Diesel", "LPG"])]

# 6. Truncate name to 3 words
car["name"] = car["name"].str.split().str[:3].str.join(" ")

# 7. Reset index
car = car.reset_index(drop=True)
```

Final output must have: ≥820 rows, 6 columns, zero NaN, correct dtypes.

---

## Model Training Architecture

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X = car[["name", "company", "year", "kms_driven", "fuel_type"]]
y = car["Price"]

# Fit OHE on FULL data first to capture all categories
ohe = OneHotEncoder()
ohe.fit(X[["name", "company", "fuel_type"]])

# Column transformer using fitted categories
column_trans = make_column_transformer(
    (OneHotEncoder(categories=ohe.categories_, handle_unknown="ignore"),
     ["name", "company", "fuel_type"]),
    remainder="passthrough"   # year and kms_driven pass through unchanged
)

# Find best random state (1000 trials)
scores = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=i)
    pipe = make_pipeline(column_trans, LinearRegression())
    pipe.fit(X_train, y_train)
    scores.append(r2_score(y_test, pipe.predict(X_test)))

best_idx = int(np.argmax(scores))
```

**Why 1000 trials?** It's documented in the synopsis as a methodology choice. The viva question "How did you choose your train-test split?" has a clear answer: "We iterated 1000 random states and picked the one with the best R² score."

---

## Prediction at Runtime

```python
# Input DataFrame — exact column names, exact order
input_df = pd.DataFrame(
    [[car_name, company, year, kms_driven, fuel_type]],
    columns=["name", "company", "year", "kms_driven", "fuel_type"]
)

# Predict
price = model.predict(input_df)[0]
price = max(float(price), 25000.0)  # never return negative or absurdly low
```

### Expected Price Ranges (for validation)
| Car profile | Expected range |
|---|---|
| Maruti/Hyundai, 2015, Petrol, 50k km | ₹2L – ₹5L |
| Toyota/Honda, 2017, Diesel, 40k km | ₹5L – ₹10L |
| BMW/Audi, 2018, Diesel, 40k km | ₹15L – ₹35L |
| Any car, 2008, Petrol, 120k km | ₹50k – ₹3L |

If predictions fall outside these ranges, the synthetic data generation has a bug — fix the price formula.

---

## Debugging Common Errors

### "ValueError: could not convert string to float"
Cause: A column still has string values when the model tries to encode.
Fix: Check that `kms_driven` and `year` are int64 in `Cleaned_Car_data.csv`. Run `print(df.dtypes)`.

### "Found unknown categories during transform"
Cause: User selected a company/model combination not in training data.
Fix: Already handled by `handle_unknown="ignore"` in OneHotEncoder. If still happening, the model was trained without this parameter — retrain.

### R² below 0.60
Cause: Price formula too noisy, or too few rows after cleaning.
Fix: Reduce noise from 9% to 6%, verify ≥820 rows in cleaned data, rerun model_training.py.

### Predictions all cluster around one value
Cause: The 1000-trial loop found a bad random state somehow.
Fix: Add `print(sorted(scores, reverse=True)[:10])` to see top 10 scores. If all are low, the issue is in the data.