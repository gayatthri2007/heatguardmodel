import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, User, Bell } from 'lucide-react';
import { supervisorAPI, workerAPI } from '../../api/client';
import './Navbar.css';

export function Navbar({ user }) {
  const navigate = useNavigate();
  const [unread, setUnread] = useState(0);
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  useEffect(() => {
    let interval;
    async function fetchUnread() {
      try {
        if (user?.role === 'supervisor') {
          const res = await supervisorAPI.getDashboardStats();
          setUnread(res.data.unread_alerts || 0);
        } else if (user?.role === 'worker') {
          const res = await workerAPI.getAlerts(5);
          setUnread(res.data.filter(a=>!a.is_read).length);
        }
      } catch (e) {
        // ignore
      }
    }
    fetchUnread();
    interval = setInterval(fetchUnread, 15000);
    return () => clearInterval(interval);
  }, [user]);
  
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-brand">
          <span className="brand-icon">🔥</span>
          <span className="brand-text">HeatGuard</span>
        </div>
        
        <div className="navbar-actions">
          {unread > 0 && (
            <div className="alert-badge">
              <Bell size={20} />
              <span className="badge-count">{unread}</span>
            </div>
          )}
          <div className="user-info">
            <User size={20} />
            <span>{user?.username}</span>
          </div>
          <button onClick={handleLogout} className="logout-btn">
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
