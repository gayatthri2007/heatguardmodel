import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../api/client';
import './Login.css';

export function Login({ onLogin }) {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'worker',
    zone: 'Zone A',
    bmi_bucket: 'medium',
    fitness_level: 'medium'
  });
  
  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      let response;
      if (isLogin) {
        response = await authAPI.login({
          username: formData.username,
          password: formData.password
        });
      } else {
        response = await authAPI.register(formData);
      }
      console.log('auth response', response.data);
      // store token for later calls
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      console.log('stored user', response.data.user);
      // update parent state so route guards don't immediately redirect
      if (onLogin) {
        onLogin(response.data.user);
      }
      
      navigate(response.data.user.role === 'supervisor' ? '/supervisor' : '/worker');
    } catch (err) {
      console.error('login/register error', err);
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <h1>🔥 HeatGuard</h1>
          <p>Worker Heat Safety Monitoring System</p>
        </div>
        
        {error && <div className="alert alert-danger">{error}</div>}
        
        <div className="login-tabs">
          <button 
            className={`tab ${isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button 
            className={`tab ${!isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Enter username"
            />
          </div>
          
          {!isLogin && (
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="Enter email"
              />
            </div>
          )}
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter password"
            />
          </div>
          
          {!isLogin && (
            <>
              <div className="form-group">
                <label>Role</label>
                <select name="role" value={formData.role} onChange={handleChange}>
                  <option value="worker">Worker</option>
                  <option value="supervisor">Supervisor</option>
                </select>
              </div>
              
              {formData.role === 'worker' && (
                <>
                  <div className="form-group">
                    <label>Zone</label>
                    <input
                      type="text"
                      name="zone"
                      value={formData.zone}
                      onChange={handleChange}
                      placeholder="e.g., Zone A - Construction"
                    />
                  </div>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label>BMI Bucket</label>
                      <select name="bmi_bucket" value={formData.bmi_bucket} onChange={handleChange}>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                    
                    <div className="form-group">
                      <label>Fitness Level</label>
                      <select name="fitness_level" value={formData.fitness_level} onChange={handleChange}>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                  </div>
                </>
              )}
            </>
          )}
          
          <button type="submit" className="primary login-btn" disabled={loading}>
            {loading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
          </button>
        </form>
        
        <p className="disclaimer">
          ℹ️ This prototype demonstrates heat safety monitoring with OSHA compliance
        </p>
      </div>
    </div>
  );
}
