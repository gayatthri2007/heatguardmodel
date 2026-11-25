import pickle
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

print("Loading data...")
env = pd.read_csv("data/environment.csv")
pre = pd.read_csv("data/Pre_Shift.csv")
post = pd.read_csv("data/Post_Shift.csv")

print(f"Environment shape: {env.shape}")
print(f"Pre-shift shape: {pre.shape}")
print(f"Post-shift shape: {post.shape}")

# Keep only first record per worker to avoid Cartesian product
env = env.drop_duplicates(subset=['worker_id'], keep='first')
pre = pre.drop_duplicates(subset=['worker_id'], keep='first')
post = post.drop_duplicates(subset=['worker_id'], keep='first')

print(f"After dedup - Env: {env.shape}, Pre: {pre.shape}, Post: {post.shape}")

# Merge with inner join to get only common worker IDs
df = env.merge(pre, on="worker_id", how="inner")
df = df.merge(post, on="worker_id", how="inner")

print(f"Merged data shape: {df.shape}")

# Compute DTHS
print("Computing heat stress index (DTHS)...")

def normalize(val, min_v, max_v):
    if max_v == min_v:
        return 0
    return (val - min_v) / (max_v - min_v)

def compute_dths(row):
    temp_rise = row["body_temp_post"] - row["body_temp_pre"]
    hr_rise = row["heart_rate_post"] - row["heart_rate_pre"]
    
    phys = (temp_rise / 2.0) + (hr_rise / 100.0)
    
    wbgt_n = normalize(row["wbgt"], 25, 40)
    temp_n = normalize(row["ambient_temp"], 25, 45)
    rh_n = normalize(row["humidity"], 30, 100)
    rad_n = normalize(row["radiant_heat"], 100, 900)
    
    env = 0.4*wbgt_n + 0.2*temp_n + 0.2*rh_n + 0.2*rad_n
    
    dths = 0.6*phys + 0.4*env
    return min(max(dths, 0), 1)

df["dths"] = df.apply(compute_dths, axis=1)

# Create risk labels
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

print(f"Risk label distribution: {df['risk_label'].value_counts().to_dict()}")

# Prepare features - only numeric columns
X = df.select_dtypes(include=[np.number]).drop(["dths"], axis=1)
y = df["risk_label"]

print(f"Features shape: {X.shape}, Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
print("Training RandomForest model with 50 trees...")
model = RandomForestClassifier(n_estimators=50, n_jobs=1, random_state=42, verbose=1)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Save the model
os.makedirs("models", exist_ok=True)
model_path = "models/random_forest.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")

def normalize(val, min_v, max_v):
    if max_v == min_v:
        return 0
    return (val - min_v) / (max_v - min_v)

def compute_dths(row):
    temp_rise = row["body_temp_post"] - row["body_temp_pre"]
    hr_rise = row["heart_rate_post"] - row["heart_rate_pre"]
    
    phys = (temp_rise / 2.0) + (hr_rise / 100.0)
    
    wbgt_n = normalize(row["wbgt"], 25, 40)
    temp_n = normalize(row["ambient_temp"], 25, 45)
    rh_n = normalize(row["humidity"], 30, 100)
    rad_n = normalize(row["radiant_heat"], 100, 900)
    
    env = 0.4*wbgt_n + 0.2*temp_n + 0.2*rh_n + 0.2*rad_n
    
    dths = 0.6*phys + 0.4*env
    return min(max(dths, 0), 1)

df["dths"] = df.apply(compute_dths, axis=1)

# Create risk labels
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

print(f"Risk label distribution: {df['risk_label'].value_counts().to_dict()}")

# Prepare features - only numeric columns
X = df.select_dtypes(include=[np.number]).drop(["dths"], axis=1)
y = df["risk_label"]

print(f"Features shape: {X.shape}, Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
print("Training RandomForest model...")
model = RandomForestClassifier(n_estimators=50, n_jobs=1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Save the model
os.makedirs("models", exist_ok=True)
model_path = "models/random_forest.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")
