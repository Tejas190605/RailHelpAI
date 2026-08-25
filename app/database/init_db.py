import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
from app.database.connection import engine, Base, SessionLocal
from app.database.models import Department, Complaint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_DEPARTMENTS = [
    {"department_name": "Electrical / Coach Maintenance", "category": "Air Conditioning", "default_sla_hours": 2},
    {"department_name": "Housekeeping / Sanitation", "category": "Cleanliness", "default_sla_hours": 4},
    {"department_name": "Water Operations", "category": "Water Supply", "default_sla_hours": 2},
    {"department_name": "Electrical Maintenance", "category": "Electrical", "default_sla_hours": 4},
    {"department_name": "Catering Services", "category": "Catering", "default_sla_hours": 4},
    {"department_name": "Railway Protection Force (RPF)", "category": "Security", "default_sla_hours": 1},
    {"department_name": "Passenger Grievance Cell", "category": "Staff Behaviour", "default_sla_hours": 8},
    {"department_name": "Mechanical Engineering", "category": "Coach Maintenance", "default_sla_hours": 6},
    {"department_name": "Station Administration", "category": "Station Facilities", "default_sla_hours": 8},
    {"department_name": "Ticketing & Commercial", "category": "Ticketing", "default_sla_hours": 12},
    {"department_name": "Medical Emergency Response", "category": "Medical", "default_sla_hours": 1},
    {"department_name": "Luggage & Parcel Office", "category": "Luggage", "default_sla_hours": 8},
    {"department_name": "Pest Control Division", "category": "Pest Control", "default_sla_hours": 12},
    {"department_name": "General Operations", "category": "Other", "default_sla_hours": 24},
]


def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed default departments if table is empty
        existing_depts = db.query(Department).count()
        if existing_depts == 0:
            logger.info("Seeding default departments...")
            for dept_data in DEFAULT_DEPARTMENTS:
                dept = Department(**dept_data)
                db.add(dept)
            db.commit()
            logger.info(f"Seeded {len(DEFAULT_DEPARTMENTS)} default departments.")
        else:
            logger.info(f"Database already contains {existing_depts} departments.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
