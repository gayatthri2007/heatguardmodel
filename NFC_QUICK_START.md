# NFC Health Check - Quick Start Guide

## What is the NFC Health Check Feature?

The NFC Health Check is a mobile-first feature that allows workers to perform rapid health assessments using:
- **NFC Tag/Sensor** to measure body temperature
- **Back Camera** to detect heart rate via photoplethysmography (PPG)
- **AI/ML Model** to calculate heat stress risk instantly

## Where is it Located?

In the Worker Dashboard, immediately below the "Current Status" section, you'll see a large circular button labeled **"NFC Health Check"**.

## How to Use It

### Step-by-Step:

1. **Navigate to Worker Dashboard**
   - Login with: `worker1` / `password123`
   - You'll see the "Current Status" card

2. **Locate the NFC Button**
   - Scroll down slightly below "Current Status"
   - You'll see a large purple circular button with a phone icon
   - Label: "NFC Health Check"

3. **Click the Button**
   - The button will show a spinning loader
   - Status messages will appear below the button
   - Follow on-screen instructions

4. **Grant Permissions**
   - **NFC Permission**: "Allow" (if your device has NFC)
   - **Camera Permission**: "Allow" for back camera access
   - Note: If NFC not supported, system uses simulated temperature

5. **Position for Heart Rate Reading**
   - Point your phone's **back camera** at a light source
   - Place your **finger firmly** on the back camera lens
   - Keep still for 10 seconds while scanning
   - The green light at the camera will be analyzed

6. **View Results**
   - Health check completes automatically
   - Results card displays:
     - **Temperature**: From NFC tag
     - **Heart Rate**: From camera analysis
     - **Risk Level**: 0=Safe, 1=Low, 2=High, 3=Critical
     - **DTHS Score**: Heat stress physiological score
     - **Message**: Quick assessment message
     - **Recommendation**: What to do next

7. **Dashboard Updates**
   - Recent Metrics section refreshes automatically
   - If risk ≥ 2, new alert appears in Recent Alerts
   - Supervisor dashboard also receives notification

## What the Risk Levels Mean

| Level | Status | Color | What to Do |
|-------|--------|-------|-----------|
| **0** | Safe ✅ | Green | Continue normal work |
| **1** | Low Risk ⚠️ | Orange | Increase water intake, monitor |
| **2** | High Risk ⚠️ | Red | Take immediate 15-min break |
| **3** | Critical 🚨 | Dark Red | Stop work, seek medical evaluation |

## Technical Details

### Temperature Reading (NFC)
- **What it measures**: Core body temperature
- **Source**: NFC tag/sensor attached to worker or device
- **Format**: °C (Celsius)
- **If unavailable**: System simulates reading (fallback)

### Heart Rate Detection (Camera)
- **What it measures**: Beats per minute (BPM)
- **Method**: Photoplethysmography (PPG) - light reflection analysis
- **Source**: Back camera analyzing finger on lens
- **Range**: 60-180 BPM (system validates realistic values)
- **Duration**: 10-second capture, analyzed in real-time

### Risk Calculation (AI/ML)
- **Algorithm**: Digital Twin + Random Forest Model
- **Inputs**: Temperature, Heart Rate, WBGT, Ambient Temp, Humidity, etc.
- **Output**: Risk Level (0-3) + DTHS Score + Recommendation
- **Processing**: <1 second response time

## Important Notes

⚠️ **Device Requirements:**
- **For NFC**: Smartphone with NFC hardware (most modern phones have this)
- **For Camera**: Any smartphone or device with back camera
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **Connection**: Must be on `http://localhost:5173` or HTTPS for security

⚠️ **Best Practices:**
- Use in **well-lit conditions** for accurate heart rate reading
- Keep **finger still** on camera for 10 seconds
- Perform checks **every 1-2 hours** in hot conditions
- Compare with other measurements if results seem off
- Always follow visual recommendations (take breaks, drink water)

⚠️ **Limitations:**
- **Not a medical device**: Results are for occupational screening only
- **No replacement for MD**: Consult healthcare if symptoms persist
- **Accuracy**: ±2-3 BPM and ±0.5°C typical variance
- **Privacy**: All data stored locally in heat stress database

## Testing the Feature

### Scenario 1: Normal Conditions (Safe)
- Temperature: 36.8°C
- Heart Rate: 72 BPM
- Expected Risk: 0 (Safe)
- Result: No alert generated

### Scenario 2: Warm Day (Low Risk)
- Temperature: 37.5°C
- Heart Rate: 95 BPM
- Expected Risk: 1 (Low Risk)
- Result: Notification to drink water

### Scenario 3: Hot Conditions (High Risk)
- Temperature: 38.8°C
- Heart Rate: 125 BPM
- Expected Risk: 2 (High Risk)
- Result: Alert appears, supervisor notified

### Scenario 4: Critical Conditions (Emergency)
- Temperature: 39.5°C
- Heart Rate: 150 BPM
- Expected Risk: 3 (Critical)
- Result: Urgent alert, immediate action recommended

## Troubleshooting

### "NFC not supported on this device"
- **Cause**: Device lacks NFC hardware
- **Solution**: Feature will use simulated temperature; camera heart rate still works
- **Action**: Continue with camera reading; supervisor can manually validate

### "Camera Error: Permission denied"
- **Cause**: You denied camera access
- **Solution**: 
  1. Go to browser settings
  2. Find "HeatGuard" or "localhost:5173"
  3. Change Camera permission to "Allow"
  4. Reload the page and try again

### "Heart rate shows 0 or very low number"
- **Cause**: Poor lighting or camera not positioned correctly
- **Solution**:
  1. Ensure bright light on back camera
  2. Place finger firmly on camera lens
  3. Keep completely still for 10 seconds
  4. Try again with better lighting

### Results don't appear in dashboard
- **Cause**: Polling refresh hasn't happened yet
- **Solution**: Wait 15 seconds for automatic update, or refresh page manually (F5)

### Supervisor doesn't see my alert
- **Cause**: Risk level is 0 or 1 (no alert triggered)
- **Solution**: Alerts only appear when risk ≥ 2; try another reading

## Frequently Asked Questions

**Q: Is my data private?**
A: All data stays in the HeatGuard system. NFC and camera data are not shared externally.

**Q: Can I use this without permission?**
A: Your supervisor/manager must authorize NFC Health Check usage. Obtain approval first.

**Q: How often should I use this?**
A: In normal conditions: once per shift. In hot conditions: every 1-2 hours.

**Q: What if my phone runs out of battery during scanning?**
A: System will show an error; ensure 20%+ battery before starting health check.

**Q: Can I share results with others?**
A: Results are automatically shared with your supervisor through the system. Screenshots are not recommended.

**Q: Is this replacing manual safety checks?**
A: No, this is a **supplement** to manual checks. Always report symptoms to supervisor.

## Advanced: API Integration

For developers integrating NFC Health Check via API:

```javascript
// Example: POST to backend
const payload = {
  worker_id: 'W_1',
  temperature: 37.5,
  heart_rate: 88,
  wbgt: 28,
  ambient_temp: 32,
  humidity: 60,
  radiant_heat: 500,
  break_duration: 0,
  bmi_bucket: 'medium',
  fitness_level: 'medium'
};

const response = await fetch('/nfc-check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
});

const result = await response.json();
// result.risk: 0-3
// result.dths_score: 0-1
// result.message: recommendation
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review NFC_FEATURE_GUIDE.md for technical details
3. Contact your IT/Safety department

---

**Version**: 1.0  
**Last Updated**: February 2025  
**Created for**: HeatGuard Worker Dashboard v1.0
