from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def init_db(app):
    db.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # On some Windows environments opening/creating the sqlite file
            # may fail during startup (permissions/locking). Log a warning and
            # allow the app to continue; tables can be created later when
            # the application first writes to the DB.
            print(f"[DB] Warning: create_all() failed: {e}")
