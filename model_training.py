import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_percentage_error, median_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


REPO_DIR = Path(__file__).resolve().parent
DATA_FILE = REPO_DIR / "Cleaned_Car_data.csv"
MODEL_FILE = REPO_DIR / "LinearRegressionModel.pkl"
META_FILE = REPO_DIR / "model_meta.pkl"

FEATURE_COLUMNS = [
    "name",
    "company",
    "year",
    "age",
    "kms_driven",
    "fuel_type",
    "transmission",
    "owner",
]
CATBOOST_COLUMNS = ["name", "company", "fuel_type", "transmission", "owner"]
NUMERIC_COLUMNS = ["year", "age", "kms_driven"]


def build_tree_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATBOOST_COLUMNS,
            ),
            (
                "num",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                NUMERIC_COLUMNS,
            ),
        ]
    )

    model = ExtraTreesRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=1,
        min_samples_leaf=1,
    )

    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def build_catboost_model() -> CatBoostRegressor:
    return CatBoostRegressor(
        loss_function="RMSE",
        depth=8,
        learning_rate=0.05,
        iterations=700,
        l2_leaf_reg=5,
        random_seed=42,
        verbose=False,
    )


def evaluate_predictions(actual_price: pd.Series, predicted_price: np.ndarray) -> dict:
    return {
        "r2_price": float(r2_score(actual_price, predicted_price)),
        "mape": float(mean_absolute_percentage_error(actual_price, predicted_price)),
        "median_abs_error": float(median_absolute_error(actual_price, predicted_price)),
    }


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError("Cleaned_Car_data.csv not found. Run data_cleaning.py first.")

    car_df = pd.read_csv(DATA_FILE)
    car_df = car_df.dropna(subset=FEATURE_COLUMNS + ["Price"]).copy()

    X = car_df[FEATURE_COLUMNS].copy()
    y_price = car_df["Price"].astype(float)
    y_log = np.log1p(y_price)

    X_train, X_test, y_train, y_test, price_train, price_test = train_test_split(
        X,
        y_log,
        y_price,
        test_size=0.2,
        random_state=42,
    )

    print(f"Training rows: {len(car_df)}")
    print(f"Brands: {car_df['company'].nunique()} | Models: {car_df['name'].nunique()}")

    extra_trees = build_tree_pipeline()
    extra_trees.fit(X_train, y_train)
    extra_pred_log = extra_trees.predict(X_test)
    extra_pred_price = np.expm1(extra_pred_log)
    extra_metrics = evaluate_predictions(price_test, extra_pred_price)
    extra_metrics["r2_log"] = float(r2_score(y_test, extra_pred_log))

    catboost = build_catboost_model()
    catboost.fit(
        X_train,
        y_train,
        cat_features=CATBOOST_COLUMNS,
    )
    cat_pred_log = catboost.predict(X_test)
    cat_pred_price = np.expm1(cat_pred_log)
    cat_metrics = evaluate_predictions(price_test, cat_pred_price)
    cat_metrics["r2_log"] = float(r2_score(y_test, cat_pred_log))

    print(f"ExtraTrees holdout metrics: {extra_metrics}")
    print(f"CatBoost holdout metrics: {cat_metrics}")

    if cat_metrics["r2_log"] >= extra_metrics["r2_log"]:
        best_model = catboost
        best_metrics = cat_metrics
        model_name = "CatBoostRegressor"
    else:
        best_model = extra_trees
        best_metrics = extra_metrics
        model_name = "ExtraTreesRegressor"

    if model_name == "CatBoostRegressor":
        best_model.fit(X, y_log, cat_features=CATBOOST_COLUMNS)
    else:
        best_model.fit(X, y_log)

    with open(MODEL_FILE, "wb") as model_file:
        pickle.dump(best_model, model_file)

    metadata = {
        "log_transform": True,
        "model_type": model_name,
        "feature_columns": FEATURE_COLUMNS,
        "categorical_features": CATBOOST_COLUMNS,
        "numeric_features": NUMERIC_COLUMNS,
        "training_rows": int(len(car_df)),
        "metrics": {
            "extra_trees": extra_metrics,
            "catboost": cat_metrics,
            "selected_model": best_metrics,
        },
    }

    with open(META_FILE, "wb") as meta_file:
        pickle.dump(metadata, meta_file)

    print(f"Selected model: {model_name}")
    print(
        "Selected holdout performance: "
        f"R²(log)={best_metrics['r2_log']:.4f}, "
        f"MAPE={best_metrics['mape']:.4f}, "
        f"Median AE=₹{best_metrics['median_abs_error']:,.0f}"
    )


if __name__ == "__main__":
    main()
