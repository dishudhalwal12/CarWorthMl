# CarWorthML - Used Car Price Predictor

This is a machine learning web application that predicts the resale price of used cars in the Indian automobile market using a Gradient Boosting Regression model.

## How to Run This Project

Follow these steps to run the application on your local machine:

### 1. Prerequisites

Ensure you have **Python 3.10 or higher** installed on your computer.

### 2. Install Dependencies

Open your terminal (or command prompt), navigate to the project folder, and install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 3. Generate Data and Train the Model

This project requires generating the dataset, cleaning it, and training the ML model. We have provided a single setup script that does all of this automatically.

Run the following command:

```bash
python setup.py
```

_This script will:_

1. Generate `quikr_car.csv` (Raw Dataset)
2. Clean the data to produce `Cleaned_Car_data.csv`
3. Train the model to produce `LinearRegressionModel.pkl`

Wait until you see the `✅ Setup complete.` message.

### 4. Start the Application

Once the setup is successfully completed, you can launch the Streamlit web app by running:

```bash
streamlit run app.py
```

The app will open automatically in your default internet browser (usually at `http://localhost:8501`).

---

### Troubleshooting

- **Missing Files Error:** If the app complains about missing `.csv` or `.pkl` files, make sure you ran `python setup.py` successfully.
- **Port already in use:** If port 8501 is occupied, Streamlit will automatically pick the next available port (e.g., 8502, 8503). Look at your terminal output for the exact `Local URL`.
- **Invalid image width:** If you see any browser errors related to images, ensure you do not have aggressive ad-blockers (like Dishuflix-Blocker) interfering with the page.
