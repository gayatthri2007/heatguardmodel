import { useEffect, useState } from 'react';
import './SessionExpiredModal.css';

export function SessionExpiredModal() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    function onExpired() {
      setVisible(true);
    }
    window.addEventListener('sessionExpired', onExpired);
    return () => window.removeEventListener('sessionExpired', onExpired);
  }, []);

  if (!visible) return null;

  const handleConfirm = () => {
    setVisible(false);
    // ensure storage cleared and redirect
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  return (
    <div className="session-modal-overlay">
      <div className="session-modal">
        <h3>Session expired</h3>
        <p>Your session appears to have expired or become invalid. Please sign in again.</p>
        <div className="actions">
          <button className="primary" onClick={handleConfirm}>Sign in</button>
        </div>
      </div>
    </div>
  );
}

export default SessionExpiredModal;
