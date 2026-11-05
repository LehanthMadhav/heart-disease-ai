
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "datasets" / "processed.cleveland.data"
REPORT_DIR = BASE_DIR / "reports"
MODEL_DIR = BASE_DIR / "models"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


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

print("\n========== DATASET LOADED ==========")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 3. SEPARATE FEATURES AND TARGET
# --------------------------------------------------

X = df.drop(columns=["num"])

# Binary classification:
# 0 = no disease label
# 1 = disease label (original values 1, 2, 3, 4)

y = (df["num"] > 0).astype(int)

print("\n========== TARGET DISTRIBUTION ==========")
print(y.value_counts().sort_index())

print("\nTarget percentages:")
print((y.value_counts(normalize=True) * 100).round(2))


# --------------------------------------------------
# 4. DEFINE FEATURE TYPES
# --------------------------------------------------

numeric_features = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]

categorical_features = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal"
]


# --------------------------------------------------
# 5. CREATE PREPROCESSING PIPELINES
# --------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features)
    ]
)


# --------------------------------------------------
# 6. SPLIT DATASET
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== DATASET SPLIT ==========")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining target distribution:")
print(y_train.value_counts().sort_index())

print("\nTesting target distribution:")
print(y_test.value_counts().sort_index())


# --------------------------------------------------
# 7. FIT ON TRAINING DATA ONLY
# --------------------------------------------------

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)

# Convert sparse matrices to regular arrays
if hasattr(X_train_processed, "toarray"):
    X_train_processed = X_train_processed.toarray()

if hasattr(X_test_processed, "toarray"):
    X_test_processed = X_test_processed.toarray()

print("\n========== PREPROCESSING ==========")
print("Training feature shape:", X_train_processed.shape)
print("Testing feature shape:", X_test_processed.shape)


# --------------------------------------------------
# 8. SAVE PREPROCESSOR
# --------------------------------------------------

preprocessor_path = MODEL_DIR / "preprocessor.joblib"

joblib.dump(preprocessor, preprocessor_path)


# --------------------------------------------------
# 9. SAVE PROCESSED DATA
# --------------------------------------------------

feature_names = preprocessor.get_feature_names_out()

X_train_df = pd.DataFrame(
    X_train_processed,
    columns=feature_names
)

X_test_df = pd.DataFrame(
    X_test_processed,
    columns=feature_names
)

X_train_df.to_csv(
    REPORT_DIR / "X_train_processed.csv",
    index=False
)

X_test_df.to_csv(
    REPORT_DIR / "X_test_processed.csv",
    index=False
)

y_train.to_csv(
    REPORT_DIR / "y_train.csv",
    index=False,
    header=["target"]
)

y_test.to_csv(
    REPORT_DIR / "y_test.csv",
    index=False,
    header=["target"]
)


# --------------------------------------------------
# 10. SAVE PREPROCESSING SUMMARY
# --------------------------------------------------

with open(REPORT_DIR / "preprocessing_summary.txt", "w") as file:

    file.write("HEART DISEASE DATA PREPROCESSING REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Original records: {len(df)}\n")
    file.write(f"Original features: {X.shape[1]}\n")

    file.write("\nMissing values before preprocessing:\n")
    file.write(X.isnull().sum().to_string())

    file.write("\n\nTraining records:\n")
    file.write(str(len(X_train)))

    file.write("\n\nTesting records:\n")
    file.write(str(len(X_test)))

    file.write("\n\nProcessed training shape:\n")
    file.write(str(X_train_processed.shape))

    file.write("\n\nProcessed testing shape:\n")
    file.write(str(X_test_processed.shape))

    file.write("\n\nBinary target distribution:\n")
    file.write(y.value_counts().sort_index().to_string())

    file.write("\n\nPreprocessing methods:\n")
    file.write("Numeric missing values: Median imputation\n")
    file.write("Numeric scaling: StandardScaler\n")
    file.write("Categorical missing values: Most frequent imputation\n")
    file.write("Categorical encoding: OneHotEncoder\n")
    file.write("Train-test split: 80:20\n")
    file.write("Random state: 42\n")


# --------------------------------------------------
# 11. FINAL STATUS
# --------------------------------------------------

print("\n========== PREPROCESSING COMPLETED ==========")

print("Missing values handled through fitted imputers.")
print("Categorical features encoded.")
print("Numerical features standardized.")
print("Training and testing datasets prepared.")

print("\nSaved preprocessor:")
print(preprocessor_path)

print("\nSaved reports:")
print(REPORT_DIR)

print("\nPHASE 3 COMPLETED SUCCESSFULLY!")
