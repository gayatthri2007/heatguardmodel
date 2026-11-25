import os
import pandas as pd
from flask import Blueprint, jsonify, request

demo_bp = Blueprint('demo', __name__, url_prefix='/api/demo')

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'merged_with_risk.csv'))

def load_df():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()


@demo_bp.route('/supervisor/stats', methods=['GET'])
def demo_supervisor_stats():
    df = load_df()
    total_workers = df['worker_id'].nunique() if not df.empty else 0
    high_risk_workers = df[df['risk_label'] >= 2]['worker_id'].nunique() if not df.empty else 0
    recent_alerts = []
    return jsonify({
        'total_workers': int(total_workers),
        'high_risk_workers': int(high_risk_workers),
        'unread_alerts': 0,
        'recent_alerts': recent_alerts
    }), 200


@demo_bp.route('/workers', methods=['GET'])
def demo_workers():
    df = load_df()
    if df.empty:
        return jsonify([]), 200

    # for each worker return latest row
    last = df.sort_values('worker_id').groupby('worker_id').last().reset_index()
    result = []
    for _, row in last.iterrows():
        result.append({
            'worker_id': int(row['worker_id']),
            'zone': int(row.get('zone_id', 0)),
            'current_risk': int(row.get('risk_label', 0)),
            'current_temp': float(row.get('body_temp_post', None)),
            'current_hr': float(row.get('heart_rate_post', None))
        })
    return jsonify(result), 200


@demo_bp.route('/worker/<int:worker_id>/history', methods=['GET'])
def demo_worker_history(worker_id):
    df = load_df()
    if df.empty:
        return jsonify({'worker': {}, 'metrics': []}), 200

    wdf = df[df['worker_id'] == worker_id]
    if wdf.empty:
        return jsonify({'worker': {}, 'metrics': []}), 200

    metrics = wdf.to_dict(orient='records')
    worker_info = metrics[0]
    return jsonify({'worker': worker_info, 'metrics': metrics}), 200
