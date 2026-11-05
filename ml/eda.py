
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "datasets" / "processed.cleveland.data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "num"
]

df = pd.read_csv(
    DATASET_PATH,
    header=None,
    names=columns,
    na_values="?"
)

print("\n========== DATASET OVERVIEW ==========")
print("Dataset shape:", df.shape)
print("\nFirst five records:")
print(df.head())

# --------------------------------------------------
# 3. DATA QUALITY ANALYSIS
# --------------------------------------------------

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")
print("Duplicates:", df.duplicated().sum())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

# --------------------------------------------------
# 4. TARGET DISTRIBUTION
# --------------------------------------------------

print("\n========== ORIGINAL TARGET DISTRIBUTION ==========")
print(df["num"].value_counts().sort_index())

df["target"] = (df["num"] > 0).astype(int)

print("\n========== BINARY TARGET DISTRIBUTION ==========")
print(df["target"].value_counts().sort_index())

print("\nTarget percentages:")
print(df["target"].value_counts(normalize=True) * 100)

# --------------------------------------------------
# 5. STATISTICAL SUMMARY
# --------------------------------------------------

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe().round(2))

# --------------------------------------------------
# 6. TARGET DISTRIBUTION GRAPH
# --------------------------------------------------

sns.set_theme(style="whitegrid")

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="target")

plt.title("Heart Disease Target Distribution")
plt.xlabel("Target (0 = No disease, 1 = Disease)")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.savefig(REPORT_DIR / "target_distribution.png", dpi=300)
plt.show()

# --------------------------------------------------
# 7. AGE DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="age", bins=20, kde=True)

plt.title("Patient Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Patients")

plt.tight_layout()
plt.savefig(REPORT_DIR / "age_distribution.png", dpi=300)
plt.show()

# --------------------------------------------------
# 8. CORRELATION HEATMAP
# --------------------------------------------------

correlation = df.drop(columns=["num"]).corr()

plt.figure(figsize=(12, 9))
sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Clinical Features Correlation Heatmap")
plt.tight_layout()
plt.savefig(REPORT_DIR / "correlation_heatmap.png", dpi=300)
plt.show()

# --------------------------------------------------
# 9. SAVE DATA QUALITY REPORT
# --------------------------------------------------

with open(REPORT_DIR / "eda_summary.txt", "w") as file:
    file.write("HEART DISEASE DATASET - EDA SUMMARY\n")
    file.write("=" * 45 + "\n\n")
    file.write(f"Dataset shape: {df.shape}\n\n")
    file.write("Missing values:\n")
    file.write(df.isnull().sum().to_string())
    file.write("\n\nDuplicate records:\n")
    file.write(str(df.duplicated().sum()))
    file.write("\n\nBinary target distribution:\n")
    file.write(df["target"].value_counts().sort_index().to_string())
    file.write("\n\nStatistical summary:\n")
    file.write(df.describe().to_string())

print("\nEDA COMPLETED SUCCESSFULLY!")
print("Reports saved inside:", REPORT_DIR)
