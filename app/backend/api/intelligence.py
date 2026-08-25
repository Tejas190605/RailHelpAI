from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.ai.duplicate_detector import detect_duplicates
from app.ai.clustering import rebuild_incident_clusters, get_active_clusters
from app.ai.resolution_predictor import resolution_predictor_service
from app.services.hotspot_service import get_hotspot_analytics
from app.services.train_service import get_trains_summary, get_train_profile
from app.services.station_service import get_stations_summary, get_station_profile
from app.backend.schemas.intelligence_schema import (
    DuplicateDetectRequest, DuplicateDetectResponse,
    ResolutionPredictRequest, ResolutionPredictResponse,
    ClusterItemResponse, HotspotItemResponse
)

router = APIRouter(tags=["Advanced Intelligence"])


@router.post("/ai/detect-duplicates", response_model=DuplicateDetectResponse)
def detect_duplicates_endpoint(
    payload: DuplicateDetectRequest,
    db: Session = Depends(get_db)
):
    """Detect potential duplicate/related complaints using TF-IDF vector similarity."""
    return detect_duplicates(payload.text, db, threshold=payload.threshold or 0.80)


@router.post("/ai/predict-resolution", response_model=ResolutionPredictResponse)
def predict_resolution_endpoint(payload: ResolutionPredictRequest):
    """Predict advisory resolution duration (minutes) using RandomForestRegressor."""
    return resolution_predictor_service.predict_resolution_time(
        category=payload.category,
        priority=payload.priority,
        department=payload.department,
        train_number=payload.train_number,
        station=payload.station
    )


@router.get("/analytics/clusters", response_model=List[ClusterItemResponse])
def list_clusters_endpoint(db: Session = Depends(get_db)):
    """Fetch active incident clusters."""
    return get_active_clusters(db)


@router.post("/analytics/clusters/rebuild")
def rebuild_clusters_endpoint(db: Session = Depends(get_db)):
    """Trigger DBSCAN clustering rebuild across open complaints."""
    return rebuild_incident_clusters(db)


@router.get("/analytics/hotspots", response_model=List[HotspotItemResponse])
def list_hotspots_endpoint(db: Session = Depends(get_db)):
    """Fetch multi-factor operational hotspot risk scores."""
    return get_hotspot_analytics(db)


@router.get("/analytics/trains")
def list_trains_endpoint(db: Session = Depends(get_db)):
    """List operational train summaries."""
    return get_trains_summary(db)


@router.get("/analytics/trains/{train_number}")
def get_train_profile_endpoint(train_number: str, db: Session = Depends(get_db)):
    """Fetch analytical profile for a specific train."""
    return get_train_profile(db, train_number)


@router.get("/analytics/stations")
def list_stations_endpoint(db: Session = Depends(get_db)):
    """List operational station summaries."""
    return get_stations_summary(db)


@router.get("/analytics/stations/{station_name}")
def get_station_profile_endpoint(station_name: str, db: Session = Depends(get_db)):
    """Fetch analytical profile for a specific station."""
    return get_station_profile(db, station_name)
