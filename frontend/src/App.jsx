import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { WorkerDashboard } from './components/Worker/Dashboard';
import { SupervisorDashboard } from './components/Supervisor/Dashboard';
import { Navbar } from './components/Common/Navbar';
import SessionExpiredModal from './components/Common/SessionExpiredModal';
import './styles/global.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);
  
  if (loading) return <div className="loader">Loading...</div>;
  
  return (
    <BrowserRouter>
      {user && <Navbar user={user} />}
      <SessionExpiredModal />
      <Routes>
        <Route
          path="/login"
          element={!user ? <Login onLogin={setUser} /> : <Navigate to={user.role === 'supervisor' ? '/supervisor' : '/worker'} />}
        />
        <Route
          path="/worker"
          element={
            (user?.role === 'worker' || (JSON.parse(localStorage.getItem('user') || '{}').role === 'worker'))
              ? <WorkerDashboard />
              : <Navigate to="/login" />
          }
        />
        <Route
          path="/supervisor"
          element={
            (user?.role === 'supervisor' || (JSON.parse(localStorage.getItem('user') || '{}').role === 'supervisor'))
              ? <SupervisorDashboard />
              : <Navigate to="/login" />
          }
        />
        <Route path="/" element={<Navigate to={user ? (user.role === 'supervisor' ? '/supervisor' : '/worker') : '/login'} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
