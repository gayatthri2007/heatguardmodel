import requests

url = 'http://localhost:5000/nfc-check'
for hr in [70, 150]:
    payload = {'worker_id': 'W_1', 'temperature': 37, 'heart_rate': hr, 'wbgt': 28,
               'ambient_temp': 32, 'humidity': 60, 'radiant_heat': 500,
               'break_duration': 0, 'bmi_bucket': 'medium', 'fitness_level': 'medium'}
    r = requests.post(url, json=payload)
    print(hr, r.status_code, r.json())
