---
trigger: always_on
---

# CarWorthML File Structure — Workspace Rule
# Save to: .agent/rules/file-structure.md

## ACTIVATION: Always On

---

## Canonical File Structure

```
CarWorthML/
├── app.py                      ← MAIN FILE. All 4 tabs live here.
├── generate_dataset.py         ← Creates quikr_car.csv
├── data_cleaning.py            ← Reads quikr_car.csv → Cleaned_Car_data.csv
├── model_training.py           ← Reads Cleaned_Car_data.csv → LinearRegressionModel.pkl
├── setup.py                    ← Runs all 3 scripts in order, verifies output
├── requirements.txt            ← Python dependencies
├── quikr_car.csv               ← AUTO-GENERATED. Do not edit manually.
├── Cleaned_Car_data.csv        ← AUTO-GENERATED. Do not edit manually.
└── LinearRegressionModel.pkl   ← AUTO-GENERATED. Do not edit manually.
```

**No other files should be created.** No subfolders. No utils.py. No config.py. No .env.

---

## File Responsibilities — Hard Boundaries

### app.py
- Contains: page config, CSS injection, sidebar, all 4 tab definitions
- Contains: helper functions (card, badge, section_header, stat_card, price_result_card)
- Contains: load_data() and load_model() cached functions
- Does NOT contain: any data generation logic
- Does NOT contain: any model training logic
- Does NOT write any files at runtime

### generate_dataset.py
- Produces exactly: `quikr_car.csv` with ~1,050 raw rows
- Has intentional dirty data (Ask For Price, comma strings, NaN fuel types)
- Standalone — runnable as `python generate_dataset.py`

### data_cleaning.py
- Reads: `quikr_car.csv`
- Produces: `Cleaned_Car_data.csv` with 820+ clean rows
- Standalone — runnable as `python data_cleaning.py`

### model_training.py
- Reads: `Cleaned_Car_data.csv`
- Produces: `LinearRegressionModel.pkl`
- Iterates 1000 random states to find best split
- Prints R² to terminal
- Standalone — runnable as `python model_training.py`

---

## What to Edit vs What to Leave Alone

| Situation | Action |
|-----------|--------|
| Changing UI text or colors | Edit app.py only |
| Fixing prediction logic | Edit app.py Tab 2 block only |
| Changing chart types | Edit app.py Tab 3 block only |
| Fixing dataset generation | Edit generate_dataset.py only |
| Improving model accuracy | Edit model_training.py → re-run it → new pkl |
| Adding a dependency | Add to requirements.txt |

Never refactor across multiple files in one step — change one file, verify, then proceed.

---

## CSV Column Schema — Do Not Alter

```
Cleaned_Car_data.csv columns (exact, in order):
  name         : str   — e.g. "Maruti Swift VXI"
  company      : str   — e.g. "Maruti"
  year         : int   — e.g. 2015
  Price        : int   — e.g. 350000
  kms_driven   : int   — e.g. 45000
  fuel_type    : str   — "Petrol" | "Diesel" | "LPG"
```

The model was trained on these exact columns in this exact order. Changing column names breaks predictions.

---

## Model Input Schema

```python
# Prediction input must always be this exact DataFrame:
input_df = pd.DataFrame(
    [[car_name, company, year, kms_driven, fuel_type]],
    columns=["name", "company", "year", "kms_driven", "fuel_type"]
)
price = model.predict(input_df)[0]
```

Column order matters. Do not change it.