import pickle
import pandas as pd
import os
import sys

# Handle imports properly
try:
    from .cooling import apply_cooling
    from .dths import compute_dths
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cooling import apply_cooling
    from dths import compute_dths

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/random_forest.pkl')

model = None
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Warning: Model not found at {MODEL_PATH}")
    model = None

def digital_twin(input_data):
    """
    4-Pillar Digital Twin Logic:
    1. Baseline adjustment (BMI, fitness)
    2. Environmental exposure
    3. Cooling intervention
    4. DTHS calculation + ML prediction
    
    Returns: (final_risk, dths_score)
    """
    
    # Pillar 1: Baseline adjustment
    baseline_factor = 1.0
    
    if input_data.get("bmi_bucket") == "high":
        baseline_factor += 0.1
    
    if input_data.get("fitness_level") == "low":
        baseline_factor += 0.1
    
    # Pillar 3: Cooling intervention
    if input_data.get("break_duration", 0) > 0:
        input_data["body_temp_post"] = apply_cooling(
            input_data.get("body_temp_post", 37),
            input_data.get("ambient_temp", 25),
            input_data.get("break_duration", 0)
        )
    
    # Pillar 4: DTHS calculation
    dths = compute_dths(input_data)
    dths *= baseline_factor
    dths = min(max(dths, 0), 1)
    
    # ML Prediction
    rf_pred = 0
    if model:
        try:
            df = pd.DataFrame([input_data])
            rf_pred = model.predict(df)[0]
        except Exception as e:
            print(f"ML prediction error: {e}")
            rf_pred = 0
    
    # Rule-based override
    rule_pred = 0
    if input_data.get("body_temp_post", 37) >= 39:
        rule_pred = 3
    elif input_data.get("heart_rate_post", 70) >= 140:
        rule_pred = 2
    elif input_data.get("wbgt", 25) > 35:
        rule_pred = 2
    
    # Final risk = max of ML and rules
    final_risk = max(int(rf_pred), rule_pred)
    
    return final_risk, round(dths, 3)

def get_risk_message(risk_level):
    """Get message based on risk level"""
    messages = {
        0: "✅ Safe - Continue work",
        1: "⚠️ Low Risk - Monitor closely",
        2: "🔴 High Risk - Take break",
        3: "🚨 Critical - Immediate action required"
    }
    return messages.get(risk_level, "Unknown risk")


def get_risk_label(risk_level):
    """Return a short textual label for the numeric risk level.

    This complements the human-readable message and lets clients render
    consistent string classifiers (e.g. safe/low/high/critical).
    """
    labels = ['safe', 'low', 'high', 'critical']
    try:
        return labels[int(risk_level)]
    except Exception:
        return 'unknown'


def get_recommendation(risk_level):
    """Return written recommendation based on risk level (reuse in API).

    This was previously defined inside ``routes/predictions.py`` but moving it
    here lets the no-auth predict endpoint in ``app.py`` reuse the same
    language without creating a circular import between the blueprints.
    """
    recommendations = {
        0: "Continue work, maintain hydration",
        1: "Monitor vital signs, take regular water breaks",
        2: "Take 15-20 minute break in cool area, hydrate",
        3: "Stop work immediately, seek medical attention"
    }
    return recommendations.get(risk_level, "Unknown")
