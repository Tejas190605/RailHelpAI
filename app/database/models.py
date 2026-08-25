from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String(32), unique=True, index=True, nullable=False)
    complaint_text = Column(Text, nullable=False)
    complaint_type = Column(String(64), nullable=True, default="Other")
    subcategory = Column(String(64), nullable=True)
    train_number = Column(String(32), nullable=True, index=True)
    train_name = Column(String(128), nullable=True)
    station = Column(String(128), nullable=True, index=True)
    coach = Column(String(32), nullable=True)
    seat = Column(String(32), nullable=True)
    incident_datetime = Column(DateTime, nullable=True)
    priority = Column(String(16), nullable=True, default="P3", index=True)
    priority_score = Column(Float, nullable=True, default=50.0)
    sentiment = Column(String(32), nullable=True, default="Neutral")
    language = Column(String(16), nullable=True, default="en")
    department = Column(String(128), nullable=True, default="Unassigned")
    status = Column(String(32), nullable=False, default="New", index=True)
    response_deadline = Column(DateTime, nullable=True)
    sla_deadline = Column(DateTime, nullable=True)
    assigned_to = Column(String(128), nullable=True, default="System Auto-Router")
    assigned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    rating = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)

    # Relationships
    predictions = relationship("AIPrediction", back_populates="complaint", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="complaint", cascade="all, delete-orphan")
    resolutions = relationship("Resolution", back_populates="complaint", cascade="all, delete-orphan")
    clusters = relationship("ComplaintCluster", back_populates="complaint", cascade="all, delete-orphan")
    reviews = relationship("AIReview", back_populates="complaint", cascade="all, delete-orphan")


class AIReview(Base):
    __tablename__ = "ai_reviews"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    reviewer = Column(String(128), nullable=False, default="Operator Admin")
    original_category = Column(String(64), nullable=True)
    final_category = Column(String(64), nullable=True)
    original_priority = Column(String(16), nullable=True)
    final_priority = Column(String(16), nullable=True)
    original_department = Column(String(128), nullable=True)
    final_department = Column(String(128), nullable=True)
    action = Column(String(32), nullable=False, default="Approve")  # Approve, Override
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    complaint = relationship("Complaint", back_populates="reviews")


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    model_name = Column(String(64), nullable=False, default="baseline_model")
    model_version = Column(String(32), nullable=False, default="1.0.0")
    category = Column(String(64), nullable=True)
    category_confidence = Column(Float, nullable=True, default=0.0)
    priority = Column(String(16), nullable=True)
    priority_confidence = Column(Float, nullable=True, default=0.0)
    sentiment = Column(String(32), nullable=True)
    sentiment_confidence = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    complaint = relationship("Complaint", back_populates="predictions")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(128), unique=True, nullable=False, index=True)
    category = Column(String(64), nullable=False)
    default_sla_hours = Column(Integer, nullable=False, default=8)
    active = Column(Boolean, default=True, nullable=False)


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    department = Column(String(128), nullable=False)
    assigned_to = Column(String(128), nullable=True, default="System Auto-Router")
    assigned_at = Column(DateTime, default=utc_now, nullable=False)
    status = Column(String(32), nullable=False, default="Assigned")

    complaint = relationship("Complaint", back_populates="assignments")


class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    resolution_text = Column(Text, nullable=False)
    resolution_type = Column(String(64), nullable=False, default="Standard Action")
    resolved_at = Column(DateTime, default=utc_now, nullable=False)
    resolution_time_minutes = Column(Float, nullable=True)

    complaint = relationship("Complaint", back_populates="resolutions")


class ComplaintCluster(Base):
    __tablename__ = "complaint_clusters"

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(String(64), nullable=False, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    similarity_score = Column(Float, nullable=False, default=0.0)
    cluster_label = Column(String(128), nullable=True)

    complaint = relationship("Complaint", back_populates="clusters")


class ComplaintSimilarity(Base):
    __tablename__ = "complaint_similarities"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    matched_complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    similarity_score = Column(Float, nullable=False, default=0.0)
    model_name = Column(String(64), nullable=False, default="tfidf_cosine")
    model_version = Column(String(32), nullable=False, default="1.0.0")
    created_at = Column(DateTime, default=utc_now, nullable=False)


class ComplaintImage(Base):
    __tablename__ = "complaint_images"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    file_path = Column(String(256), nullable=False)
    file_name = Column(String(128), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(64), nullable=False)
    detected_category = Column(String(64), nullable=True)
    vision_confidence = Column(Float, nullable=True, default=0.0)
    ocr_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)


class MultimodalPrediction(Base):
    __tablename__ = "multimodal_predictions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False, index=True)
    text_category = Column(String(64), nullable=True)
    image_category = Column(String(64), nullable=True)
    fused_category = Column(String(64), nullable=False)
    fusion_confidence = Column(Float, nullable=False, default=0.0)
    conflict_detected = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    severity = Column(String(16), nullable=False, default="MEDIUM")
    supporting_metrics = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False, default=0.85)
    created_at = Column(DateTime, default=utc_now, nullable=False)


# Index definitions for optimized querying
Index("idx_complaint_status_priority", Complaint.status, Complaint.priority)
Index("idx_complaint_train_station", Complaint.train_number, Complaint.station)
Index("idx_similarity_lookup", ComplaintSimilarity.complaint_id, ComplaintSimilarity.similarity_score)
