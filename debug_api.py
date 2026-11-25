import requests

API_BASE = 'http://localhost:5000/api'
LOGIN = API_BASE + '/auth/login'
SUP_STATS = API_BASE + '/supervisor/dashboard/stats'
SUP_ZONES = API_BASE + '/supervisor/zones'
SUP_WORKERS = API_BASE + '/supervisor/workers'
WORK_PROFILE = API_BASE + '/worker/profile'
PREDICT = API_BASE + '/predictions/predict'

s = requests.Session()

def login(username, password):
    r = s.post(LOGIN, json={'username': username, 'password': password}, timeout=10)
    print(f'LOGIN {username}:', r.status_code)
    print(r.text)
    r.raise_for_status()
    return r.json().get('access_token')

# Supervisor: list workers and call predict for worker by worker_id
try:
    sup_token = login('supervisor1', 'admin123')
    headers = {'Authorization': f'Bearer {sup_token}'}

    r = s.get(SUP_WORKERS, headers=headers, timeout=10)
    print('\nSUP_WORKERS', r.status_code)
    print(r.text)
    workers = r.json() if r.status_code == 200 else []
    if workers:
        wid = workers[0]['worker_id']
        print('\nFound worker_id for test:', wid)
        # Supervisor tries predicting for worker by worker_id
        sample = {
            'worker_id': wid,
            'body_temp_post': 37.5,
            'body_temp_pre': 36.8,
            'heart_rate_post': 90,
            'heart_rate_pre': 75,
            'wbgt': 30,
            'ambient_temp': 33,
            'humidity': 60,
            'radiant_heat': 400,
            'break_duration': 10
        }
        rp = s.post(PREDICT, headers=headers, json=sample, timeout=10)
        print('\nPREDICT as supervisor for worker', rp.status_code)
        print(rp.text)
    else:
        print('No workers to test predict')

except Exception as e:
    print('Supervisor test error', e)

# Worker: login and predict for self
try:
    worker_token = login('worker1', 'password123')
    headers = {'Authorization': f'Bearer {worker_token}'}
    sample = {
        'body_temp_post': 37.2,
        'body_temp_pre': 36.7,
        'heart_rate_post': 88,
        'heart_rate_pre': 72,
        'wbgt': 29,
        'ambient_temp': 32,
        'humidity': 58,
        'radiant_heat': 380,
        'break_duration': 5
    }
    rp = s.post(PREDICT, headers=headers, json=sample, timeout=10)
    print('\nPREDICT as worker', rp.status_code)
    print(rp.text)
except Exception as e:
    print('Worker test error', e)
