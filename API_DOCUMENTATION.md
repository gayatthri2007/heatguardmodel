# HeatGuard API Documentation

## Base URL
- **Development:** `http://localhost:5000`
- **Production:** `https://your-domain.com`

## Authentication
All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Authentication Endpoints

### Register New User
**POST** `/api/auth/register`

**Request:**
```json
{
  "username": "worker1",
  "email": "worker@example.com",
  "password": "password123",
  "role": "worker",
  "zone": "Zone A",
  "bmi_bucket": "medium",
  "fitness_level": "medium"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "worker1",
    "email": "worker@example.com",
    "role": "worker"
  }
}
```

---

### Login
**POST** `/api/auth/login`

**Request:**
```json
{
  "username": "worker1",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "worker1",
    "email": "worker@example.com",
    "role": "worker"
  }
}
```

---

### Get Current User
**GET** `/api/auth/me`

**Headers:** 
- Authorization: Bearer <token>

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "worker1",
  "email": "worker@example.com",
  "role": "worker"
}
```

---

### Logout
**POST** `/api/auth/logout`

**Headers:** 
- Authorization: Bearer <token>

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## 🔥 Prediction Endpoints

### Digital Twin Prediction
**POST** `/api/predictions/predict`

**Headers:** 
- Authorization: Bearer <token>
- Content-Type: application/json

**Request:**
```json
{
  "body_temp_post": 37.2,
  "body_temp_pre": 36.8,
  "heart_rate_post": 85,
  "heart_rate_pre": 72,
  "wbgt": 29,
  "ambient_temp": 32,
  "humidity": 60,
  "radiant_heat": 500,
  "break_duration": 10,
  "bmi_bucket": "medium",
  "fitness_level": "medium"
}
```

**Response (200 OK):**
```json
{
  "risk": "HIGH",
  "dths": 42.5,
  "message": "High heat stress detected. Risk level HIGH",
  "recommendations": [
    "Increase water intake",
    "Take immediate cooling break",
    "Reduce work intensity"
  ]
}
```

---

### Quick Predict (No Auth)
**POST** `/predict`

This endpoint can be used by external systems (e.g. a stream of live
sensor data) to obtain a risk prediction without going through the normal
JWT‑protected API.  If the payload contains a `worker_id` value that matches
an existing worker profile the result will be recorded in the database just
like the authenticated `/api/predictions/predict` route – metrics are stored
and an alert row is created when the risk is elevated.  This makes it suitable
for feeding real‑time data into the dashboards.

**Request:**
```json
{
  "worker_id": "W_1",          # optional, use to persist data to that worker
  "body_temp_post": 37.2,
  "body_temp_pre": 36.8,
  "heart_rate_post": 85,
  "heart_rate_pre": 72,
  "wbgt": 29,
  "ambient_temp": 32,
  "humidity": 60,
  "radiant_heat": 500,
  "break_duration": 10,
  "bmi_bucket": "medium",
  "fitness_level": "medium"
}
```

**Response (200 OK):**
```json
{
  "risk": "HIGH",
  "dths": 42.5,
  "message": "High heat stress detected",
  "recommendation": "Take immediate cooling break"   
}
```

---

## 👷 Worker Endpoints

### Get Worker Profile
**GET** `/api/worker/profile`

**Headers:** 
- Authorization: Bearer <token>

**Response (200 OK):**
```json
{
  "id": 1,
  "worker_id": "W_1",
  "user_id": 1,
  "zone": "Zone A - Construction",
  "bmi_bucket": "medium",
  "fitness_level": "medium",
  "status": "ACTIVE",
  "created_at": "2024-02-16T10:00:00"
}
```

---

### Get Worker Metrics
**GET** `/api/worker/metrics?limit=20`

**Headers:** 
- Authorization: Bearer <token>

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 20)

**Response (200 OK):**
```json
{
  "metrics": [
    {
      "id": 1,
      "worker_id": 1,
      "timestamp": "2024-02-16T14:30:00",
      "body_temp": 37.2,
      "heart_rate": 85,
      "zone": "Zone A",
      "risk_level": "HIGH",
      "dths": 42.5
    },
    {
      "id": 2,
      "worker_id": 1,
      "timestamp": "2024-02-16T14:25:00",
      "body_temp": 37.0,
      "heart_rate": 80,
      "zone": "Zone A",
      "risk_level": "MEDIUM",
      "dths": 38.2
    }
  ]
}
```

---

### Get Worker Alerts
**GET** `/api/worker/alerts?limit=10`

**Headers:** 
- Authorization: Bearer <token>

**Query Parameters:**
- `limit` (optional): Number of alerts to return (default: 10)

**Response (200 OK):**
```json
{
  "alerts": [
    {
      "id": 1,
      "worker_id": 1,
      "alert_type": "TEMPERATURE",
      "severity": "CRITICAL",
      "message": "Body temperature exceeded critical threshold",
      "timestamp": "2024-02-16T14:35:00",
      "is_read": false
    },
    {
      "id": 2,
      "worker_id": 1,
      "alert_type": "HEART_RATE",
      "severity": "WARNING",
      "message": "Heart rate elevated",
      "timestamp": "2024-02-16T14:30:00",
      "is_read": true
    }
  ]
}
```

---

### Mark Alert as Read
**PUT** `/api/worker/alerts/{alertId}/read`

**Headers:** 
- Authorization: Bearer <token>

**Response (200 OK):**
```json
{
  "message": "Alert marked as read",
  "alert": {
    "id": 1,
    "is_read": true
  }
}
```

---

## 👨‍💼 Supervisor Endpoints

### Get All Workers
**GET** `/api/supervisor/workers`

**Headers:** 
- Authorization: Bearer <token> (Supervisor role required)

**Response (200 OK):**
```json
{
  "workers": [
    {
      "id": 1,
      "worker_id": "W_1",
      "username": "worker1",
      "zone": "Zone A - Construction",
      "status": "ACTIVE",
      "current_risk_level": "MEDIUM",
      "body_temp": 37.0,
      "heart_rate": 80,
      "latest_timestamp": "2024-02-16T14:30:00"
    },
    {
      "id": 2,
      "worker_id": "W_2",
      "username": "worker2",
      "zone": "Zone B - Excavation",
      "status": "ACTIVE",
      "current_risk_level": "LOW",
      "body_temp": 36.5,
      "heart_rate": 72,
      "latest_timestamp": "2024-02-16T14:28:00"
    }
  ]
}
```

---

### Get Dashboard Statistics
**GET** `/api/supervisor/dashboard/stats`

**Headers:** 
- Authorization: Bearer <token> (Supervisor role required)

**Response (200 OK):**
```json
{
  "total_workers": 10,
  "active_workers": 7,
  "workers_by_zone": {
    "Zone A - Construction": 4,
    "Zone B - Excavation": 3
  },
  "risk_distribution": {
    "LOW": 3,
    "MEDIUM": 3,
    "HIGH": 1,
    "CRITICAL": 0
  },
  "average_metrics": {
    "avg_body_temp": 36.8,
    "avg_heart_rate": 78,
    "avg_dths": 35.2
  },
  "critical_alerts": 1,
  "warning_alerts": 3
}
```

---

### Get Worker History
**GET** `/api/supervisor/worker/{workerId}/history?limit=100`

**Headers:** 
- Authorization: Bearer <token> (Supervisor role required)

**Path Parameters:**
- `workerId`: The worker's ID

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 100)

**Response (200 OK):**
```json
{
  "worker": {
    "id": 1,
    "worker_id": "W_1",
    "username": "worker1"
  },
  "history": [
    {
      "timestamp": "2024-02-16T14:30:00",
      "body_temp": 37.2,
      "heart_rate": 85,
      "wbgt": 29,
      "risk_level": "HIGH",
      "dths": 42.5,
      "alert_severity": "HIGH"
    },
    {
      "timestamp": "2024-02-16T14:25:00",
      "body_temp": 37.0,
      "heart_rate": 80,
      "wbgt": 28,
      "risk_level": "MEDIUM",
      "dths": 38.2,
      "alert_severity": null
    }
  ]
}
```

---

## 🏥 Health & Status

### System Health Check
**GET** `/api/health`

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

---

### Model Test
**GET** `/model-test`

**Response:** HTML page with model test results

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## 🔄 Request/Response Headers

### Required Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Response Headers
```
Content-Type: application/json
X-Total-Count: <number>  (for paginated responses)
```

---

## 📊 Risk Levels

| Level | Description | DTHS Range |
|-------|-------------|-----------|
| **LOW** | Safe working conditions | < 30 |
| **MEDIUM** | Monitor conditions closely | 30-38 |
| **HIGH** | Immediate intervention needed | 38-42 |
| **CRITICAL** | Emergency response required | > 42 |

---

## 🎯 Prediction Input Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| body_temp_post | float | 35-42 | Body temperature after work (°C) |
| body_temp_pre | float | 35-42 | Body temperature before work (°C) |
| heart_rate_post | int | 40-180 | Heart rate after work (bpm) |
| heart_rate_pre | int | 40-180 | Heart rate before work (bpm) |
| wbgt | float | 0-50 | Wet Bulb Globe Temperature (°C) |
| ambient_temp | float | -10-50 | Ambient temperature (°C) |
| humidity | float | 0-100 | Relative humidity (%) |
| radiant_heat | float | 0-1000 | Radiant heat intensity (W/m²) |
| break_duration | int | 0-120 | Cooling break duration (minutes) |
| bmi_bucket | string | low/medium/high | BMI category |
| fitness_level | string | low/medium/high | Worker fitness level |

---

## 📌 Rate Limiting

Currently no rate limiting is enforced. For production deployments, consider implementing rate limiting at application or API gateway level.

---

## 🔐 Security Notes

- All tokens expire after 30 days
- Passwords are hashed using werkzeug security
- Supervisor endpoints require supervisor role
- Database connections use parameterized queries to prevent SQL injection
- CORS is configured for specified origins only

---

## Testing with cURL

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"password123",
    "role":"worker"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "password":"password123"
  }'
```

### Make Prediction
```bash
curl -X POST http://localhost:5000/api/predictions/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "body_temp_post":37.2,
    "body_temp_pre":36.8,
    "heart_rate_post":85,
    "heart_rate_pre":72,
    "wbgt":29,
    "ambient_temp":32,
    "humidity":60,
    "radiant_heat":500,
    "break_duration":10,
    "bmi_bucket":"medium",
    "fitness_level":"medium"
  }'
```

---

**For more details, see [DEPLOYMENT.md](DEPLOYMENT.md) or [QUICKSTART.md](QUICKSTART.md)**
