def apply_cooling(body_temp_post, ambient_temp):

    cooling_rate = (body_temp_post - ambient_temp) * 0.15
    body_temp_post -= cooling_rate

    return body_temp_post
