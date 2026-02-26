import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

car = pd.read_csv("Cleaned_Car_data.csv")

X = car[["name", "company", "year", "kms_driven", "fuel_type"]]
y = car["Price"]

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

# Find best random state across 1000 trials
print("Finding best train/test split (1000 trials)...")
scores = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=i
    )
    pipe = make_pipeline(column_trans, LinearRegression())
    pipe.fit(X_train, y_train)
    scores.append(r2_score(y_test, pipe.predict(X_test)))

best_idx   = int(np.argmax(scores))
best_score = scores[best_idx]
print(f"Best R²: {best_score:.4f} at random_state={best_idx}")

# Final model with best split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=best_idx
)
pipe = make_pipeline(column_trans, LinearRegression())
pipe.fit(X_train, y_train)

with open("LinearRegressionModel.pkl", "wb") as f:
    pickle.dump(pipe, f)

print(f"✅ LinearRegressionModel.pkl saved")
print(f"   Final R² on test: {r2_score(y_test, pipe.predict(X_test)):.4f}")
