
from pathlib import Path
import joblib

MODEL_DIR = Path(__file__).resolve().parent / "models"

files = [
    "best_model.joblib",
    "logistic_regression.joblib",
    "decision_tree.joblib",
    "random_forest.joblib",
    "preprocessor.joblib",
]

print("\n========== MODEL ARTIFACT VERIFICATION ==========\n")

for filename in files:
    path = MODEL_DIR / filename

    print(f"\nChecking: {filename}")

    if not path.exists():
        print("ERROR: File not found")
        continue

    try:
        artifact = joblib.load(path)

        print("Status: Successfully loaded")
        print("Object type:", type(artifact).__name__)

        if isinstance(artifact, dict):
            print("Dictionary keys:", list(artifact.keys()))

        if hasattr(artifact, "n_features_in_"):
            print("Number of input features:", artifact.n_features_in_)

        if hasattr(artifact, "feature_names_in_"):
            print("Feature names:", list(artifact.feature_names_in_))

        if hasattr(artifact, "classes_"):
            print("Model classes:", artifact.classes_)

        if hasattr(artifact, "get_feature_names_out"):
            try:
                print(
                    "Transformed features:",
                    artifact.get_feature_names_out()
                )
            except Exception as error:
                print("Feature-name inspection:", error)

    except Exception as error:
        print("ERROR:", error)

print("\n========== VERIFICATION COMPLETED ==========\n")
