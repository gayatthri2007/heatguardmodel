import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import config
from database.db import init_db, db

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Serve production frontend from frontend/dist when available
    static_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist'))
    app = Flask(__name__, static_folder=static_dir, static_url_path='')
    app.config.from_object(config.get(config_name))
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    # Re-attempt to create tables in-app context if earlier create_all failed
    try:
        with app.app_context():
            try:
                db.create_all()
            except Exception as _e:
                print(f"[DB] Warning: second create_all() attempt failed: {_e}")
    except Exception as _e:
        print(f"[DB] Warning: could not re-attempt create_all(): {_e}")
    
    # Initialize sample data on first run (best-effort; don't crash if DB inaccessible)
    with app.app_context():
        try:
            from models.user import User
            from models.worker import Worker

            try:
                needs_seed = User.query.count() == 0
            except Exception as e:
                # DB not accessible during startup (permission/lock); skip seeding
                print(f"[DB] Warning: cannot access DB to check seed state: {e}")
                needs_seed = False

            if needs_seed:
                try:
                    # Create sample worker user
                    worker_user = User(
                        username='worker1',
                        email='worker1@heatguard.com',
                        role='worker'
                    )
                    worker_user.set_password('password123')
                    db.session.add(worker_user)
                    db.session.flush()

                    # Create worker profile
                    worker = Worker(
                        user_id=worker_user.id,
                        worker_id=f"W_{worker_user.id}",
                        zone="Zone A - Construction",
                        bmi_bucket="medium",
                        fitness_level="medium"
                    )
                    db.session.add(worker)

                    # Create sample supervisor user
                    supervisor_user = User(
                        username='supervisor1',
                        email='supervisor1@heatguard.com',
                        role='supervisor'
                    )
                    supervisor_user.set_password('admin123')
                    db.session.add(supervisor_user)

                    # Create admin user
                    admin_user = User(
                        username='admin',
                        email='admin@heatguard.com',
                        role='supervisor'
                    )
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)

                    db.session.commit()
                    print("[DB] Sample data initialized successfully")
                except Exception as e:
                    db.session.rollback()
                    print(f"[DB] Sample data initialization failed: {e}")
        except Exception as e:
            print(f"[Startup] Skipping DB seed due to import error: {e}")
    
    # Register blueprints (import after app/config to avoid early DB access)
    from routes.auth import auth_bp
    from routes.predictions import pred_bp
    from routes.worker import worker_bp
    from routes.supervisor import supervisor_bp
    from routes.demo import demo_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pred_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(supervisor_bp)
    app.register_blueprint(demo_bp)

    # Simple demo web UIs that render JSON demo data as HTML tables
    @app.route('/demo/supervisor-ui')
    def demo_supervisor_ui():
        try:
            # interactive supervisor UI: client-side fetch from /api/demo/workers
            html = """
            <!doctype html>
            <html>
            <head>
            <meta charset='utf-8'>
            <title>Demo Supervisor</title>
            <style>body{font-family:Arial,Helvetica,sans-serif}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;text-align:left}tr:hover{background:#f5f5f5}a.button{display:inline-block;padding:6px 10px;background:#2b6cb0;color:#fff;border-radius:4px;text-decoration:none}</style>
            </head>
            <body>
            <h1>Supervisor - Demo Workers</h1>
            <p>Live demo data from <code>/api/demo/workers</code></p>
            <input id="filter" placeholder="Filter by worker id or zone" style="padding:6px;margin-bottom:8px;width:300px">
            <div><a class="button" href="/demo/supervisor-ui">Refresh</a></div>
            <table id="workers"><thead><tr><th>Worker ID</th><th>Zone</th><th>Risk</th><th>Temp</th><th>HR</th><th>Action</th></tr></thead><tbody></tbody></table>
            <script>
            async function load(){
                const res = await fetch('/api/demo/workers');
                const data = await res.json();
                const tb = document.querySelector('#workers tbody'); tb.innerHTML='';
                for(const w of data){
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${w.worker_id}</td><td>${w.zone}</td><td>${w.current_risk}</td><td>${w.current_temp}</td><td>${w.current_hr}</td><td><a href='/demo/worker-ui/${w.worker_id}'>Open</a></td>`;
                    tb.appendChild(tr);
                }
            }
            document.getElementById('filter').addEventListener('input', function(e){
                const q = e.target.value.toLowerCase();
                document.querySelectorAll('#workers tbody tr').forEach(tr=>{
                    tr.style.display = tr.innerText.toLowerCase().includes(q)?'':'none';
                });
            });
            load();
            </script>
            </body>
            </html>
            """
            return html
        except Exception as e:
            return f"<pre>Error: {e}</pre>", 500

    @app.route('/demo/worker-ui/<int:worker_id>')
    def demo_worker_ui(worker_id):
        try:
            # interactive worker UI: shows history and a predict form that calls /predict
            html = """
            <!doctype html>
            <html>
            <head>
            <meta charset='utf-8'>
            <title>Worker __WORKER_ID__ - Demo</title>
            <style>body{font-family:Arial,Helvetica,sans-serif}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px}</style>
            </head>
            <body>
            <h1>Worker __WORKER_ID__ - Demo Dashboard</h1>
            <p>History (from <code>/api/demo/worker/__WORKER_ID__/history</code>)</p>
            <div id="history">Loading...</div>

            <h2>Quick Predict</h2>
            <form id="predForm">
            <label>body_temp_pre: <input name="body_temp_pre" value="36.8"></label><br>
            <label>body_temp_post: <input name="body_temp_post" value="37.5"></label><br>
            <label>heart_rate_pre: <input name="heart_rate_pre" value="72"></label><br>
            <label>heart_rate_post: <input name="heart_rate_post" value="110"></label><br>
            <label>wbgt: <input name="wbgt" value="32"></label><br>
            <label>ambient_temp: <input name="ambient_temp" value="34"></label><br>
            <label>humidity: <input name="humidity" value="60"></label><br>
            <label>radiant_heat: <input name="radiant_heat" value="500"></label><br>
            <label>break_duration: <input name="break_duration" value="0"></label><br>
            <button type="submit">Predict</button>
            </form>
            <div id="predResult"></div>

            <script>
            async function loadHistory(){
                const res = await fetch('/api/demo/worker/__WORKER_ID__/history');
                const data = await res.json();
                const metrics = data.metrics || [];
                if(metrics.length===0){document.getElementById('history').innerHTML='<p>No history</p>';return}
                let html = '<table><thead><tr><th>dths</th><th>risk</th><th>temp</th><th>hr</th></tr></thead><tbody>';
                for(const m of metrics){html += `<tr><td>${m.dths||''}</td><td>${m.risk_label||m.risk_level||''}</td><td>${m.body_temp_post||''}</td><td>${m.heart_rate_post||''}</td></tr>`}
                html += '</tbody></table>';
                document.getElementById('history').innerHTML = html;
            }
            document.getElementById('predForm').addEventListener('submit', async function(e){
                e.preventDefault();
                const form = e.target; const fd = new FormData(form); const obj = {};
                fd.forEach((v,k)=>obj[k]=isNaN(v)?v:parseFloat(v));
                // add bmi_bucket and fitness_level defaults
                obj.bmi_bucket = 'medium'; obj.fitness_level = 'medium';
                const res = await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(obj)});
                const j = await res.json();
                document.getElementById('predResult').innerText = JSON.stringify(j,null,2);
            });
            loadHistory();
            </script>
            </body>
            </html>
            """
            html = html.replace('__WORKER_ID__', str(worker_id))
            return html
        except Exception as e:
            return f"<pre>Error: {e}</pre>", 500
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200
    
    # Lightweight predict endpoint for Streamlit / external calls (no auth)
    @app.route('/predict', methods=['POST'])
    def predict_noauth():
        try:
            data = request.json
            from ml_engine.twin_engine import digital_twin, get_risk_message, get_recommendation, get_risk_label

            # perform the digital twin calculation
            risk, dths = digital_twin(data)
            response = {
                'risk_level': risk,
                'risk_label': get_risk_label(risk),
                'dths_score': dths,
                'message': get_risk_message(risk),
                'recommendation': get_recommendation(risk)
            }

            # if caller supplied a worker identifier we can persist the
            # metric/alert exactly as the authenticated prediction endpoint
            # does; this makes the lightweight route useful for ingesting
            # live sensor data without requiring JWTs.
            worker_key = data.get('worker_id')
            if worker_key:
                from models.worker import Worker, WorkerMetrics
                from models.alert import Alert
                worker = Worker.query.filter_by(worker_id=worker_key).first()
                if worker:
                    metrics = WorkerMetrics(
                        worker_id=worker.id,
                        body_temp_post=data.get('body_temp_post'),
                        body_temp_pre=data.get('body_temp_pre'),
                        heart_rate_post=data.get('heart_rate_post'),
                        heart_rate_pre=data.get('heart_rate_pre'),
                        wbgt=data.get('wbgt'),
                        ambient_temp=data.get('ambient_temp'),
                        humidity=data.get('humidity'),
                        radiant_heat=data.get('radiant_heat'),
                        break_duration=int(data.get('break_duration', 0)),
                        risk_level=risk,
                        dths_score=dths
                    )
                    db.session.add(metrics)
                    if risk >= 2:
                        db.session.add(Alert(
                            worker_id=worker.id,
                            risk_level=risk,
                            message=get_risk_message(risk)
                        ))
                    db.session.commit()

            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # NFC Health Check endpoint
    @app.route('/nfc-check', methods=['POST'])
    def nfc_check():
        """
        NFC Health Check endpoint
        Accepts temperature and heart rate from NFC/camera sensors
        Returns risk assessment and DTHS score
        """
        try:
            data = request.json
            from ml_engine.twin_engine import digital_twin, get_risk_message, get_recommendation, get_risk_label

            # Extract temperature and heart rate from NFC/camera
            body_temp = data.get('temperature', 37.0)
            heart_rate = data.get('heart_rate', 72)
            worker_id = data.get('worker_id')

            # Build complete prediction input with NFC data
            prediction_input = {
                'body_temp_post': body_temp,
                'body_temp_pre': 36.8,  # baseline
                'heart_rate_post': heart_rate,
                'heart_rate_pre': 70,   # baseline
                'wbgt': data.get('wbgt', 28),
                'ambient_temp': data.get('ambient_temp', 32),
                'humidity': data.get('humidity', 60),
                'radiant_heat': data.get('radiant_heat', 500),
                'break_duration': data.get('break_duration', 0),
                'bmi_bucket': data.get('bmi_bucket', 'medium'),
                'fitness_level': data.get('fitness_level', 'medium')
            }

            # Perform digital twin calculation
            risk, dths = digital_twin(prediction_input)

            # Build response
            response = {
                'temperature': body_temp,
                'heart_rate': heart_rate,
                'risk_level': risk,
                'risk_label': get_risk_label(risk),
                'dths_score': dths,
                'message': get_risk_message(risk),
                'recommendation': get_recommendation(risk)
            }

            # Persist NFC reading as a metric if worker_id provided
            if worker_id:
                from models.worker import Worker, WorkerMetrics
                from models.alert import Alert
                
                worker = Worker.query.filter_by(worker_id=worker_id).first()
                if worker:
                    # Create NFC metric record
                    nfc_metric = WorkerMetrics(
                        worker_id=worker.id,
                        body_temp_post=body_temp,
                        body_temp_pre=36.8,
                        heart_rate_post=heart_rate,
                        heart_rate_pre=70,
                        wbgt=prediction_input['wbgt'],
                        ambient_temp=prediction_input['ambient_temp'],
                        humidity=prediction_input['humidity'],
                        radiant_heat=prediction_input['radiant_heat'],
                        break_duration=prediction_input['break_duration'],
                        risk_level=risk,
                        dths_score=dths
                    )
                    db.session.add(nfc_metric)

                    # Create alert if risk is elevated
                    if risk >= 2:
                        # only persist alerts for elevated risk (2 or 3)
                        nfc_alert = Alert(
                            worker_id=worker.id,
                            risk_level=risk,
                            # use the standard risk message so UI banner is generic
                            message=get_risk_message(risk)
                        )
                        db.session.add(nfc_alert)

                    db.session.commit()
                    response['persisted'] = True
                else:
                    response['warning'] = f"Worker {worker_id} not found in database"

            return jsonify(response), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Serve SPA static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if app.static_folder and path and os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        return app.send_static_file('index.html')

    # Simple test page that runs a sample prediction and shows output
    @app.route('/model-test')
    def model_test():
        try:
            from ml_engine.twin_engine import digital_twin, get_risk_message
            sample = {
                'body_temp_post': 37.2,
                'body_temp_pre': 36.8,
                'heart_rate_post': 85,
                'heart_rate_pre': 72,
                'wbgt': 29,
                'ambient_temp': 32,
                'humidity': 60,
                'radiant_heat': 500,
                'break_duration': 10,
                'bmi_bucket': 1,
                'fitness_level': 1
            }
            risk, dths = digital_twin(sample)
            msg = get_risk_message(risk)
            html = f"""
            <!doctype html>
            <html>
            <head><meta charset='utf-8'><title>Model Test</title></head>
            <body>
            <h1>Model Test Output</h1>
            <pre>sample input: {sample}</pre>
            <pre>risk: {risk}</pre>
            <pre>dths: {dths}</pre>
            <pre>message: {msg}</pre>
            <p>API predict endpoint: <a href='/predict'>/predict</a> (POST)</p>
            </body>
            </html>
            """
            return html
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
