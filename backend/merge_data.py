import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

def merge_all(include_risk=False):
    # Determine the data directory path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    data_dir = os.path.join(project_root, "data")
    
    # Read CSV files with correct case-sensitive names
    baseline = pd.read_csv(os.path.join(data_dir, "Worker_Baseline.csv"))
    memory = pd.read_csv(os.path.join(data_dir, "Worker_Memory.csv"))
    env = pd.read_csv(os.path.join(data_dir, "environment.csv"))
    pre = pd.read_csv(os.path.join(data_dir, "Pre_Shift.csv"))
    post = pd.read_csv(os.path.join(data_dir, "Post_Shift.csv"))

    # Filter to matching worker IDs only to avoid Cartesian product
    valid_workers = set(env['worker_id']).intersection(
        set(pre['worker_id']), 
        set(post['worker_id']),
        set(baseline['worker_id']),
        set(memory['worker_id'])
    )
    
    env = env[env['worker_id'].isin(valid_workers)]
    pre = pre[pre['worker_id'].isin(valid_workers)]
    post = post[post['worker_id'].isin(valid_workers)]
    baseline = baseline[baseline['worker_id'].isin(valid_workers)]
    memory = memory[memory['worker_id'].isin(valid_workers)]
    
    # Merge on worker_id
    df = env.merge(pre, on="worker_id")
    df = df.merge(post, on="worker_id")
    df = df.merge(baseline, on="worker_id")
    df = df.merge(memory, on="worker_id")
    
    # Convert categorical columns to numeric
    categorical_cols = ['age_range', 'bmi_bucket', 'job_role', 'fitness_level', 'ppe_type']
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    
    # Select only numeric columns for modeling
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    df = df[numeric_cols]

    # if caller wants labels we compute dths and risk_label (same logic as retrain)
    if include_risk:
        from dths import compute_dths

        df['dths'] = df.apply(compute_dths, axis=1)

        def label_from_dths(val):
            if val <= 0.30:
                return 0
            elif val <= 0.60:
                return 1
            elif val <= 0.80:
                return 2
            else:
                return 3

        df['risk_label'] = df['dths'].apply(label_from_dths)

    return df


if __name__ == "__main__":
    # when executed as a script, produce merged dataset including risk labels
    df = merge_all(include_risk=True)
    print(df.head())
    print("rows,cols", df.shape)
    # save to disk for offline inspection or dashboard ingestion
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    out_path = os.path.join(project_root, "data", "merged_with_risk.csv")
    df.to_csv(out_path, index=False)
    print(f"✅ merged dataset written to {out_path}")

