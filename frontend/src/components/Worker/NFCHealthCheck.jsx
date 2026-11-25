import { useState, useRef } from "react";
import { Smartphone, Loader } from "lucide-react";
import { ref, get } from "firebase/database";
import { database } from "../../firebase";
import "./NFCHealthCheck.css";

export function NFCHealthCheck({ onResultsUpdate }) {

  const workerId = "016FB302"; // 🔥 Make sure this matches Firebase

  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // 🔥 Simple heart rate simulation (replace with your OpenCV if needed)
  const detectHeartRate = async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const simulatedHR = 60 + Math.floor(Math.random() * 10);
        resolve(simulatedHR);
      }, 2000);
    });
  };

  const handleHealthCheck = async () => {
    setIsScanning(true);
    setError(null);
    setResult(null);
    setSuccessMessage(null);

    try {

      // 🔥 1. READ LIVE DATA FROM FIREBASE
      const workerRef = ref(database, `workers/${workerId}`);
      const snapshot = await get(workerRef);
      const liveData = snapshot.val();

      console.log("🔥 Firebase live data:", liveData);

      if (!liveData) {
        throw new Error("No data found for this worker in Firebase.");
      }

      const bodyTemp = liveData.bodyTemperature;
      const humidity = liveData.humidity;
      const airTemp = liveData.airTemp;

      if (bodyTemp === undefined) {
        throw new Error("bodyTemperature field missing in Firebase.");
      }

      // 🔥 2. Detect Heart Rate
      const heartRate = await detectHeartRate();

      // 🔥 3. Send to backend
      const response = await fetch("http://localhost:5000/nfc-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          worker_id: workerId,
          temperature: bodyTemp,
          heart_rate: heartRate,
          wbgt: 28,
          ambient_temp: airTemp,
          humidity: humidity,
          radiant_heat: 500
        })
      });

      const data = await response.json();

      // 🔥 4. Display EXACT Firebase temperature
      setResult({
        temperature: bodyTemp,
        heart_rate: heartRate,
        risk: data.risk_level,
        risk_label: data.risk_label,
        dths_score: data.dths_score,
        message: data.message,
        recommendation: data.recommendation
      });

      const ts = new Date();
      setSuccessMessage(
        `Worker entry recorded at ${ts.toLocaleString()} — HR: ${heartRate} BPM`
      );

      if (onResultsUpdate) {
        onResultsUpdate({
          body_temp_post: bodyTemp,
          heart_rate_post: heartRate,
          risk_level: data.risk_level,
          dths_score: data.dths_score
        });
      }

    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="nfc-health-check-wrapper">

      <button
        className={`nfc-button ${isScanning ? "scanning" : ""}`}
        onClick={handleHealthCheck}
        disabled={isScanning}
      >
        {isScanning ? <Loader size={32} className="spinner" /> : <Smartphone size={32} />}
        <span>NFC Health Check</span>
      </button>

      {error && (
        <div className="alert alert-danger" style={{ marginTop: 15 }}>
          ❌ {error}
        </div>
      )}

      {result && (
        <div className="nfc-result-card">
          <h4>Health Check Results</h4>

          <div className="result-grid">
            <div className="result-item">
              <label>Temperature</label>
              <value>{Number(result.temperature).toFixed(1)}°C</value>
            </div>

            <div className="result-item">
              <label>Heart Rate</label>
              <value>{result.heart_rate} BPM</value>
            </div>

            <div className="result-item">
              <label>Risk Level</label>
              <value className={`risk-${result.risk}`}>
                {result.risk} ({result.risk_label})
              </value>
            </div>

            <div className="result-item">
              <label>DTHS Score</label>
              <value>{Number(result.dths_score).toFixed(3)}</value>
            </div>
          </div>

          <p className="result-message">{result.message}</p>
          <p className="result-recommendation">
            <strong>Recommendation:</strong> {result.recommendation}
          </p>
        </div>
      )}

      {successMessage && (
        <div className="alert alert-success" style={{ marginTop: 15 }}>
          ✅ {successMessage}
        </div>
      )}

      <video ref={videoRef} style={{ display: "none" }} />
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
}