import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# ── Company tiers and models ──────────────────────────────────────
COMPANIES = {
    # Luxury tier (multiplier 3.0)
    "Audi":       (3.0, ["A4", "A6", "Q3", "Q5", "Q7"]),
    "BMW":        (3.0, ["3 Series", "5 Series", "X1", "X3"]),
    "Mercedes":   (3.2, ["C-Class", "E-Class", "GLA", "GLC"]),
    "Jaguar":     (3.5, ["XE", "XF", "F-Pace"]),
    "Volvo":      (2.8, ["XC40", "XC60", "XC90"]),
    "Jeep":       (2.2, ["Compass", "Meridian"]),
    # Premium tier (multiplier 1.8)
    "Toyota":     (1.8, ["Innova", "Fortuner", "Corolla Altis", "Etios", "Glanza"]),
    "Honda":      (1.7, ["City", "Amaze", "Jazz", "WR-V", "Accord"]),
    "Skoda":      (1.7, ["Rapid", "Octavia", "Superb", "Kushaq"]),
    "Volkswagen": (1.6, ["Polo", "Vento", "Tiguan", "Ameo"]),
    "Kia":        (1.6, ["Seltos", "Sonet", "Carnival"]),
    "MG":         (1.5, ["Hector", "Astor", "ZS EV"]),
    # Mass market tier (multiplier 1.0)
    "Maruti":     (1.0, ["Swift", "Alto", "Wagon R", "Baleno", "Dzire", "Ertiga", "Celerio", "Ignis"]),
    "Hyundai":    (1.05,["i20", "i10", "Creta", "Verna", "Grand i10", "Santro", "Venue"]),
    "Tata":       (1.0, ["Nexon", "Harrier", "Tiago", "Tigor", "Safari", "Altroz"]),
    "Mahindra":   (1.1, ["XUV500", "Bolero", "Scorpio", "Thar", "KUV100"]),
    "Ford":       (1.0, ["EcoSport", "Endeavour", "Figo", "Aspire"]),
    "Renault":    (0.95,["Kwid", "Duster", "Triber"]),
    "Nissan":     (0.95,["Micra", "Terrano", "Kicks"]),
    "Chevrolet":  (0.9, ["Beat", "Cruze", "Spark"]),
    "Datsun":     (0.85,["GO", "GO+", "Redi-GO"]),
    "Fiat":       (0.9, ["Punto", "Linea"]),
    "Land":       (4.0, ["Rover Discovery", "Defender"]),
    "Force":      (1.2, ["Gurkha"]),
    "Hindustan":  (0.7, ["Ambassador"]),
}

FUEL_TYPES = ["Petrol", "Petrol", "Petrol", "Diesel", "Diesel", "Diesel", "Diesel", "LPG"]

def generate_price(company, multiplier, year, kms_driven, fuel_type):
    base = 280000
    age_dep = (2024 - year) * 17000
    km_dep  = kms_driven * 0.85
    fuel_add = 38000 if fuel_type == "Diesel" else (-8000 if fuel_type == "LPG" else 0)
    price = (base - age_dep - km_dep + fuel_add) * multiplier
    price = max(price, 40000)
    noise = random.gauss(0, price * 0.09)
    return max(int(price + noise), 25000)

rows = []
TARGET = 1060

company_list = list(COMPANIES.keys())
weights = [8 if COMPANIES[c][0] < 1.5 else (3 if COMPANIES[c][0] < 2.0 else 1) for c in company_list]

for _ in range(TARGET):
    company = random.choices(company_list, weights=weights, k=1)[0]
    multiplier, models = COMPANIES[company]
    model   = random.choice(models)
    name    = f"{company} {model} {'VXI' if random.random() > 0.5 else 'LXI' if random.random() > 0.5 else 'ZXI'}"

    # Year distribution
    r = random.random()
    if r < 0.60:
        year = random.randint(2012, 2019)
    elif r < 0.85:
        year = random.randint(2008, 2011)
    else:
        year = random.randint(2019, 2023)

    # KMs — inversely correlated with year
    avg_km  = max(5000, (2024 - year) * 12000 + random.gauss(0, 15000))
    kms_raw = max(3000, int(avg_km))

    fuel_type = random.choice(FUEL_TYPES)
    price     = generate_price(company, multiplier, year, kms_raw, fuel_type)

    rows.append({
        "name":       name,
        "company":    company,
        "year":       year,
        "Price":      price,
        "kms_driven": kms_raw,
        "fuel_type":  fuel_type,
    })

df = pd.DataFrame(rows)

# ── Inject intentional dirt ──────────────────
# 80 rows: kms_driven as "45,000 kms"
for i in range(80):
    df.at[i, "kms_driven"] = f"{df.at[i, 'kms_driven']:,} kms"

# 40 rows: Price as comma-string
for i in range(80, 120):
    p = df.at[i, "Price"]
    df.at[i, "Price"] = f"{p:,}"

# 30 rows: Price = "Ask For Price"
for i in range(120, 150):
    df.at[i, "Price"] = "Ask For Price"

# 20 rows: NaN fuel_type
df.loc[150:169, "fuel_type"] = None

# 15 rows: NaN kms_driven
df.loc[170:184, "kms_driven"] = None

# 10 rows: year as float string
for i in range(185, 195):
    df.at[i, "year"] = f"{df.at[i, 'year']}.0"

df.to_csv("quikr_car.csv", index=False)
print(f"✅ quikr_car.csv created — {len(df)} raw rows, 6 columns")
