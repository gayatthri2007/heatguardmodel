import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from models.user import User
from models.worker import Worker, WorkerMetrics
from models.alert import Alert
from ml_engine.twin_engine import digital_twin, get_risk_message, get_recommendation, get_risk_label

pred_bp = Blueprint('predictions', __name__, url_prefix='/api/predictions')

@pred_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """Predict heat stress for a worker"""
    user_id = get_jwt_identity()
    data = request.json
    
    try:
        # Get or find worker
        if 'worker_id' in data:
            worker = Worker.query.filter_by(worker_id=data['worker_id']).first()
        else:
            worker = Worker.query.filter_by(user_id=user_id).first()
        
        if not worker:
            return jsonify({'error': 'Worker not found'}), 404
        
        # Prepare input data
        input_data = {
            'body_temp_post': float(data.get('body_temp_post', 37)),
            'body_temp_pre': float(data.get('body_temp_pre', 37)),
            'heart_rate_post': float(data.get('heart_rate_post', 70)),
            'heart_rate_pre': float(data.get('heart_rate_pre', 70)),
            'wbgt': float(data.get('wbgt', 25)),
            'ambient_temp': float(data.get('ambient_temp', 25)),
            'humidity': float(data.get('humidity', 50)),
            'radiant_heat': float(data.get('radiant_heat', 400)),
            'break_duration': int(data.get('break_duration', 0)),
            'bmi_bucket': worker.bmi_bucket,
            'fitness_level': worker.fitness_level
        }
        
        # Get prediction
        risk_level, dths_score = digital_twin(input_data)
        
        # Save metrics
        metrics = WorkerMetrics(
            worker_id=worker.id,
            body_temp_post=input_data['body_temp_post'],
            body_temp_pre=input_data['body_temp_pre'],
            heart_rate_post=input_data['heart_rate_post'],
            heart_rate_pre=input_data['heart_rate_pre'],
            wbgt=input_data['wbgt'],
            ambient_temp=input_data['ambient_temp'],
            humidity=input_data['humidity'],
            radiant_heat=input_data['radiant_heat'],
            break_duration=input_data['break_duration'],
            risk_level=risk_level,
            dths_score=dths_score
        )
        db.session.add(metrics)
        
        # Create alert if risk is high
        if risk_level >= 2:
            alert = Alert(
                worker_id=worker.id,
                risk_level=risk_level,
                message=get_risk_message(risk_level)
            )
            db.session.add(alert)
        
        db.session.commit()
        
        return jsonify({
            'risk_level': risk_level,
            'risk_label': get_risk_label(risk_level),
            'dths_score': dths_score,
            'message': get_risk_message(risk_level),
            'recommendation': get_recommendation(risk_level)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500