import subprocess
import sys
import os

def run(script, label):
    print(f"\n{'─'*50}")
    print(f"  {label}")
    print(f"{'─'*50}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"\n❌ FAILED: {script}")
        sys.exit(1)

def check(path, label):
    exists = os.path.exists(path)
    size   = os.path.getsize(path) if exists else 0
    status = f"✅  {label:35s} {size:>10,} bytes" if exists else f"❌  {label:35s} NOT FOUND"
    print(status)
    return exists

print("\n" + "═"*50)
print("  CarWorthML — Setup Pipeline")
print("═"*50)

run("generate_dataset.py", "Step 1/3  →  Generating dataset")
run("data_cleaning.py",    "Step 2/3  →  Cleaning data")
run("model_training.py",   "Step 3/3  →  Training model (~30 sec)")

print(f"\n{'─'*50}")
print("  File Verification")
print(f"{'─'*50}")

all_ok = True
all_ok &= check("quikr_car.csv",              "Raw dataset")
all_ok &= check("Cleaned_Car_data.csv",        "Cleaned dataset")
all_ok &= check("LinearRegressionModel.pkl",   "ML model")
all_ok &= check("app.py",                      "Streamlit app")
all_ok &= check("requirements.txt",            "Requirements file")

print(f"\n{'═'*50}")
if all_ok:
    print("  ✅  Setup complete.\n")
    print("  Run the app:")
    print("      streamlit run app.py\n")
else:
    print("  ❌  Setup incomplete. Check errors above.\n")
print("═"*50 + "\n")
