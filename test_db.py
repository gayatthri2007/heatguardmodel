#!/usr/bin/env python
"""Quick database test"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database.db import db
from backend.models.user import User
from backend.models.worker import Worker

app = create_app()
with app.app_context():
    print(f"Total users: {User.query.count()}")
    for u in User.query.all():
        print(f"  - {u.username} ({u.role})")
    print(f"\nTotal workers: {Worker.query.count()}")
    for w in Worker.query.all():
        print(f"  - {w.worker_id} (Zone: {w.zone})")
