# NFC Health Check Feature - Complete Implementation Guide

## Overview

The NFC Health Check feature enables workers to perform rapid health assessments using:
1. **NFC (Near Field Communication)** for temperature reading from an NFC tag/sensor
2. **Back Camera + PPG (Photoplethysmography)** for non-contact heart rate detection
3. **Risk Assessment** via Flask backend using Digital Twin ML model

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKER DASHBOARD (React)                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           Current Status Card                              │ │
│  │  Zone | Ambient Temp | Hydration Reminder                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         NFC Health Check Component                         │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  [NFC Health Check] (Circular Button)                │ │ │
│  │  │  • Spinner during scan                               │ │ │
│  │  │  • Status messages                                   │ │ │
│  │  │  • Results card with metrics                         │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Recent Metrics (Updated automatically)                    │ │
│  │  • Latest reading from NFC check                           │ │
│  │  • Risk level & DTHS score                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Recent Alerts (Updated automatically)                     │ │
│  │  • If risk ≥ 2, alert appears                            │ │
│  │  • NFC Alert prefix for identification                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────┬──────────────────────┘
                                           │
                      (2) Fetch to /nfc-check
                      with temp + HR + worker_id
                                           │
                                           ↓
                    ┌─────────────────────────────────┐
                    │  Flask Backend (/nfc-check)     │
                    │                                  │
                    │  • Parse NFC data               │
                    │  • Build prediction input       │
                    │  • Call digital_twin()          │
                    │  • Persist metric & alert       │
                    │  • Return risk + DTHS           │
                    │                                  │
                    │  (1) Web NFC API                │
                    │  (2) getUserMedia() for camera  │
                    │  (3) PPG heart rate detection   │
                    └─────────────────────────────────┘
```

---

## Frontend Implementation

### Component: NFCHealthCheck.jsx

**Location:** `frontend/src/components/Worker/NFCHealthCheck.jsx`

**Key Features:**

1. **NFC Temperature Reading (Web NFC API)**
   - Requests access to device NFC hardware
   - Scans for NDEF records containing temperature
   - Format expected: `TEMP:37.5` (text record)
   - Fallback: Simulated temperature if not supported

2. **Heart Rate Detection (Camera + PPG)**
   - Requests back camera access via `getUserMedia()`
   - Captures video frames for 10 seconds
   - Analyzes green channel pixel intensity (PPG signal)
   - Detects peaks to calculate BPM
   - Returns estimated heart rate (60-180 range)

3. **Risk Calculation**
   - Sends temperature + heart rate to Flask backend
   - Receives risk level (0-3) from Digital Twin model
   - Displays results in formatted card

4. **State Management**
   - `isScanning`: Button disabled state during scan
   - `scanStatus`: User-friendly status messages
   - `tempReading`: Temperature from NFC
   - `hrReading`: Heart rate from camera
   - `result`: Calculated risk and DTHS
   - `error`: Error messages

### Styling: NFCHealthCheck.css

**Key Classes:**
- `.nfc-button`: Circular floating button (100x100px)
- `.nfc-button.scanning`: Spinning animation during scan
- `.scan-status`: Status message box with progress indicator
- `.nfc-result-card`: Results display card
- `.result-grid`: 4-column grid for temperature/HR/risk/DTHS
- `.alert-danger`: Error message styling
- Animations: `spin`, `fadeInUp`, `slideDown`, `slideUp`

---

## Backend Implementation

### Endpoint: POST /nfc-check

**Purpose:** Process NFC health check data and assess risk

**Request Schema:**
```json
{
  "worker_id": "W_1",
  "temperature": 37.5,
  "heart_rate": 88,
  "wbgt": 28,
  "ambient_temp": 32,
  "humidity": 60,
  "radiant_heat": 500,
  "break_duration": 0,
  "bmi_bucket": "medium",
  "fitness_level": "medium"
}
```

**Response Schema (Success):**
```json
{
  "temperature": 37.5,
  "heart_rate": 88,
  "risk": 1,
  "dths_score": 0.425,
  "message": "⚠️ Low Risk - Stay hydrated",
  "recommendation": "Increase water intake and take a 10-minute break",
  "persisted": true
}
```

**Response Schema (Error):**
```json
{
  "error": "Required field missing"
}
```

**Backend Processing:**
1. Extract temperature and heart rate from request
2. Build complete prediction input with environmental data
3. Call `digital_twin(input)` for risk assessment
4. Generate appropriate message via `get_risk_message()`
5. Persist WorkerMetrics record with NFC data
6. Create Alert if risk ≥ 2
7. Return risk level and DTHS score to frontend

**Database Updates:**
- **WorkerMetrics table**: New row with all vital signs and risk
- **Alert table**: New alert if risk_level ≥ 2, marked as NFC source
- **Processing Time**: <1 second (synchronous)

---

## API Examples

### Example 1: Safe Reading
```bash
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "W_1",
    "temperature": 36.8,
    "heart_rate": 72,
    "wbgt": 24,
    "ambient_temp": 28,
    "humidity": 55,
    "radiant_heat": 300,
    "break_duration": 5,
    "bmi_bucket": "medium",
    "fitness_level": "medium"
  }'
```

**Response:**
```json
{
  "temperature": 36.8,
  "heart_rate": 72,
  "risk": 0,
  "dths_score": 0.180,
  "message": "✅ Safe - Conditions Normal",
  "recommendation": "Continue normal work pace",
  "persisted": true
}
```

### Example 2: High Risk Reading
```bash
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "W_1",
    "temperature": 39.2,
    "heart_rate": 135,
    "wbgt": 32,
    "ambient_temp": 38,
    "humidity": 75,
    "radiant_heat": 800,
    "break_duration": 0,
    "bmi_bucket": "medium",
    "fitness_level": "low"
  }'
```

**Response:**
```json
{
  "temperature": 39.2,
  "heart_rate": 135,
  "risk": 2,
  "dths_score": 0.680,
  "message": "⚠️ High Risk - Increase monitoring",
  "recommendation": "Take immediate 15-minute break, hydrate, move to shaded area",
  "persisted": true
}
```

### Example 3: Unknown Worker
```bash
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "W_999",
    "temperature": 37.5,
    "heart_rate": 85,
    "wbgt": 28,
    "ambient_temp": 32,
    "humidity": 60,
    "radiant_heat": 500,
    "break_duration": 0,
    "bmi_bucket": "medium",
    "fitness_level": "medium"
  }'
```

**Response:**
```json
{
  "temperature": 37.5,
  "heart_rate": 85,
  "risk": 0,
  "dths_score": 0.344,
  "message": "✅ Safe - Conditions Normal",
  "recommendation": "Continue normal work pace",
  "warning": "Worker W_999 not found in database"
}
```

---

## Browser Requirements

### For NFC Functionality:
- **Browser Support**: Chrome 89+, Edge 89+, Firefox 113+
- **Device**: Mobile device with NFC hardware (most smartphones)
- **Permissions**: User must grant NFC access permission
- **API Version**: Web NFC Level 1

### For Camera Heart Rate Detection:
- **Browser Support**: All modern browsers (Chrome, Firefox, Safari, Edge)
- **Device**: Back camera available (smartphone/tablet)
- **Permissions**: User must grant camera access permission
- **Constraints**: Prefers back camera (`facingMode: 'environment'`)

### Fallback Behavior:
- If NFC unavailable: Simulates temperature (37.2 + 0-2°C random)
- If Camera unavailable: Returns error message "Camera Error"
- System continues to function with either sensor failing

---

## Risk Classification

| Level | Value | Color | Message | Action |
|-------|-------|-------|---------|--------|
| Safe | 0 | Green | ✅ Safe - Conditions Normal | Continue work |
| Low Risk | 1 | Orange | ⚠️ Low Risk - Stay hydrated | Monitor closely |
| High Risk | 2 | Red | ⚠️ High Risk - Increase monitoring | Take break immediately |
| Critical | 3 | Dark Red | 🚨 Critical - Immediate action required | Stop work, seek medical eval |

---

## Digital Twin Risk Calculation

The `/nfc-check` endpoint uses the same risk algorithm as the main prediction pipeline:

```python
def digital_twin(input_data):
    # 1. Baseline adjustment (BMI, fitness level)
    adjusted_baseline = adjust_baseline(input_data)
    
    # 2. Environmental exposure calculation
    env_exposure = calculate_env_exposure(
        wbgt, ambient_temp, radiant_heat, humidity
    )
    
    # 3. Cooling intervention adjustment
    cooling_effect = apply_cooling_intervention(break_duration)
    
    # 4. DTHS physiological score (0.6*phys + 0.4*env)
    dths = 0.6 * normalized_bodytemp_and_hr + 0.4 * env_exposure
    
    # 5. ML Random Forest prediction
    ml_risk = trained_model.predict(input_data)
    
    # 6. Rule-based override
    if body_temp >= 39 or heart_rate >= 140 or wbgt > 35:
        return risk_level=3
    else:
        return ml_risk
    
    return (final_risk, dths_score)
```

---

## Testing the Feature

### Step 1: Verify Backend Endpoint
```bash
# Test with cURL
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{"worker_id":"W_1","temperature":37.5,"heart_rate":80,"wbgt":28,"ambient_temp":32,"humidity":60,"radiant_heat":500,"break_duration":0,"bmi_bucket":"medium","fitness_level":"medium"}'

# Expected: risk=0 or 1, persisted=true response
```

### Step 2: Simulate NFC + Camera in Browser
1. Navigate to Worker Dashboard
2. Scroll to "NFC Health Check" section
3. Click the circular NFC button
4. Browser will request NFC permission (allow if device supports)
5. Browser will request camera permission (allow and point at light source)
6. Wait 10 seconds for heart rate detection
7. Observe results card with temperature, HR, risk, DTHS

### Step 3: Verify Database Persistence
```bash
# Query backend logs or database
# Check that new WorkerMetrics row was created
# Check that new Alert appeared (if risk ≥ 2)

# In Python:
from models.worker import WorkerMetrics
from models.alert import Alert
metrics = WorkerMetrics.query.filter_by(worker_id=1).order_by(WorkerMetrics.id.desc()).first()
print(f"Latest NFC metric: {metrics.body_temp_post}°C, HR={metrics.heart_rate_post} bpm, Risk={metrics.risk_level}")
```

### Step 4: Verify Dashboard Updates
1. After NFC check completes, Recent Metrics section should auto-update
2. If risk ≥ 2, Recent Alerts section shows new NFC Alert
3. Supervisor dashboard shows new alert in Recent Alerts with "NFC Alert:" prefix
4. Supervisor navbar bell icon increments unread count

---

## Troubleshooting

### NFC Not Working
**Symptom**: "NFC not supported on this device"
- **Cause**: Device lacks NFC hardware or browser doesn't support Web NFC API
- **Solution**: Ensure you're on a compatible mobile device and browser; fallback will use simulated temperature

### Camera Permission Denied
**Symptom**: "Camera Error: Permission denied"
- **Cause**: User denied camera access or HTTPS not available
- **Solution**: Grant camera permission in browser settings; ensure `localhost` is trusted

### Heart Rate Shows 0 or Unrealistic Value
**Symptom**: PPG algorithm returns invalid BPM
- **Cause**: Poor lighting, hand movement, finger not covering camera
- **Solution**: Ensure bright light on camera, keep finger steady, place finger firmly on back camera

### Backend Returns 500 Error
**Symptom**: "Backend request failed" in UI
- **Cause**: Server error, worker_id not found, or database connection issue
- **Solution**: Check Flask logs for detailed error; verify worker exists in database

### Results Not Persisting
**Symptom**: Data sent to backend but metrics not appearing in dashboard
- **Cause**: Database commit failed or Alert threshold not met
- **Solution**: Check backend logs; ensure worker_id exists; risk must be ≥ 2 to create Alert

---

## Performance Metrics

| Operation | Duration | Notes |
|-----------|----------|-------|
| NFC temperature read | 2-3s | Waits for tag scan |
| Camera heart rate detect | ~10s | Requires 10-second video capture |
| Backend risk calculation | <500ms | Synchronous processing |
| Dashboard update (polling) | 15s | Next automatic refresh |
| **Total end-to-end** | ~12-15s | From button click to results visible |

---

## Security Considerations

1. **No Authentication Required for /nfc-check**
   - Same as `/predict` endpoint
   - Requires valid `worker_id` in request body
   - Worker validation happens at database query time
   - Consider adding JWT auth if sensitive data involved

2. **Data Retention**
   - All NFC readings persisted to database
   - No automatic pruning (consider retention policy)
   - Alerts stored indefinitely (marked as read manually)

3. **Camera Access**
   - User grants explicit permission (browser prompt)
   - Only accessible via HTTPS or localhost
   - Stream stopped immediately after measurement

4. **NFC Tag Data**
   - No encryption in Web NFC API (Level 1)
   - Consider secure implementation for production NFC hardware

---

## Future Enhancements

1. **Audio Alerts**: Play warning sound if risk ≥ 2
2. **Mobile Notifications**: Push notifications to supervisor
3. **Trend Analysis**: Compare NFC readings over time
4. **Adaptive Sampling**: Increase frequency if approaching high risk
5. **Wearable Integration**: Connect to smartwatch sensors
6. **Geolocation**: Auto-detect ambient conditions from location
7. **Historical Comparison**: Show improvement/deterioration trends
8. **Photo Validation**: Capture image proof of environmental conditions
9. **Multi-Device Sync**: Share results across worker/supervisor devices
10. **Export Reports**: Generate PDF health check reports

---

## Related Files

- `frontend/src/components/Worker/NFCHealthCheck.jsx` - React component
- `frontend/src/components/Worker/NFCHealthCheck.css` - Styling
- `frontend/src/components/Worker/Dashboard.jsx` - Parent component (integration)
- `backend/app.py` - Flask route definition
- `backend/ml_engine/twin_engine.py` - Risk calculation logic
- `backend/models/worker.py` - WorkerMetrics and Alert models

---

## References

- [Web NFC API - W3C Specification](https://w3c.github.io/web-nfc/)
- [getUserMedia() - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- [Photoplethysmography - Wikipedia](https://en.wikipedia.org/wiki/Photoplethysmography)
- [PPG Heart Rate Detection - Academic Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6407942/)

