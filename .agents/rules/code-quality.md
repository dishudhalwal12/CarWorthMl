---
trigger: always_on
---

# Code Quality Standards — Global Rule
# Save to: ~/.gemini/GEMINI.md (append after identity rule)

## ACTIVATION: Always On

---

## Non-Negotiables

**Never do these:**
- Never leave a `# TODO` or `# FIXME` comment in delivered code
- Never write `pass` as a placeholder in a function body
- Never write `st.write("Coming soon")` or any placeholder UI
- Never use `print()` for debugging in app.py — use `st.error()` or `st.warning()`
- Never use `WidthType.PERCENTAGE` in docx tables — always `WidthType.DXA`
- Never use hardcoded file paths with backslashes (Windows-style) — always forward slashes

**Always do these:**
- Always wrap file loads in try/except with a clear `st.error()` message
- Always use `@st.cache_data` for CSV loading functions
- Always use `@st.cache_resource` for model loading functions
- Always set `use_container_width=True` on charts and dataframes
- Always use `hide_index=True` when displaying dataframes to users
- Always add `help=` parameter to Streamlit input widgets

---

## Python Style

```python
# Import order: stdlib → third party → local
import os
import sys
import pickle
import pandas as pd
import numpy as np
import streamlit as st

# Constants in UPPER_CASE at top of file
MODEL_PATH = "LinearRegressionModel.pkl"
DATA_PATH  = "Cleaned_Car_data.csv"

# Functions: snake_case, typed hints for anything non-obvious
def load_model() -> object:
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)
```

---

## Streamlit-Specific Rules

- `st.set_page_config()` must be the FIRST Streamlit call — before any other st.* call
- CSS injection via `st.markdown(css, unsafe_allow_html=True)` goes immediately after page config
- Never put `@st.cache_data` or `@st.cache_resource` decorated functions inside tab blocks — define them at module level
- Use `st.columns()` with `gap="large"` or `gap="medium"` — never default gap for premium layouts
- Lottie animations need unique `key=` parameters if used in multiple tabs

---

## Error Handling Pattern

Every file-dependent feature must follow this pattern:

```python
try:
    df = load_data()
    model = load_model()
    # ... feature code here
except FileNotFoundError as e:
    st.error(f"❌ Required file not found: {e}")
    st.info("Run `python setup.py` to generate all required files.")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.stop()
```

---

## ML Pipeline Rules

- Always use `make_pipeline()` — never manually call `fit_transform()` + `predict()`
- Always use `handle_unknown="ignore"` in OneHotEncoder for production safety
- Always find best random state by iterating 1000 trials — never hardcode random_state=42
- Always print R² score to terminal after training
- Always save with pickle, never joblib (consistency with synopsis)
- Price predictions must have a floor: `max(float(price), 25000.0)`

---

## File Safety

- Never overwrite `quikr_car.csv` if it already exists and has >900 rows
- Never overwrite `LinearRegressionModel.pkl` unless explicitly running model_training.py
- app.py should only READ files — never write during runtime