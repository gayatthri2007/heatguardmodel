import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.user import User
from models.worker import Worker, WorkerMetrics
from models.alert import Alert

worker_bp = Blueprint('worker', __name__, url_prefix='/api/worker')

@worker_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get worker profile"""
    user_id = int(get_jwt_identity())
    worker = Worker.query.filter_by(user_id=user_id).first()
    
    if not worker:
        return jsonify({'error': 'Worker not found'}), 404
    
    return jsonify(worker.to_dict()), 200

@worker_bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Get worker metrics history"""
    user_id = int(get_jwt_identity())
    worker = Worker.query.filter_by(user_id=user_id).first()
    
    if not worker:
        return jsonify({'error': 'Worker not found'}), 404
    
    limit = request.args.get('limit', 20, type=int)
    metrics = WorkerMetrics.query.filter_by(worker_id=worker.id).order_by(
        WorkerMetrics.timestamp.desc()
    ).limit(limit).all()
    
    return jsonify([m.to_dict() for m in metrics]), 200

@worker_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get worker alerts"""
    user_id = int(get_jwt_identity())
    worker = Worker.query.filter_by(user_id=user_id).first()
    
    if not worker:
        return jsonify({'error': 'Worker not found'}), 404
    
    limit = request.args.get('limit', 10, type=int)
    alerts = Alert.query.filter_by(worker_id=worker.id).order_by(
        Alert.created_at.desc()
    ).limit(limit).all()
    
    return jsonify([a.to_dict() for a in alerts]), 200

@worker_bp.route('/alerts/<int:alert_id>/read', methods=['PUT'])
@jwt_required()
def mark_alert_read(alert_id):
    """Mark alert as read"""
    alert = Alert.query.get(alert_id)
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    alert.is_read = True
    db.session.commit()
    
    return jsonify({'message': 'Alert marked as read'}), 200
