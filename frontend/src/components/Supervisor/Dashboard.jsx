import { useEffect, useState } from 'react';
import { supervisorAPI } from '../../api/client';
import { AlertCircle, Users, TrendingUp, Eye } from 'lucide-react';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

export function SupervisorDashboard() {
  const [stats, setStats] = useState(null);
  const [workers, setWorkers] = useState([]);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [prevAlertCount, setPrevAlertCount] = useState(0);
  const [showNewAlertBanner, setShowNewAlertBanner] = useState(false);

  // simple beep helper
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
  
  useEffect(() => {
    loadData();
    // refresh stats periodically
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);
  
  const loadData = async () => {
    try {
      setError(null);
      const [statsRes, workersRes, zonesRes] = await Promise.all([
        supervisorAPI.getDashboardStats(),
        supervisorAPI.getAllWorkers(),
        supervisorAPI.getZonesOverview()
      ]);
      
      // check for new alerts
      if (statsRes.data) {
        const incoming = statsRes.data.recent_alerts.length;
        if (prevAlertCount && incoming > prevAlertCount) {
          // new alert received
          playBeep();
          setShowNewAlertBanner(true);
          setTimeout(() => setShowNewAlertBanner(false), 5000);
        }
        setPrevAlertCount(incoming);
      }
      setStats(statsRes.data);
      setWorkers(workersRes.data);
      setZones(zonesRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      setError(error.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };
  
  const markAlertRead = async (id) => {
    try {
      await supervisorAPI.markAlertRead(id);
      loadData();
    } catch (err) {
      console.error('failed to mark alert', err);
    }
  };

  if (loading) return <div className="loader">Loading...</div>;

  // banner will be rendered inside main layout below
  
  if (error) {
    return (
      <div className="supervisor-dashboard">
        <div className="error-container">
          <AlertCircle size={48} />
          <h2>Error Loading Dashboard</h2>
          <p>{error}</p>
          <button onClick={loadData} className="primary">Retry</button>
        </div>
      </div>
    );
  }
  
  if (!stats) {
    return (
      <div className="supervisor-dashboard">
        <div className="error-container">
          <AlertCircle size={48} />
          <h2>No Data Available</h2>
          <p>Unable to load dashboard statistics.</p>
          <button onClick={loadData} className="primary">Retry</button>
        </div>
      </div>
    );
  }
  
  const riskData = [
    { name: 'Safe', value: stats.total_workers - stats.high_risk_workers, fill: '#81c784' },
    { name: 'High Risk', value: stats.high_risk_workers, fill: '#e57373' }
  ];
  
  return (
    <div className="supervisor-dashboard">
      {showNewAlertBanner && (
        <div className="new-alert-banner">
          🔔 New alert received!
        </div>
      )}
      <div className="dashboard-header">
        <h1>Supervisor Dashboard</h1>
        <p>Monitor all workers and zones</p>
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-4">
        <div className="stat-card">
          <div className="stat-icon users">
            <Users size={32} />
          </div>
          <div className="stat-content">
            <h3>{stats.total_workers}</h3>
            <p>Total Workers</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon alerts">
            <AlertCircle size={32} />
          </div>
          <div className="stat-content">
            <h3>{stats.high_risk_workers}</h3>
            <p>High Risk Workers</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon warnings">
            <TrendingUp size={32} />
          </div>
          <div className="stat-content">
            <h3>{stats.recent_alerts.length}</h3>
            <p>Recent Alerts</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon view">
            <Eye size={32} />
          </div>
          <div className="stat-content">
            <h3>{stats.unread_alerts}</h3>
            <p>Unread Alerts</p>
          </div>
        </div>
      </div>
      
      {/* Charts */}
      <div className="grid grid-2">
        <div className="card">
          <h3>Risk Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({name, value}) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div className="card">
          <h3>Zone Overview</h3>
          <div className="zones-list">
            {zones.map((zone) => (
              <div key={zone.zone} className="zone-item">
                <div>
                  <strong>{zone.zone}</strong>
                  <p>{zone.total_workers} workers</p>
                </div>
                <div className="zone-stats">
                  <span className="temp">{zone.avg_ambient_temp}°C</span>
                  <span className={`risk ${zone.high_risk_workers > 0 ? 'danger' : 'safe'}`}>
                    {zone.high_risk_workers} at risk
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Recent Alerts */}
      <div className="card">
        <h3>Recent Alerts & Warnings</h3>
        <button className="secondary">View Analytics</button>
        <div className="alerts-list">
          {stats.recent_alerts.map((alert) => (
            <div key={alert.id} className={`alert-item alert-level-${alert.risk_level}`}>
              <div className="alert-header">
                <strong>{alert.message}</strong>
                <span className="time">
                  {new Date(alert.created_at).toLocaleTimeString()}
                </span>
              </div>
              <p className="alert-zone">Worker ID: {alert.worker_id}</p>
              {!alert.is_read && (
                <button className="secondary mark-read-btn" onClick={() => markAlertRead(alert.id)}>
                  Mark read
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
      
      {/* Workers List */}
      <div className="card">
        <h3>Workers Status</h3>
        <div className="workers-table">
          <div className="table-header">
            <div>Worker ID</div>
            <div>Zone</div>
            <div>Status</div>
            <div>Temp</div>
            <div>HR</div>
            <div>Last Update</div>
          </div>
          {workers.map((worker) => (
            <div key={worker.id} className="table-row">
              <div className="worker-name">
                <strong>{worker.worker_id}</strong>
                <small>{worker.user.username}</small>
              </div>
              <div>{worker.zone}</div>
              <div>
                <span className={`status-badge status-${worker.current_risk}`}>
                  Level {worker.current_risk}
                </span>
              </div>
              <div>{worker.current_temp ? worker.current_temp.toFixed(1) + '°C' : 'N/A'}</div>
              <div>{worker.current_hr ? worker.current_hr + ' bpm' : 'N/A'}</div>
              <div className="time-ago">
                {worker.last_update ? new Date(worker.last_update).toLocaleTimeString() : 'Never'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
