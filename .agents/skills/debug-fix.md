---
name: debug-fix
description: Diagnoses and fixes bugs in CarWorthML. Use when the app crashes, a prediction fails, a chart doesn't render, a white background appears, or any error shows in the Streamlit terminal. Given an error message or visual symptom, this skill identifies the root cause and provides the exact fix.
---

# Debug & Fix Skill — CarWorthML

## Step 1: Identify the Error Category

Read the error message or symptom and classify it:

| Symptom | Category |
|---------|----------|
| `streamlit run app.py` crashes immediately | Import or page config error |
| White background on any element | CSS specificity issue |
| Predict tab returns wrong price or crashes | Model/data mismatch |
| Chart renders with white background | Streamlit version conflict |
| "FileNotFoundError" in tab | Missing generated file |
| Tab loads blank (no content) | Indentation error in tab block |
| Lottie doesn't show | CDN timeout or wrong key |
| `st.balloons()` doesn't fire | `submitted` variable scoping issue |
| Model returns negative price | Missing price floor guard |

---

## Import Error at Startup

```
ImportError: cannot import name 'X' from 'streamlit'
```
Fix: Check `requirements.txt` version. Streamlit 1.32.0 is the pinned target.
Run: `pip install streamlit==1.32.0`

```
ModuleNotFoundError: No module named 'streamlit_lottie'
```
Fix: `pip install streamlit-lottie==0.0.5`

---

## Page Config Error

```
StreamlitAPIException: set_page_config() can only be called once per app
```
Cause: `st.set_page_config()` is not the first Streamlit call.
Fix: Move `st.set_page_config()` to line 1 of the Streamlit section, before all other `st.*` calls including `st.markdown()`.

---

## White Background Issues

If any element shows a white background when it should be dark:

```python
# Add this to the CSS injection block:
st.markdown("""
<style>
/* Force dark background on specific element */
.stMarkdown { background: transparent !important; }
[data-testid="stVerticalBlock"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)
```

For white chart backgrounds specifically:
```python
# Use st.bar_chart / st.line_chart — NOT st.pyplot()
# st.pyplot() always has white bg and cannot be easily overridden
```

---

## FileNotFoundError in Tab

```
FileNotFoundError: [Errno 2] No such file or directory: 'Cleaned_Car_data.csv'
```

This is the correct behavior — the try/except block catches it and shows an error card.
Fix for user: Run `python setup.py` or `python data_cleaning.py`.

If happening during development, confirm you're in the right directory:
```bash
ls -la  # should show quikr_car.csv, Cleaned_Car_data.csv, LinearRegressionModel.pkl
```

---

## Prediction Returns Absurd Value

**Symptom:** Price shows as ₹-50,000 or ₹500,00,00,000

Cause 1: Missing price floor guard.
Fix:
```python
price = model.predict(input_df)[0]
price = max(float(price), 25000.0)  # ADD THIS LINE
```

Cause 2: Input DataFrame column order is wrong.
Fix: Verify columns are EXACTLY `["name", "company", "year", "kms_driven", "fuel_type"]` in that order.

---

## Model Predict Crashes with ValueError

```
ValueError: could not convert string to float: 'Maruti Swift VXI'
```

Cause: Model was saved without the ColumnTransformer properly fitted.
Fix: Delete `LinearRegressionModel.pkl` and re-run `python model_training.py`.

---

## Dropdown Not Filtering

**Symptom:** Changing manufacturer doesn't update model dropdown.

Cause: Model dropdown is outside the `st.form()` block so it can dynamically update, but the variable reference is wrong.

Fix: The selectbox for model must reference the already-selected company:
```python
# This must be INSIDE st.form()
company = st.selectbox("Manufacturer", options=sorted(df["company"].unique()))
models_for_company = sorted(df[df["company"] == company]["name"].unique())
car_name = st.selectbox("Model", options=models_for_company)
```

Note: Inside `st.form()`, the dropdown updates happen when the form is submitted, not on change. This is expected Streamlit behavior with forms.

---

## Lottie Not Loading

**Symptom:** Lottie area is blank, no fallback emoji.

Cause 1: `LOTTIE_AVAILABLE` flag is False because import failed.
Fix:
```python
try:
    from streamlit_lottie import st_lottie
    lottie_data = load_lottie_url(LOTTIE_URL)
    LOTTIE_AVAILABLE = lottie_data is not None
except ImportError:
    LOTTIE_AVAILABLE = False
```

Cause 2: Unique `key=` not provided, causing conflict across tabs.
Fix: Every `st_lottie()` call must have a unique key:
```python
st_lottie(lottie_car, height=320, key="home_lottie")    # Tab 1
st_lottie(lottie_car, height=200, key="predict_lottie") # Tab 2
st_lottie(lottie_car, height=160, key="explain_lottie") # Tab 3
st_lottie(lottie_car, height=140, key="about_lottie")   # Tab 4
```

---

## Cached Function Defined Inside Tab Block

**Symptom:** Warning: `@st.cache_data` used inside a function defined in a tab block causes re-computation.

Fix: Move all `@st.cache_data` and `@st.cache_resource` functions to module level (outside any `with tab:` block).

```python
# WRONG — inside tab block
with tab2:
    @st.cache_data
    def load_data():
        return pd.read_csv("Cleaned_Car_data.csv")

# CORRECT — module level
@st.cache_data
def load_data():
    return pd.read_csv("Cleaned_Car_data.csv")

with tab2:
    df = load_data()
```

---

## R² Below 0.60 After Training

Possible causes (check in order):
1. Less than 700 rows in cleaned data → check `data_cleaning.py` isn't over-filtering
2. Price noise too high → reduce `random.gauss(0, price * 0.09)` to `0.06`
3. Price formula has a bug → verify age_dep and km_dep are subtracted, not added
4. Year range too wide → very old cars (pre-2000) with high kms create outliers

Quick diagnostic:
```python
import pandas as pd
df = pd.read_csv("Cleaned_Car_data.csv")
print(df.describe())
print(df["Price"].quantile([0.05, 0.25, 0.5, 0.75, 0.95]))
```

If the 5th percentile price is below ₹30,000 or the 95th percentile is above ₹80,00,000 — the data has outliers that are hurting the model.