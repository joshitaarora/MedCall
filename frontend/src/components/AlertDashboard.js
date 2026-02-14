import React from 'react';
import { AlertTriangle, Calendar, AlertCircle, Shield } from 'lucide-react';
import './AlertDashboard.css';

function AlertDashboard({ alerts }) {
  const getAlertIcon = (type) => {
    switch (type) {
      case 'adverse_event':
        return <AlertTriangle size={20} />;
      case 'appointment':
        return <Calendar size={20} />;
      case 'emergency':
        return <AlertCircle size={20} />;
      case 'sentiment_mismatch':
        return <Shield size={20} />;
      default:
        return <AlertTriangle size={20} />;
    }
  };

  const getSeverityClass = (severity) => {
    return `alert-card severity-${severity}`;
  };

  const getAlertStats = () => {
    const stats = {
      total: alerts.length,
      critical: alerts.filter(a => a.severity === 'critical').length,
      high: alerts.filter(a => a.severity === 'high').length,
      medium: alerts.filter(a => a.severity === 'medium').length,
    };
    return stats;
  };

  const stats = getAlertStats();

  return (
    <div className="alert-dashboard">
      <div className="dashboard-header">
        <h2>Alert Dashboard</h2>
        <div className="alert-count">{alerts.length} Alerts</div>
      </div>

      {stats.total > 0 && (
        <div className="alert-stats">
          <div className="stat-card critical">
            <div className="stat-number">{stats.critical}</div>
            <div className="stat-label">Critical</div>
          </div>
          <div className="stat-card high">
            <div className="stat-number">{stats.high}</div>
            <div className="stat-label">High</div>
          </div>
          <div className="stat-card medium">
            <div className="stat-number">{stats.medium}</div>
            <div className="stat-label">Medium</div>
          </div>
        </div>
      )}

      <div className="alerts-container">
        {alerts.length === 0 ? (
          <div className="no-alerts">
            <Shield size={48} color="#d1d5db" />
            <p>No alerts yet</p>
            <p className="sub-text">Alerts will appear here in real-time</p>
          </div>
        ) : (
          <div className="alerts-list">
            {[...alerts].reverse().map((alert, index) => (
              <div key={index} className={getSeverityClass(alert.severity)}>
                <div className="alert-header">
                  <div className="alert-icon">
                    {getAlertIcon(alert.type)}
                  </div>
                  <div className="alert-type">{alert.type.replace('_', ' ').toUpperCase()}</div>
                  <div className={`severity-badge ${alert.severity}`}>
                    {alert.severity}
                  </div>
                </div>
                
                <div className="alert-message">
                  {alert.message}
                </div>
                
                {alert.action && (
                  <div className="alert-action">
                    <strong>Action:</strong> {alert.action}
                  </div>
                )}
                
                <div className="alert-timestamp">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AlertDashboard;
