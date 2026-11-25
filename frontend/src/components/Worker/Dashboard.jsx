import { useEffect, useState } from 'react';
import { workerAPI, predictionAPI, quickPredict } from '../../api/client';
import { AlertCircle, Heart, Thermometer, Wind } from 'lucide-react';
import { NFCHealthCheck } from './NFCHealthCheck';
import './Dashboard.css';

export function WorkerDashboard() {
  const [profile, setProfile] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showPredictForm, setShowPredictForm] = useState(false);
  const [prevAlertId, setPrevAlertId] = useState(null); // track for notifications

  // beep helper
  const playBeep = () => {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      osc.type = 'sine';
      osc.frequency.value = 1000;
      osc.connect(ctx.destination);
      osc.start();
      setTimeout(() => {
        osc.stop();
        ctx.close();
      }, 200);
    } catch (e) {
      console.warn('beep failed', e);
    }
  };
  const [formData, setFormData] = useState({
    body_temp_post: 37,
    body_temp_pre: 36.5,
    heart_rate_post: 80,
    heart_rate_pre: 70,
    wbgt: 28,
    ambient_temp: 32,
    humidity: 60,
    radiant_heat: 500,
    break_duration: 0
  });
  
  useEffect(() => {
    loadData();
    // start polling every 15 seconds so dashboard stays up to date
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);
  
  const loadData = async () => {
    try {
      const [profileRes, metricsRes, alertsRes] = await Promise.all([
        workerAPI.getProfile(),
        workerAPI.getMetrics(10),
        workerAPI.getAlerts(10)
      ]);

      setProfile(profileRes.data);
      setMetrics(metricsRes.data);

      const newAlerts = alertsRes.data;
      // if we already had a previous alert id and it changed, notify user
      if (prevAlertId && newAlerts.length && newAlerts[0].id !== prevAlertId) {
        const latest = newAlerts[0];
        // audio + browser notification
        playBeep();
        window.alert(`🔔 New alert: ${latest.message}`);
      }
      setPrevAlertId(newAlerts.length ? newAlerts[0].id : null);
      setAlerts(newAlerts);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handlePredictSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      try {
        response = await predictionAPI.predict(formData);
      } catch (err) {
        console.warn('predictionAPI failed, falling back to quickPredict', err);
        // use lightweight no-auth endpoint; include worker_id so metrics persist
        const fallbackData = {
          ...formData,
          worker_id: profile?.worker_id
        };
        response = await quickPredict(fallbackData);
      }

      setPredictionResult({
        ...response.data,
        input: { ...formData }
      });
      alert(`Risk Level: ${response.data.risk_level} (${response.data.risk_label || ''})\n${response.data.message}`);
      setShowPredictForm(false);
      loadData();
    } catch (error) {
      console.error('Prediction error', error);
      alert('Error making prediction: ' + (error.response?.data?.error || error.message));
    }
  };

  const [quickResult, setQuickResult] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);

  const handleQuickPredict = async () => {
    try {
      const response = await quickPredict(formData);
      setQuickResult(response.data);
    } catch (error) {
      setQuickResult({ error: error.response?.data || error.message });
    }
  };
  
  const getRiskColor = (level) => {
    const colors = {
      0: '#81c784',
      1: '#ffb74d',
      2: '#e57373',
      3: '#c62828'
    };
    return colors[level] || '#757575';
  };

  const handleNFCResultsUpdate = (nfcData) => {
    // Update the form data with NFC readings
    setFormData(prev => ({
      ...prev,
      body_temp_post: nfcData.body_temp_post,
      heart_rate_post: nfcData.heart_rate_post
    }));
    // Reload dashboard to show new metrics and alerts
    setTimeout(loadData, 1000);
  };
  
  if (loading) return <div className="loader">Loading...</div>;
  
  const latestMetric = metrics[0];
  const latestAlert = alerts[0];
  
  const markAlertAsRead = async (id) => {
    try {
      await workerAPI.markAlertRead(id);
      loadData();
    } catch (e) {
      console.error('Unable to mark alert read', e);
    }
  };

  return (
    <div className="worker-dashboard">
      <div className="dashboard-header">
        <h1>Good Morning, {profile?.user?.username}!</h1>
        <p>Stay safe and hydrated today</p>
      </div>

      
      {/* Current Status */}
      <div className="card status-card">
        <h2>Current Status</h2>
        <div className="grid grid-3">
          <div className="status-item">
            <Wind size={24} />
            <label>Current Zone</label>
            <value>{profile?.zone}</value>
          </div>
          <div className="status-item">
            <Thermometer size={24} />
            <label>Ambient Temperature</label>
            <value>{latestMetric?.ambient_temp || 'N/A'}°C</value>
          </div>
          <div className="status-item">
            <AlertCircle size={24} />
            <label>Hydration Reminder</label>
            <value>Drink water in 15 min</value>
          </div>
        </div>
      </div>

      {/* NFC Health Check Feature */}
      <NFCHealthCheck onResultsUpdate={handleNFCResultsUpdate} />
      
      {/* Latest Alert */}
      {latestAlert && (
        <div className={`alert alert-${['success', 'warning', 'warning', 'danger'][latestAlert.risk_level]}`}>
          <AlertCircle size={20} />
          <div>
            <strong>{latestAlert.message}</strong>
            <p>{new Date(latestAlert.created_at).toLocaleString()}</p>
          </div>
        </div>
      )}

      {/* All Alerts */}
      {alerts.length > 0 && (
        <div className="card alerts-card">
          <h3>Recent Alerts</h3>
          {alerts.map((a) => (
            <div key={a.id} className={`alert alert-${['success', 'warning', 'warning', 'danger'][a.risk_level]}`}>
              <div style={{flex:1}}>
                <strong>{a.message}</strong>
                <p style={{fontSize:'12px',margin:0}}>{new Date(a.created_at).toLocaleString()}</p>
              </div>
              {!a.is_read && (
                <button className="secondary" onClick={() => markAlertAsRead(a.id)}>
                  Mark read
                </button>
              )}
            </div>
          ))}
        </div>
      )}
      
      {/* Predict Heat Stress */}
      <div className="card">
        <h3>Digital Twin Simulation</h3>
        {!showPredictForm ? (
          <button 
            onClick={() => setShowPredictForm(true)}
            className="primary"
          >
            Start Prediction
          </button>
        ) : (
          <form onSubmit={handlePredictSubmit} className="predict-form">
            <div className="form-row">
              <div>
                <label>Body Temp (Post °C)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.body_temp_post}
                  onChange={(e) => setFormData({...formData, body_temp_post: parseFloat(e.target.value)})}
                  required
                />
              </div>
              <div>
                <label>Heart Rate (Post bpm)</label>
                <input
                  type="number"
                  value={formData.heart_rate_post}
                  onChange={(e) => setFormData({...formData, heart_rate_post: parseFloat(e.target.value)})}
                  required
                />
              </div>
            </div>
            
            <div className="form-row">
              <div>
                <label>WBGT (°C)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.wbgt}
                  onChange={(e) => setFormData({...formData, wbgt: parseFloat(e.target.value)})}
                  required
                />
              </div>
              <div>
                <label>Ambient Temp (°C)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.ambient_temp}
                  onChange={(e) => setFormData({...formData, ambient_temp: parseFloat(e.target.value)})}
                  required
                />
              </div>
            </div>
            
            <div className="form-row">
              <div>
                <label>Humidity (%)</label>
                <input
                  type="number"
                  value={formData.humidity}
                  onChange={(e) => setFormData({...formData, humidity: parseFloat(e.target.value)})}
                  required
                />
              </div>
              <div>
                <label>Break Duration (min)</label>
                <input
                  type="number"
                  value={formData.break_duration}
                  onChange={(e) => setFormData({...formData, break_duration: parseInt(e.target.value)})}
                  required
                />
              </div>
            </div>
            
            <div className="form-actions">
              <button type="submit" className="primary">Predict</button>
              <button type="button" onClick={() => setShowPredictForm(false)}>Cancel</button>
              <button type="button" className="secondary" onClick={handleQuickPredict}>Quick Model (No Auth)</button>
            </div>
          </form>
        )}
        {quickResult && (
          <div className="card">
            <h4>Quick Model Result</h4>
            {quickResult.error ? (
              <pre className="error">{JSON.stringify(quickResult.error, null, 2)}</pre>
            ) : (
              <pre>{JSON.stringify(quickResult, null, 2)}</pre>
            )}
          </div>
        )}
        {predictionResult && (
          <div className="card prediction-summary">
            <h4>Last Prediction</h4>
            <p><strong>Risk Level:</strong> {predictionResult.risk_level}</p>
            <p><strong>Score:</strong> {predictionResult.dths_score}</p>
            <p><strong>Message:</strong> {predictionResult.message}</p>
            <p><strong>Recommendation:</strong> {predictionResult.recommendation}</p>
          </div>
        )}
      </div>
      
      {/* Recent Metrics */}
      <div className="card">
        <h3>Recent Metrics</h3>
        <div className="metrics-table">
          {metrics.slice(0, 5).map((m) => (
            <div key={m.id} className="metric-row" style={{borderLeftColor: getRiskColor(m.risk_level)}}>
              <div>
                <strong>Risk Level: {m.risk_level}</strong>
                <p>{new Date(m.timestamp).toLocaleString()}</p>
              </div>
              <div>
                <span>Temp: {m.body_temp_post}°C</span>
                <span>HR: {m.heart_rate_post} bpm</span>
              </div>
              <div>
                <span className="dths-score">DTHS: {m.dths_score.toFixed(3)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
