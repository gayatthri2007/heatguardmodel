# NFC Health Check - Testing & API Reference

## Quick API Testing

### Using PowerShell (Windows)

#### Safe Condition Test
```powershell
$payload = @{
    worker_id = "W_1"
    temperature = 36.8
    heart_rate = 72
    wbgt = 24
    ambient_temp = 28
    humidity = 55
    radiant_heat = 300
    break_duration = 5
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "temperature": 36.8,
  "heart_rate": 72,
  "risk": 0,
  "dths_score": 0.18,
  "message": "✅ Safe - Conditions Normal",
  "recommendation": "Continue normal work pace",
  "persisted": true
}
```

---

#### Low Risk Test
```powershell
$payload = @{
    worker_id = "W_1"
    temperature = 37.5
    heart_rate = 95
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "temperature": 37.5,
  "heart_rate": 95,
  "risk": 1,
  "dths_score": 0.42,
  "message": "⚠️ Low Risk - Stay hydrated",
  "recommendation": "Increase water intake and take a 10-minute break",
  "persisted": true
}
```

---

#### High Risk Test
```powershell
$payload = @{
    worker_id = "W_1"
    temperature = 38.8
    heart_rate = 125
    wbgt = 32
    ambient_temp = 38
    humidity = 75
    radiant_heat = 800
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "low"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "temperature": 38.8,
  "heart_rate": 125,
  "risk": 2,
  "dths_score": 0.68,
  "message": "⚠️ High Risk - Increase monitoring",
  "recommendation": "Take immediate 15-minute break, hydrate, move to shaded area",
  "persisted": true
}
```

---

#### Critical Risk Test
```powershell
$payload = @{
    worker_id = "W_1"
    temperature = 39.5
    heart_rate = 150
    wbgt = 36
    ambient_temp = 40
    humidity = 80
    radiant_heat = 900
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "low"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "temperature": 39.5,
  "heart_rate": 150,
  "risk": 3,
  "dths_score": 0.92,
  "message": "🚨 Critical - Immediate action required",
  "recommendation": "Stop work immediately, seek medical evaluation, cool body",
  "persisted": true
}
```

---

#### Unknown Worker (No Persistence)
```powershell
$payload = @{
    worker_id = "W_999"
    temperature = 37.5
    heart_rate = 85
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload | ConvertTo-Json -Depth 10
```

**Expected Output:**
```json
{
  "temperature": 37.5,
  "heart_rate": 85,
  "risk": 0,
  "dths_score": 0.34,
  "message": "✅ Safe - Conditions Normal",
  "recommendation": "Continue normal work pace",
  "warning": "Worker W_999 not found in database"
}
```

---

### Using cURL (Linux/Mac)

#### Safe Condition Test
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
  }' | jq .
```

---

#### High Risk Test
```bash
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "W_1",
    "temperature": 38.8,
    "heart_rate": 125,
    "wbgt": 32,
    "ambient_temp": 38,
    "humidity": 75,
    "radiant_heat": 800,
    "break_duration": 0,
    "bmi_bucket": "medium",
    "fitness_level": "low"
  }' | jq .
```

---

#### Critical Test
```bash
curl -X POST http://localhost:5000/nfc-check \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "W_1",
    "temperature": 39.5,
    "heart_rate": 150,
    "wbgt": 36,
    "ambient_temp": 40,
    "humidity": 80,
    "radiant_heat": 900,
    "break_duration": 0,
    "bmi_bucket": "medium",
    "fitness_level": "low"
  }' | jq .
```

---

### Using Python (Requests Library)

```python
import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
ENDPOINT = "/nfc-check"

# Test scenarios
test_cases = {
    "safe": {
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
    },
    "low_risk": {
        "worker_id": "W_1",
        "temperature": 37.5,
        "heart_rate": 95,
        "wbgt": 28,
        "ambient_temp": 32,
        "humidity": 60,
        "radiant_heat": 500,
        "break_duration": 0,
        "bmi_bucket": "medium",
        "fitness_level": "medium"
    },
    "high_risk": {
        "worker_id": "W_1",
        "temperature": 38.8,
        "heart_rate": 125,
        "wbgt": 32,
        "ambient_temp": 38,
        "humidity": 75,
        "radiant_heat": 800,
        "break_duration": 0,
        "bmi_bucket": "medium",
        "fitness_level": "low"
    },
    "critical": {
        "worker_id": "W_1",
        "temperature": 39.5,
        "heart_rate": 150,
        "wbgt": 36,
        "ambient_temp": 40,
        "humidity": 80,
        "radiant_heat": 900,
        "break_duration": 0,
        "bmi_bucket": "medium",
        "fitness_level": "low"
    }
}

# Run tests
for test_name, payload in test_cases.items():
    print(f"\n{'='*60}")
    print(f"Test: {test_name.upper()}")
    print(f"{'='*60}")
    
    response = requests.post(
        f"{BASE_URL}{ENDPOINT}",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    # Verify response
    data = response.json()
    assert "risk" in data, "Missing 'risk' in response"
    assert "dths_score" in data, "Missing 'dths_score'"
    assert "message" in data, "Missing 'message'"
    assert "recommendation" in data, "Missing 'recommendation'"
    assert data["temperature"] == payload["temperature"], "Temperature mismatch"
    assert data["heart_rate"] == payload["heart_rate"], "Heart rate mismatch"
    print("✅ Test passed!")

print("\n" + "="*60)
print("All tests completed successfully!")
print("="*60)
```

**Run With:**
```bash
python nfc_test.py
```

---

## Database Verification

### Check Recent NFC Readings (SQLite)

```sql
-- View all NFC readings for worker
SELECT 
    id,
    body_temp_post as temperature,
    heart_rate_post as heart_rate,
    risk_level as risk,
    dths_score,
    timestamp
FROM worker_metrics
WHERE worker_id = 1  -- Replace with your worker ID
ORDER BY timestamp DESC
LIMIT 10;

-- View all NFC alerts
SELECT 
    id,
    risk_level,
    message,
    created_at,
    is_read
FROM alerts
WHERE message LIKE '%NFC Alert%'
ORDER BY created_at DESC
LIMIT 10;

-- Count total NFC readings
SELECT COUNT(*) as total_nfc_readings
FROM worker_metrics
WHERE worker_id = 1;

-- Get latest NFC reading
SELECT 
    body_temp_post as temperature,
    heart_rate_post as heart_rate,
    risk_level as risk,
    dths_score,
    timestamp
FROM worker_metrics
WHERE worker_id = 1
ORDER BY timestamp DESC
LIMIT 1;
```

### Check Using Python

```python
import sys
sys.path.insert(0, '/path/to/backend')

from database.db import db, create_app
from models.worker import WorkerMetrics
from models.alert import Alert

app = create_app()
with app.app_context():
    # Get latest NFC reading
    latest = WorkerMetrics.query.filter_by(worker_id=1).order_by(
        WorkerMetrics.timestamp.desc()
    ).first()
    
    if latest:
        print(f"Latest NFC Reading:")
        print(f"  Temperature: {latest.body_temp_post}°C")
        print(f"  Heart Rate: {latest.heart_rate_post} BPM")
        print(f"  Risk Level: {latest.risk_level}")
        print(f"  DTHS Score: {latest.dths_score:.3f}")
        print(f"  Timestamp: {latest.timestamp}")
    
    # Get recent NFC alerts
    nfc_alerts = Alert.query.filter(
        Alert.message.like('%NFC Alert%')
    ).order_by(Alert.created_at.desc()).limit(5).all()
    
    print(f"\nRecent NFC Alerts ({len(nfc_alerts)}):")
    for alert in nfc_alerts:
        print(f"  - {alert.message} (Risk: {alert.risk_level})")
```

---

## Frontend Testing

### Test NFC Component in DevTools Console

```javascript
// Open browser DevTools (F12) > Console tab

// Test 1: Verify component is loaded
console.log('NFCHealthCheck component loaded:', !!document.querySelector('.nfc-health-check-wrapper'));

// Test 2: Check button visibility
const nfcButton = document.querySelector('.nfc-button');
console.log('NFC button visible:', nfcButton && nfcButton.offsetParent !== null);

// Test 3: Simulate button click (won't trigger actual NFC, but shows UI)
nfcButton.click();
console.log('Button clicked, spinner should appear');

// Test 4: Check if Web NFC API supported
console.log('Web NFC API supported:', 'NDEFReader' in window);

// Test 5: Check if camera API supported
console.log('Camera API supported:', navigator.mediaDevices && !!navigator.mediaDevices.getUserMedia);

// Test 6: Monitor network requests
// Open Network tab, click NFC button, watch for POST to /nfc-check
console.log('Watch Network tab for POST /nfc-check request');

// Test 7: Monitor React state
// Install React DevTools extension, inspect NFCHealthCheck component
// Check: isScanning, scanStatus, tempReading, hrReading, result, error
console.log('Inspect NFCHealthCheck in React DevTools for component state');
```

---

## UI/UX Testing Checklist

### Visual Testing
- [ ] NFC button appears below Current Status section
- [ ] Button has gradient background (purple)
- [ ] Button has phone icon (Smartphone from lucide-react)
- [ ] Button text says "NFC Health Check"
- [ ] Button size is 100x100 pixels (circular)
- [ ] Border is visible around button (white with opacity)
- [ ] Button cursor changes to pointer on hover
- [ ] Button appears to scale up on hover (1.1x)
- [ ] Spinner appears centered in button when scanning
- [ ] Spinner rotates smoothly
- [ ] Status messages appear below button during scan
- [ ] Status box has border-left indicator (green)
- [ ] Results card appears after completion
- [ ] Results card is white with shadow
- [ ] Results grid shows 4 columns (Temp, HR, Risk, DTHS)
- [ ] Risk level displays colored value
- [ ] Recommendation box has orange border
- [ ] Error messages display in red
- [ ] All text is readable (contrast ratio ≥ 4.5:1)

### Functional Testing
- [ ] Button click triggers scanning process
- [ ] Status messages update in real-time
- [ ] NFC permission prompt appears
- [ ] Camera permission prompt appears
- [ ] Camera video stream shows in video element
- [ ] Spinner stops after ~12 seconds
- [ ] Results display with correct risk level
- [ ] Risk color matches level (0=green, 1=orange, 2=red, 3=darkred)
- [ ] Message text is appropriate for risk level
- [ ] Recommendation is specific and actionable
- [ ] Dashboard updates after completion (Recent Metrics)
- [ ] Alert appears if risk ≥ 2 (Recent Alerts)
- [ ] Form data gets updated with NFC readings
- [ ] Error displays if NFC unavailable
- [ ] Error displays if camera unavailable
- [ ] Fallback temperature used if NFC fails
- [ ] Subsequent readings create separate database rows

### Edge Case Testing
- [ ] Multiple rapid clicks don't cause issues
- [ ] Refresh during scan shows appropriate state
- [ ] Browser back button works properly
- [ ] Network failure shows error message
- [ ] Very low/high values handled correctly
- [ ] Missing optional fields use defaults
- [ ] Worker not found still returns risk calculation
- [ ] Concurrent requests from different workers work

---

## Performance Testing

### Measurement Script (PowerShell)

```powershell
# Time the NFC API request
$url = "http://localhost:5000/nfc-check"
$payload = @{
    worker_id = "W_1"
    temperature = 37.5
    heart_rate = 88
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

# Measure 10 requests
$times = @()
for ($i = 1; $i -le 10; $i++) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-RestMethod -Uri $url `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $payload
    $sw.Stop()
    $times += $sw.ElapsedMilliseconds
    Write-Host "Request $i`: $($sw.ElapsedMilliseconds)ms"
}

$avg = ($times | Measure-Object -Average).Average
$max = ($times | Measure-Object -Maximum).Maximum
$min = ($times | Measure-Object -Minimum).Minimum

Write-Host "`nPerformance Summary:"
Write-Host "Average: ${avg}ms"
Write-Host "Min: ${min}ms"
Write-Host "Max: ${max}ms"
```

---

## Error Scenarios

### Test Missing Worker ID
```powershell
$payload = @{
    temperature = 37.5
    heart_rate = 88
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload
```

**Expected**: Still calculates risk, no persistence error

---

### Test Invalid JSON
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body '{ invalid json'
```

**Expected**: 400 or 500 error with error message

---

### Test Missing Temperature
```powershell
$payload = @{
    worker_id = "W_1"
    heart_rate = 88
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/nfc-check" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $payload
```

**Expected**: Uses default value (37.0)

---

## Load Testing

### Basic Load Test (Apache Bench if available)

```bash
# Test with 100 requests, max 10 concurrent
ab -n 100 -c 10 -p payload.json -T application/json http://localhost:5000/nfc-check

# Expected: <500ms average response time
```

### PowerShell Load Test

```powershell
$url = "http://localhost:5000/nfc-check"
$payload = @{
    worker_id = "W_1"
    temperature = 37.5
    heart_rate = 88
    wbgt = 28
    ambient_temp = 32
    humidity = 60
    radiant_heat = 500
    break_duration = 0
    bmi_bucket = "medium"
    fitness_level = "medium"
} | ConvertTo-Json

$sw = [System.Diagnostics.Stopwatch]::StartNew()

for ($i = 1; $i -le 100; $i++) {
    Invoke-RestMethod -Uri $url `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $payload | Out-Null
}

$sw.Stop()
$avgTime = $sw.Elapsed.TotalMilliseconds / 100

Write-Host "Load Test Results:"
Write-Host "Total Time: $($sw.Elapsed.TotalSeconds) seconds"
Write-Host "Average Per Request: ${avgTime}ms"
Write-Host "Requests Per Second: $([Math]::Round(100 / $sw.Elapsed.TotalSeconds))"
```

---

## CI/CD Integration Example

### GitHub Actions Workflow (if you use GitHub)

```yaml
name: NFC Feature Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      flask:
        image: python:3.9
        options: >-
          --name flask-service
        
    steps:
    - uses: actions/checkout@v2
    
    - name: Start Flask Backend
      run: |
        cd backend
        pip install -r requirements.txt
        python app.py &
        sleep 5
    
    - name: Run NFC API Tests
      run: python test_nfc_api.py
      
    - name: Test Dashboard Integration
      run: npm test --prefix frontend
      
    - name: Check Database
      run: python verify_database.py
```

---

## Summary

**Test Coverage:**
- ✅ API endpoint functionality
- ✅ Request/response validation
- ✅ Database persistence
- ✅ Frontend component rendering
- ✅ Error handling
- ✅ Performance characteristics
- ✅ Browser compatibility
- ✅ Load testing

**Next Steps:**
1. Run all API tests from "Quick API Testing" section
2. Verify database with "Database Verification" section
3. Test UI in browser using "Frontend Testing" section
4. Monitor performance with "Performance Testing" section
5. Report any failures with exact curl/PowerShell command used

