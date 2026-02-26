import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score

car = pd.read_csv("Cleaned_Car_data.csv")

# Remove top 1% price outliers (luxury cars distort the model)
price_cap = car["Price"].quantile(0.99)
car = car[car["Price"] <= price_cap].copy()
print(f"Training on {len(car)} rows (after removing top-1% outliers)")

X = car[["name", "company", "year", "kms_driven", "fuel_type"]]
y_log = np.log(car["Price"])   # log-transform: better for multiplicative depreciation

# Fit OHE on full data to capture all categories
ohe = OneHotEncoder()
ohe.fit(X[["name", "company", "fuel_type"]])

column_trans = make_column_transformer(
    (
        OneHotEncoder(categories=ohe.categories_, handle_unknown="ignore"),
        ["name", "company", "fuel_type"],
    ),
    remainder="passthrough",
)

# GradientBoosting captures non-linear depreciation curves
gbr = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.08,
    max_depth=4,
    subsample=0.85,
    random_state=42,
)

pipe = make_pipeline(column_trans, gbr)

# Cross-validation on log-price
print("Running 5-fold cross-validation...")
cv_scores = cross_val_score(pipe, X, y_log, cv=5, scoring="r2", n_jobs=-1)
print(f"CV R² (log-price): {cv_scores.round(3)}")
print(f"Mean CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Final model on full dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y_log, test_size=0.1, random_state=42
)
pipe.fit(X_train, y_train)
test_r2 = r2_score(y_test, pipe.predict(X_test))
print(f"Hold-out test R² (log-price): {test_r2:.4f}")

# Verify predictions are realistic (exponentiate back)
sample_preds = np.exp(pipe.predict(X_test[:5]))
sample_actuals = np.exp(y_test[:5].values)
print("\nSample predictions vs actuals (₹):")
for p, a in zip(sample_preds, sample_actuals):
    print(f"  Predicted: ₹{p:,.0f}  |  Actual: ₹{a:,.0f}")

with open("LinearRegressionModel.pkl", "wb") as f:
    pickle.dump(pipe, f)

# Save the log-transform flag so app.py knows
with open("model_meta.pkl", "wb") as f:
    pickle.dump({"log_transform": True}, f)

print(f"\n✅ Model saved (GradientBoosting on log-price)")
print(f"   Note: model.predict() returns log(price); use np.exp() to get ₹")
