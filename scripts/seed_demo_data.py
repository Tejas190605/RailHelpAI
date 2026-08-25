import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from datetime import datetime, timedelta, timezone

from app.database.connection import SessionLocal, engine, Base
from app.database.init_db import init_db
from app.database.models import Complaint
from app.ai.pipeline import analyze_complaint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEMO_SCENARIOS = [
    {
        "complaint_text": "Medical emergency on train 12951 coach A1 seat 14. Passenger suffering severe abdominal pain.",
        "train_number": "12951",
        "coach": "A1",
        "seat": "14",
        "station": "Mumbai Central"
    },
    {
        "complaint_text": "AC failure in coach B4 seat 21 since Pune. Temperature is rising and passengers are uncomfortable.",
        "train_number": "12951",
        "coach": "B4",
        "seat": "21",
        "station": "Pune Jn"
    },
    {
        "complaint_text": "AC is not cooling in coach B4 seat 22. Multiple passengers complaining about hot air.",
        "train_number": "12951",
        "coach": "B4",
        "seat": "22",
        "station": "Pune Jn"
    },
    {
        "complaint_text": "Toilet washbasin overflowing and dirty in coach S3 seat 45 at Solapur station.",
        "train_number": "11301",
        "coach": "S3",
        "seat": "45",
        "station": "Solapur"
    },
    {
        "complaint_text": "Catering food quality was stale and foul smelling in coach B2 seat 10.",
        "train_number": "12626",
        "coach": "B2",
        "seat": "10",
        "station": "New Delhi"
    }
]


def seed_demo_data():
    logger.info("Initializing fresh database tables for demo data seeder...")
    Base.metadata.drop_all(bind=engine)
    init_db()

    db = SessionLocal()
    try:
        for idx, item in enumerate(DEMO_SCENARIOS, 1):
            text = item["complaint_text"]
            metadata = {
                "train_number": item["train_number"],
                "coach": item["coach"],
                "seat": item["seat"],
                "station": item["station"]
            }

            analysis = analyze_complaint(text, metadata)

            comp = Complaint(
                complaint_id=f"RAI-DEMO{idx:02d}",
                complaint_text=text,
                train_number=item["train_number"],
                coach=item["coach"],
                seat=item["seat"],
                station=item["station"],
                status=analysis.routing_mode if hasattr(analysis, 'routing_mode') else "NEW",
                complaint_type=analysis.category.value,
                priority=analysis.priority.level,
                priority_score=analysis.priority.score,
                department=analysis.department.name,
                sentiment=analysis.sentiment.label,
                created_at=datetime.now(timezone.utc) - timedelta(minutes=idx * 15),
                sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=30 * idx)
            )
            db.add(comp)
        
        db.commit()
        logger.info(f"Successfully seeded {len(DEMO_SCENARIOS)} controlled synthetic demo complaints into railhelpai.db")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed demo data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
