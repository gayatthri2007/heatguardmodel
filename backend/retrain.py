import pickle
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from merge_data import merge_all
from dths import compute_dths

def retrain():

    print("🔄 Retraining started...")

    df = merge_all()

    df["dths"] = df.apply(compute_dths, axis=1)

    def label_from_dths(val):
        if val <= 0.30:
            return 0
        elif val <= 0.60:
            return 1
        elif val <= 0.80:
            return 2
        else:
            return 3

    df["risk_label"] = df["dths"].apply(label_from_dths)

    X = df.drop(["risk_label", "dths"], axis=1)
    y = df["risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    # Save model
    with open("models/random_forest.pkl", "wb") as f:
        pickle.dump(model, f)

    # Log accuracy
    with open("models/retrain_log.txt", "a") as log:
        log.write(f"{datetime.now()} - Accuracy: {accuracy}\n")

    print("✅ Retraining complete. Accuracy:", accuracy)

if __name__ == "__main__":
    retrain()
