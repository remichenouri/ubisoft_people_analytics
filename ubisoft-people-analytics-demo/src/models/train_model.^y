"""
Training script : RandomForest + MLflow tracking.
Exécuter :  python src/models/train_model.py
"""

import os, joblib, mlflow, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

DATA_PATH = "data/sample_data.csv"
MODEL_PATH = "models/random_forest.pkl"

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
mlflow.set_experiment("ubisoft_people_analytics")


def main():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["adhd_risk"])
    y = df["adhd_risk"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42,
    )
    clf.fit(X_tr, y_tr)
    preds = clf.predict(X_te)
    f1 = f1_score(y_te, preds)
    print(f"F1-score : {f1:.3f}")

    with mlflow.start_run():
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 8)
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(clf, "model")

        os.makedirs("models", exist_ok=True)
        joblib.dump(clf, MODEL_PATH)
        mlflow.log_artifact(MODEL_PATH)


if __name__ == "__main__":
    main()
