
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import StratifiedKFold, cross_val_score

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

REPORT_DIR = BASE_DIR / "reports"
MODEL_DIR = BASE_DIR / "models"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD PREPROCESSED DATA
# --------------------------------------------------

print("\n========== LOADING PREPROCESSED DATA ==========")

X_train = pd.read_csv(REPORT_DIR / "X_train_processed.csv")
X_test = pd.read_csv(REPORT_DIR / "X_test_processed.csv")

y_train = pd.read_csv(REPORT_DIR / "y_train.csv").iloc[:, 0]
y_test = pd.read_csv(REPORT_DIR / "y_test.csv").iloc[:, 0]

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)

print("Training labels:", y_train.shape)
print("Testing labels:", y_test.shape)

if X_train.isnull().any().any() or X_test.isnull().any().any():
    raise ValueError("Missing values found in processed features.")

if set(y_train.unique()) != {0, 1}:
    raise ValueError("Training target must contain both classes 0 and 1.")


# --------------------------------------------------
# 3. DEFINE MACHINE LEARNING MODELS
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}


# --------------------------------------------------
# 4. CROSS-VALIDATION
# --------------------------------------------------

print("\n========== CROSS-VALIDATION ==========")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_results = []

for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    )

    mean_score = scores.mean()
    std_score = scores.std()

    cv_results.append({
        "Model": name,
        "Mean CV ROC-AUC": mean_score,
        "CV Standard Deviation": std_score
    })

    print(f"\n{name}")
    print("ROC-AUC scores:", np.round(scores, 4))
    print(f"Mean ROC-AUC: {mean_score:.4f}")
    print(f"Standard deviation: {std_score:.4f}")


# --------------------------------------------------
# 5. SELECT MODEL USING TRAINING CV RESULTS
# --------------------------------------------------

cv_df = pd.DataFrame(cv_results)

cv_df = cv_df.sort_values(
    by="Mean CV ROC-AUC",
    ascending=False
)

best_model_name = cv_df.iloc[0]["Model"]

print("\n========== MODEL SELECTION ==========")
print("Selected model:", best_model_name)

cv_df.to_csv(
    REPORT_DIR / "cross_validation_results.csv",
    index=False
)


# --------------------------------------------------
# 6. TRAIN AND SAVE ALL MODELS
# --------------------------------------------------

print("\n========== TRAINING MODELS ==========")

trained_models = {}

for name, model in models.items():

    model.fit(X_train, y_train)

    trained_models[name] = model

    filename = (
        name.lower().replace(" ", "_") + ".joblib"
    )

    joblib.dump(
        model,
        MODEL_DIR / filename
    )

    print(f"{name} trained and saved.")


# --------------------------------------------------
# 7. EVALUATE SELECTED MODEL ON TEST DATA
# --------------------------------------------------

best_model = trained_models[best_model_name]

y_pred = best_model.predict(X_test)

y_probability = best_model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


# --------------------------------------------------
# 8. DISPLAY RESULTS
# --------------------------------------------------

print("\n========== FINAL TEST RESULTS ==========")

print("Selected model:", best_model_name)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")


# --------------------------------------------------
# 9. CONFUSION MATRIX
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1]
)

print("\nConfusion Matrix:")
print(cm)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["No Disease Label", "Disease Label"]
)

display.plot(cmap="Blues")

plt.title(f"Confusion Matrix - {best_model_name}")
plt.tight_layout()

plt.savefig(
    REPORT_DIR / "confusion_matrix.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# 10. CLASSIFICATION REPORT
# --------------------------------------------------

report = classification_report(
    y_test,
    y_pred,
    target_names=["No Disease Label", "Disease Label"],
    zero_division=0
)

print("\n========== CLASSIFICATION REPORT ==========")
print(report)


# --------------------------------------------------
# 11. SAVE BEST MODEL
# --------------------------------------------------

joblib.dump(
    best_model,
    MODEL_DIR / "best_model.joblib"
)

print("\nBest model saved successfully.")


# --------------------------------------------------
# 12. SAVE EVALUATION RESULTS
# --------------------------------------------------

evaluation_results = {
    "selected_model": best_model_name,
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
    "roc_auc": float(roc_auc),
    "confusion_matrix": cm.tolist()
}

with open(
    REPORT_DIR / "model_evaluation.json",
    "w"
) as file:

    json.dump(
        evaluation_results,
        file,
        indent=4
    )

with open(
    REPORT_DIR / "classification_report.txt",
    "w"
) as file:

    file.write(report)

print("\n========== PHASE 4 COMPLETED ==========")
print("All models trained.")
print("Cross-validation completed.")
print("Selected model evaluated on test data.")
print("Reports and model files saved.")

print("\nModel directory:", MODEL_DIR)
print("Report directory:", REPORT_DIR)
