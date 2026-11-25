#!/usr/bin/env python
"""
HeatGuard Database Initialization Script
Initializes the database with sample users and data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize database with sample data"""
    from backend.app import create_app
    from backend.database.db import db
    from backend.models.user import User
    from backend.models.worker import Worker
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Check if sample users already exist
        if User.query.filter_by(username='worker1').first():
            print("✓ Sample users already exist, skipping...")
            return
        
        # Create sample worker user
        worker_user = User(
            username='worker1',
            email='worker1@heatguard.com',
            role='worker'
        )
        worker_user.set_password('password123')
        db.session.add(worker_user)
        db.session.commit()
        print("✓ Created sample worker user: worker1 / password123")
        
        # Create worker profile
        worker = Worker(
            user_id=worker_user.id,
            worker_id=f"W_{worker_user.id}",
            zone="Zone A - Construction",
            bmi_bucket="medium",
            fitness_level="medium"
        )
        db.session.add(worker)
        db.session.commit()
        print("✓ Created worker profile")
        
        # Create sample supervisor user
        supervisor_user = User(
            username='supervisor1',
            email='supervisor1@heatguard.com',
            role='supervisor'
        )
        supervisor_user.set_password('admin123')
        db.session.add(supervisor_user)
        db.session.commit()
        print("✓ Created sample supervisor user: supervisor1 / admin123")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@heatguard.com',
            role='supervisor'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("✓ Created admin user: admin / admin123")
        
        print("\n✓ Database initialization complete!")
        print("\nSample accounts created:")
        print("  Worker:      worker1 / password123")
        print("  Supervisor:  supervisor1 / admin123")
        print("  Admin:       admin / admin123")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        import traceback
       traceback.print_exc()
        sys.exit(1)
