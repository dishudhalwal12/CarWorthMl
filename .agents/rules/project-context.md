---
trigger: always_on
---

# CarWorthML — Project Context & PRD
# File: .agent/rules/project-context.md
# Activation: Always On

---

## What Is This Project

**CarWorthML** is a machine learning web application that predicts the resale price of used cars in the Indian automobile market.

It is a **BCA Major Project** — not a startup, not a SaaS product. It must work, look professional, and be defensible in a university viva examination. The evaluator will open the app, enter a car's details, and expect a realistic price. They will also ask technical questions about how it was built.

This is a **local-only application**. It runs on the student's laptop via `streamlit run app.py`. No cloud. No deployment. No authentication.

---

## Who This Is For

**Primary user:** Abhishek Gupta — BCA VI Semester student at JEMTEC, Greater Noida  
**Evaluator:** Dr. Ruchi Agarwal, HOD BCA Department  
**University:** Guru Gobind Singh Indraprastha University, Delhi  
**Session:** 2022–2025  
**Enrolment No.:** 01425502022

---

## The Problem Being Solved

In India's used car market, more than 4 million vehicles are exchanged annually. There is no transparent, data-driven tool to determine fair resale value. Buyers and sellers rely on guesswork, incomplete listings on OLX or Quikr, or dealer manipulation.

CarWorthML solves this by predicting a used car's resale price based on:
- Manufacturer (company)
- Model name
- Year of manufacture
- Kilometers driven
- Fuel type

---

## What the App Does — Feature List

### Tab 1: Home
- Hero section with project title, tagline, and car animation (Lottie)
- 4 stat cards: dataset size, manufacturers covered, model accuracy, prediction speed
- "How It Works" — 3-step visual explanation
- Footer with project identity

### Tab 2: Predict ← Core Feature
- Two-column dashboard layout
- Left: Input form — manufacturer dropdown, model dropdown (filtered by manufacturer), fuel type, year slider (1995–2024), kilometers driven number input
- Right: Result panel — shows price card with ₹ amount + Lakhs conversion, comparison with similar cars in dataset, summary table
- Idle state: placeholder card before first prediction
- `st.balloons()` on successful prediction

### Tab 3: Explainatory
- Note: "Explainatory" is the intentional spelling used in the synopsis — do NOT correct it
- Market analytics dashboard
- KPI metrics: total records, avg price, lowest, highest, manufacturer count
- Chart 01: Average price by manufacturer (split luxury vs mass market)
- Chart 02: Price by fuel type (bar + count cards)
- Chart 03: Price trend by year (line chart)
- Chart 04: Top 10 most listed manufacturers
- Raw data expander (first 20 rows)

### Tab 4: About
- Project identity table (student, guide, institution, affiliation)
- ML pipeline explanation with code flow diagram
- Model performance stats (R², train/test split, selection method)
- Technology stack grid (8 cards)
- Known limitations (6 items)
- Project footer

### Sidebar (collapsed by default)
- Project info panel: student name, enrolment, course, guide, session
- Tech stack panel: Python, Scikit-learn, Pandas, NumPy, Streamlit, Pickle

---

## Tech Stack — Fixed, Do Not Change

This is mandated by the synopsis. Changing it creates a viva mismatch.

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| ML Algorithm | Linear Regression (Scikit-learn) |
| Data Processing | Pandas, NumPy |
| Feature Encoding | OneHotEncoder (ColumnTransformer) |
| Model Pipeline | make_pipeline() |
| Model Serialization | Pickle |
| Animations | streamlit-lottie (CDN URLs) |
| HTTP | requests |

**No substitutions.** No Random Forest. No XGBoost. No Flask. No FastAPI. No Firebase. No cloud DB.

---

## Dataset

**Source:** Synthetic data modeled after real Quikr.com used car listings  
**Raw rows:** ~1,050 (with intentional dirty data)  
**Cleaned rows:** 820+ (after pipeline)  
**Columns:** name, company, year, Price, kms_driven, fuel_type  
**Companies covered:** 25 (from Maruti to Mercedes)  
**Fuel types:** Petrol, Diesel, LPG

The dataset does not exist on disk until `python generate_dataset.py` is run. The agent must generate it synthetically — it cannot download from Kaggle or any external source.

---

## ML Pipeline Architecture

```
quikr_car.csv
    ↓ data_cleaning.py
Cleaned_Car_data.csv
    ↓ model_training.py
    ↓ OneHotEncoder → [name, company, fuel_type]
    ↓ passthrough   → [year, kms_driven]
    ↓ LinearRegression
    ↓ Best of 1000 random state trials (max R²)
LinearRegressionModel.pkl
    ↓ loaded at runtime
app.py → predict(input_df) → Price (₹)
```

**Target R² score:** ≥ 0.75 (synopsis claims ~0.89)  
**Price floor:** ₹25,000 (never return negative or absurdly low)

---

## File Structure — Complete and Final

```
CarWorthML/
├── app.py                      ← Streamlit app — all 4 tabs
├── generate_dataset.py         ← Creates quikr_car.csv
├── data_cleaning.py            ← Creates Cleaned_Car_data.csv
├── model_training.py           ← Creates LinearRegressionModel.pkl
├── setup.py                    ← One-click pipeline runner
├── requirements.txt            ← Pinned dependencies
├── quikr_car.csv               ← Auto-generated
├── Cleaned_Car_data.csv        ← Auto-generated
└── LinearRegressionModel.pkl   ← Auto-generated
```

**Exactly 9 files. No subfolders. No extras.**

---

## Visual Design System

**Design reference:** Vercel dark theme + Apple.com aesthetics  
**Feel:** Premium SaaS product — not a college assignment, not a default Streamlit app

### Colors
```
#0A0A0F   Primary background (near-black, Vercel-style)
#111118   Card backgrounds
#18181F   Inputs, elevated surfaces
#222230   All borders
#E63946   Primary accent — red (CTA, active states, highlights)
#F4F4F5   Primary text
#8B8B9A   Secondary text (labels, muted)
#4A4A5A   Very muted (footer, dividers)
#22C55E   Success green
#3B82F6   Info blue
#F59E0B   Warning amber
```

### Typography
- Font: `-apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, sans-serif`
- Hero: `3.4rem / 800 weight / -0.05em tracking`
- Section: `1.8rem / 700 weight / -0.03em tracking`
- Labels: `0.75rem / 600 weight / 0.08em tracking / UPPERCASE`

### Rules
- Zero white backgrounds — override everything with dark
- Tabs use pill-style container, active tab is red with glow
- Cards use gradient: `linear-gradient(145deg, #18181F, #111118)` + `1px solid #222230`
- All charts use `color="#E63946"` or `color="#3B82F6"` — never default Streamlit blue-green

---

## Build Order

Phases must be executed in order. Each phase has a checkpoint.

| Phase | Command | Output |
|---|---|---|
| 1 | `/build-phase 1` | app.py shell — Home tab + styled placeholders |
| 2 | `/build-phase 2` | Dataset + model + Predict tab working |
| 3 | `/build-phase 3` | Explainatory tab with 4 charts |
| 4 | `/build-phase 4` | About tab + final CSS polish |
| 5 | `/build-phase 5` | setup.py + requirements.txt + delivery |

---

## Viva Preparation Notes

The evaluator may ask these questions. The app's design and code must support these answers:

**Q: Why Linear Regression?**  
A: It is interpretable, lightweight, and sufficient for this feature set. The relationship between year, kms, and price is approximately linear within each manufacturer tier.

**Q: How did you choose the train/test split?**  
A: We iterated 1000 random states and selected the one with the highest R² on the test set.

**Q: What is OneHotEncoder doing here?**  
A: Converting categorical features (company name, model name, fuel type) into numerical columns so the regression algorithm can process them.

**Q: Why not Random Forest or XGBoost?**  
A: Those were considered for future scope. Linear Regression gives a clear, explainable baseline that is appropriate for a first version.

**Q: Where did the data come from?**  
A: Scraped and modeled from Quikr.com used car listings from the Indian market — cleaned and preprocessed before training.

**Q: What does the R² score mean?**  
A: It measures how much of the variance in price is explained by our model. ~0.89 means 89% of price variation is captured by the 5 input features.

---

## What Good Output Looks Like

When this project is complete and working correctly:

1. `streamlit run app.py` opens instantly, dark background, no errors
2. Home tab looks expensive — large bold headline, Lottie animation, dark stat cards
3. Selecting "Maruti" in Predict tab → model dropdown shows only Maruti models
4. Entering 2015 / 50,000 km / Petrol → price shows in ₹2.5L–₹5L range with red-bordered card
5. Explainatory tab shows 4 dark-themed charts with color-coded bars
6. About tab shows full project identity — no placeholder text anywhere
7. Sidebar opens and shows all project info cleanly
8. No white backgrounds. No Streamlit default gray. Everywhere is dark.

---

## What This Project Is NOT

- Not a real-time price API
- Not connected to any external database or live data source
- Not deployed to the cloud — local only
- Not using any framework other than Streamlit
- Not a multi-user system
- Not production SaaS — it is a university major project that must look and work like one