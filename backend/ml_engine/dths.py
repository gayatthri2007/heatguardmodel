import numpy as np

def normalize(val, min_v, max_v):
    if max_v - min_v == 0:
        return 0
    return (val - min_v) / (max_v - min_v)

def compute_dths(row):
    """
    Compute Digital Twin Heat Strain (DTHS) score
    Returns value between 0 and 1
    """
    try:
        # Pillar 1: Physiological factors
        temp_rise = row.get("body_temp_post", 37) - row.get("body_temp_pre", 37)
        hr_rise = row.get("heart_rate_post", 70) - row.get("heart_rate_pre", 70)
        
        phys = (temp_rise / 2.0) + (hr_rise / 100.0)
        
        # Pillar 2: Environmental factors
        wbgt_n = normalize(row.get("wbgt", 25), 25, 40)
        temp_n = normalize(row.get("ambient_temp", 25), 25, 45)
        rh_n = normalize(row.get("humidity", 30), 30, 100)
        rad_n = normalize(row.get("radiant_heat", 100), 100, 900)
        
        env = 0.4*wbgt_n + 0.2*temp_n + 0.2*rh_n + 0.2*rad_n
        
        # Combined DTHS
        dths = 0.6*phys + 0.4*env
        return min(max(dths, 0), 1)
    except Exception as e:
        print(f"Error computing DTHS: {e}")
        return 0.5
