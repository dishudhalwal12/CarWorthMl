# CarWorthML - Used Car Price Predictor

CarWorthML is a Streamlit-based machine learning app that predicts the resale price of used cars in the Indian market. The current version uses a real-data pipeline built from a Kaggle used-car dataset plus the local `car data.csv` file, then trains a stronger model before serving predictions in the web app.

## What happens in setup

When you run the setup/training pipeline, the project will:

1. Download the latest Kaggle used-car dataset.
2. Merge that data with `car data.csv`.
3. Clean and standardize both datasets.
4. Train the ML model.
5. Save the final files needed by the app.

Important output files:

- `Cleaned_Car_data.csv`
- `LinearRegressionModel.pkl`
- `model_meta.pkl`

## First-time installation on a laptop

### 1. Install Python

Make sure Python `3.9` or above is installed.

Check it with:

```bash
python3 --version
```

If `python3` does not work, try:

```bash
python --version
```

### 2. Open the project folder

Open Terminal and go to the project folder:

```bash
cd /path/to/car2
```

Example:

```bash
cd ~/Desktop/car2
```

### 3. Create a virtual environment

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate
```

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

After activation, your terminal should show `(venv)` at the beginning.

### 4. Install requirements

Install all required packages:

```bash
pip install -r requirements.txt
```

## First-time setup and model training

Run the full pipeline:

```bash
python setup.py
```

If your laptop uses `python3`, run:

```bash
python3 setup.py
```

This command will automatically:

1. Download the Kaggle dataset.
2. Create the cleaned dataset.
3. Train the prediction model.

Wait until the setup finishes successfully.

## Run the app on localhost

Start the Streamlit app with:

```bash
streamlit run app.py
```

Or, if needed:

```bash
python -m streamlit run app.py
```

After that, open the local URL shown in Terminal. Usually it is:

```text
http://localhost:8501
```

## If someone installs the project for the first time

Use these commands in order:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py
streamlit run app.py
```

## How to retrain the model later

If you change the dataset or want to train again, run:

```bash
python data_cleaning.py
python model_training.py
```

Or rerun the complete pipeline:

```bash
python setup.py
```

## Project files

- `app.py` - Streamlit web app
- `generate_dataset.py` - downloads the Kaggle dataset
- `data_cleaning.py` - cleans and merges the raw data
- `model_training.py` - trains the machine learning model
- `setup.py` - runs the full pipeline in one command
- `requirements.txt` - Python dependencies

## Troubleshooting

### `python` command not found

Use `python3` instead of `python`.

### `pip` install fails

Make sure the virtual environment is activated before running:

```bash
pip install -r requirements.txt
```

### Streamlit app does not start

Try:

```bash
python -m streamlit run app.py
```

### Model file or dataset file missing

Run the setup again:

```bash
python setup.py
```

### Port 8501 already in use

Streamlit may automatically move to another port such as `8502` or `8503`. Check the Terminal output and open that URL instead.

### Kaggle dataset download issue

The setup uses `kagglehub` and needs internet access. If the download fails, check your connection and run the setup again.
