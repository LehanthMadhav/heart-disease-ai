
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Dataset location
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR / "datasets" / "processed.cleveland.data"
)

# --------------------------------------------------
# 2. Cleveland dataset column names
# --------------------------------------------------

columns = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "num"
]

# --------------------------------------------------
# 3. Load dataset
# --------------------------------------------------

print("\n========== HEART DISEASE DATASET ==========\n")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

df = pd.read_csv(
    DATASET_PATH,
    header=None,
    names=columns,
    na_values=["?", " ?"],
    skipinitialspace=True
)

# --------------------------------------------------
# 4. Basic dataset information
# --------------------------------------------------

print("1. DATASET SHAPE")
print(df.shape)

print("\n2. FIRST FIVE RECORDS")
print(df.head())

print("\n3. DATASET INFORMATION")
df.info()

# --------------------------------------------------
# 5. Missing value analysis
# --------------------------------------------------

print("\n4. MISSING VALUES")
print(df.isnull().sum())

print("\nTOTAL MISSING VALUES:")
print(df.isnull().sum().sum())

# --------------------------------------------------
# 6. Statistical summary
# --------------------------------------------------

print("\n5. STATISTICAL SUMMARY")
print(df.describe())

# --------------------------------------------------
# 7. Target distribution
# --------------------------------------------------

print("\n6. ORIGINAL TARGET DISTRIBUTION")
print(df["num"].value_counts(dropna=False).sort_index())

print("\n7. BINARY TARGET DISTRIBUTION")

binary_target = df["num"].map(
    lambda value: 0 if value == 0 else 1
    if pd.notna(value) else pd.NA
)

print(binary_target.value_counts(dropna=False).sort_index())

# --------------------------------------------------
# 8. Data type verification
# --------------------------------------------------

print("\n8. COLUMN DATA TYPES")
print(df.dtypes)

# --------------------------------------------------
# 9. Duplicate record check
# --------------------------------------------------

print("\n9. DUPLICATE RECORDS")
print(df.duplicated().sum())

print("\n========== INSPECTION COMPLETED ==========\n")
