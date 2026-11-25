import numpy as np

def normalize(val, min_v, max_v):
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
