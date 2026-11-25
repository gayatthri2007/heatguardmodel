import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import db
from datetime import datetime

class Worker(db.Model):
    __tablename__ = 'workers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    worker_id = db.Column(db.String(50), unique=True, nullable=False)
    zone = db.Column(db.String(100), nullable=False)
    bmi_bucket = db.Column(db.String(20))  # low, medium, high
    fitness_level = db.Column(db.String(20))  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='worker')
    
    def to_dict(self):
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'zone': self.zone,
            'bmi_bucket': self.bmi_bucket,
            'fitness_level': self.fitness_level
        }

class WorkerMetrics(db.Model):
    __tablename__ = 'worker_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body_temp_post = db.Column(db.Float)
    heart_rate_post = db.Column(db.Float)
    body_temp_pre = db.Column(db.Float)
    heart_rate_pre = db.Column(db.Float)
    wbgt = db.Column(db.Float)
    ambient_temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    radiant_heat = db.Column(db.Float)
    break_duration = db.Column(db.Integer, default=0)
    risk_level = db.Column(db.Integer)  # 0-3
    dths_score = db.Column(db.Float)
    
    worker = db.relationship('Worker', backref='metrics')
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'body_temp_post': self.body_temp_post,
            'body_temp_pre': self.body_temp_pre,
            'heart_rate_post': self.heart_rate_post,
            'heart_rate_pre': self.heart_rate_pre,
            'wbgt': self.wbgt,
            'ambient_temp': self.ambient_temp,
            'humidity': self.humidity,
            'radiant_heat': self.radiant_heat,
            'break_duration': self.break_duration,
            'risk_level': self.risk_level,
            'dths_score': self.dths_score
        }
