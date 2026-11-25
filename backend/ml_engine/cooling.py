def apply_cooling(body_temp_post, ambient_temp, break_duration=0):
    """
    Apply passive/active cooling based on break duration
    break_duration in minutes
    """
    if break_duration <= 0:
        return body_temp_post
    
    # Cooling rate increases with break duration
    cooling_rate = (body_temp_post - ambient_temp) * 0.15 * (break_duration / 15)
    body_temp_post -= cooling_rate
    
    # Ensure body temp doesn't go below ambient
    return max(body_temp_post, ambient_temp + 0.5)
