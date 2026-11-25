import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.user import User
from models.worker import Worker, WorkerMetrics
from models.alert import Alert
from sqlalchemy import func

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/api/supervisor')

@supervisor_bp.route('/workers', methods=['GET'])
@jwt_required()
def get_all_workers():
    """Get all workers with current status"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'supervisor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    workers = Worker.query.all()
    
    result = []
    for worker in workers:
        latest_metric = WorkerMetrics.query.filter_by(
            worker_id=worker.id
        ).order_by(WorkerMetrics.timestamp.desc()).first()
        
        result.append({
            'id': worker.id,
            'worker_id': worker.worker_id,
            'zone': worker.zone,
            'user': worker.user.to_dict(),
            'current_risk': latest_metric.risk_level if latest_metric else 0,
            'current_temp': latest_metric.body_temp_post if latest_metric else None,
            'current_hr': latest_metric.heart_rate_post if latest_metric else None,
            'last_update': latest_metric.timestamp.isoformat() if latest_metric else None
        })
    
    return jsonify(result), 200

@supervisor_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'supervisor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_workers = Worker.query.count()
    
    # Count high-risk workers
    high_risk_workers = db.session.query(Worker.id).join(WorkerMetrics).filter(
        WorkerMetrics.risk_level >= 2
    ).distinct().count()
    
    # Unread alerts count
    unread_alerts = Alert.query.filter_by(is_read=False).count()
    
    # Latest alerts
    latest_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()
    
    return jsonify({
        'total_workers': total_workers,
        'high_risk_workers': high_risk_workers,
        'unread_alerts': unread_alerts,
        'recent_alerts': [a.to_dict() for a in latest_alerts]
    }), 200

@supervisor_bp.route('/worker/<int:worker_id>/history', methods=['GET'])
@jwt_required()
def get_worker_history(worker_id):
    """Get complete worker history"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'supervisor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    worker = Worker.query.get(worker_id)
    
    if not worker:
        return jsonify({'error': 'Worker not found'}), 404
    
    limit = request.args.get('limit', 100, type=int)
    metrics = WorkerMetrics.query.filter_by(worker_id=worker_id).order_by(
        WorkerMetrics.timestamp.desc()
    ).limit(limit).all()
    
    return jsonify({
        'worker': worker.to_dict(),
        'metrics': [m.to_dict() for m in metrics]
    }), 200

@supervisor_bp.route('/zones', methods=['GET'])
@jwt_required()
def get_zones_overview():
    """Get overview by zones"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'supervisor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    zones = db.session.query(Worker.zone).distinct().all()
    result = []
    
    for (zone,) in zones:
        workers_in_zone = Worker.query.filter_by(zone=zone).all()
        zone_temp = db.session.query(func.avg(WorkerMetrics.ambient_temp)).join(
            Worker
        ).filter(Worker.zone == zone).scalar() or 0
        
        high_risk = sum(1 for w in workers_in_zone if w.metrics and max(
            (m.risk_level for m in w.metrics), default=0
        ) >= 2)
        
        result.append({
            'zone': zone,
            'total_workers': len(workers_in_zone),
            'high_risk_workers': high_risk,
            'avg_ambient_temp': round(float(zone_temp), 1)
        })
    
    return jsonify(result), 200


# supervisor alert management helper
@supervisor_bp.route('/alerts/<int:alert_id>/read', methods=['PUT'])
@jwt_required()
def mark_alert_read(alert_id):
    """Supervisor can mark an alert as read so it no longer shows as unread in
    dashboard statistics.  This helper is called from the frontend when the
    user clicks a "mark read" button on a notification.
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'supervisor':
        return jsonify({'error': 'Unauthorized'}), 403

    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404

    alert.is_read = True
    db.session.commit()
    return jsonify({'message': 'Alert marked as read'}), 200
