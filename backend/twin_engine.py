import pickle
import pandas as pd
from cooling import apply_cooling
from dths import compute_dths

with open("models/random_forest.pkl", "rb") as f:
    model = pickle.load(f)

def digital_twin(input_data):

    # Pillar 1 — Baseline adjustment
    baseline_factor = 1.0

    if input_data["bmi_bucket"] == "high":
        baseline_factor += 0.1

    if input_data["fitness_level"] == "low":
        baseline_factor += 0.1

    # Pillar 3 — Cooling
    if input_data["break_duration"] > 0:
        input_data["body_temp_post"] = apply_cooling(
            input_data["body_temp_post"],
            input_data["ambient_temp"]
        )

    # Pillar 4 — DTHS
    dths = compute_dths(input_data)

    # ML Prediction
    df = pd.DataFrame([input_data])
    rf_pred = model.predict(df)[0]

    # Rule Override
    rule_pred = 0
    if input_data["body_temp_post"] >= 39:
        rule_pred = 3
    elif input_data["heart_rate_post"] >= 140:
        rule_pred = 2
    elif input_data["wbgt"] > 35:
        rule_pred = 2

    final_risk = max(rf_pred, rule_pred)

    return final_risk, dths
