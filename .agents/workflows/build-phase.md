---
description: Executes one phase of the CarWorthML project build. Pass the phase number (1–5) as argument. Each phase has a built-in checkpoint — do not proceed unless checkpoint passes.
---

# CarWorthML Build Workflow
# Save to: .agent/workflows/build-phase.md
# Invoke with: /build-phase

---

title: CarWorthML Phase Build
description: Executes one phase of the CarWorthML project build. Pass the phase number (1–5) as argument. Each phase has a built-in checkpoint — do not proceed unless checkpoint passes.

---

## How to Use

```
/build-phase 1    ← Frontend shell + Home tab
/build-phase 2    ← Dataset + Model + Predict tab
/build-phase 3    ← Explainatory tab (charts)
/build-phase 4    ← About tab + final CSS polish
/build-phase 5    ← Setup orchestrator + delivery
```

Do not skip phases. Each phase depends on the previous one being complete and verified.

---

## Phase 1 — Frontend Shell

### Goal
Build app.py with premium dark UI, Home tab fully designed, other tabs as styled placeholders.

### Steps
1. Install dependencies: `pip install streamlit streamlit-lottie requests`
2. Create `app.py` with:
   - `st.set_page_config()` as the very first call
   - Full GLOBAL_CSS injected immediately after
   - All helper functions defined: `card()`, `badge()`, `section_header()`, `stat_card()`, `price_result_card()`
   - Sidebar with project info and tech stack panels
   - Tab 1 (Home): Hero section, stat cards, how-it-works cards, footer
   - Tabs 2, 3, 4: Styled placeholder cards only — no placeholder text
3. Run: `streamlit run app.py`

### Checkpoint — ALL must pass before Phase 2
- [ ] App opens at http://localhost:8501 with zero terminal errors
- [ ] Background is `#0A0A0F` — NOT Streamlit's default gray
- [ ] Tab navigation shows pill-style container, active tab is red with glow
- [ ] Sidebar opens and shows project info correctly
- [ ] Hero headline renders at large size with red gradient on "True Value."
- [ ] Lottie car animation loads (or emoji fallback shows cleanly)
- [ ] Four stat cards visible with dark borders
- [ ] How It Works section shows 3 numbered step cards
- [ ] No white boxes anywhere in any tab
- [ ] Scrollbar is thin and dark

**If any checkpoint fails → fix it before calling /build-phase 2**

---

## Phase 2 — Dataset, Model, Predict Tab

### Goal
Generate data, train model, build the working Predict tab.

### Steps
1. Create `generate_dataset.py` — generates `quikr_car.csv` with 1,050 rows
2. Create `data_cleaning.py` — cleans to `Cleaned_Car_data.csv` (820+ rows)
3. Create `model_training.py` — trains and saves `LinearRegressionModel.pkl`
4. Run in order:
   ```bash
   python generate_dataset.py
   python data_cleaning.py
   python model_training.py
   ```
5. Replace Tab 2 placeholder in app.py with full predict form (two-column layout)
6. Add `import pickle` and `import pandas as pd` at top of app.py if not present

### Checkpoint — ALL must pass before Phase 3
- [ ] `quikr_car.csv` exists with 1,000+ rows
- [ ] `Cleaned_Car_data.csv` exists with 820+ rows, zero NaN values
- [ ] Terminal shows R² ≥ 0.75 after model training
- [ ] `LinearRegressionModel.pkl` exists
- [ ] Predict tab: manufacturer dropdown shows 25 brands
- [ ] Predict tab: model dropdown filters when manufacturer changes
- [ ] Predict tab: submitting form shows price card with red border glow
- [ ] Price card shows both ₹ amount and Lakhs conversion
- [ ] `st.balloons()` fires on successful prediction
- [ ] Idle state (before predict) shows placeholder card, not blank space
- [ ] No white backgrounds in Tab 2

**If any checkpoint fails → fix it before calling /build-phase 3**

---

## Phase 3 — Explainatory Tab

### Goal
Build the market analytics dashboard in Tab 3.

### Steps
1. Replace Tab 3 placeholder in app.py with full analytics content
2. Load `Cleaned_Car_data.csv` via `@st.cache_data` decorated function
3. Build all 4 charts + KPI metrics + fuel type cards + raw data toggle

### Checkpoint — ALL must pass before Phase 4
- [ ] Tab 3 loads without terminal errors
- [ ] 5 KPI metrics show at top (Total Records, Avg Price, Lowest, Highest, Manufacturers)
- [ ] Chart 01: Two-column bar charts (Luxury vs Mass market) — both render with colors
- [ ] Chart 02: Fuel type bar chart + fuel count cards with colored dots side by side
- [ ] Chart 03: Line chart — year vs avg price — upward trend visible
- [ ] Chart 04: Top 10 manufacturers bar chart
- [ ] Raw data expander works
- [ ] No white chart backgrounds
- [ ] Lottie or emoji fallback shows in header

**If any checkpoint fails → fix it before calling /build-phase 4**

---

## Phase 4 — About Tab + Final Polish

### Goal
Build the About tab and apply polish across the full app.

### Steps
1. Replace Tab 4 placeholder in app.py with full About content
2. Add second CSS polish block after the global CSS injection
3. Full visual review of all 4 tabs

### Checkpoint — ALL must pass before Phase 5
- [ ] About tab: two-column project identity table renders
- [ ] About tab: pipeline diagram code block visible
- [ ] About tab: 8 tech stack cards in 2 rows of 4
- [ ] About tab: 6 limitation cards with red left border
- [ ] About tab: footer shows project info
- [ ] Dataframe headers are uppercase with muted color (not default bold)
- [ ] Metric delta values are green
- [ ] Expander headers are dark-styled
- [ ] Active tab has no underline
- [ ] Full checklist review: all 4 tabs, sidebar, no white anywhere

**If any checkpoint fails → fix it before calling /build-phase 5**

---

## Phase 5 — Setup + Delivery

### Goal
Create requirements.txt, setup.py, run end-to-end test, prepare for handoff.

### Steps
1. Create `requirements.txt` with exact pinned versions
2. Create `setup.py` that runs all 3 pipeline scripts and verifies output
3. Run full test:
   ```bash
   pip install -r requirements.txt
   python setup.py
   streamlit run app.py
   ```
4. Perform 3 manual price prediction tests (Maruti mid-range, BMW luxury, Datsun budget)
5. Confirm folder contains exactly 9 files (no extras)

### Final Delivery Checkpoint
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `python setup.py` prints all ✅ green
- [ ] App opens cleanly after fresh setup
- [ ] Maruti Swift 2015 50k km → ₹2.5L–₹5L range ✓
- [ ] BMW 5 Series 2018 40k km → ₹15L–₹35L range ✓
- [ ] Datsun GO 2012 90k km → ₹80k–₹2L range ✓
- [ ] Folder has exactly: app.py, generate_dataset.py, data_cleaning.py, model_training.py, setup.py, requirements.txt, quikr_car.csv, Cleaned_Car_data.csv, LinearRegressionModel.pkl
- [ ] No stray files, no __pycache__ in delivery

**Project is complete when this checklist passes entirely.**