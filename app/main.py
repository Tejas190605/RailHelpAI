import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database.init_db import init_db
from app.database.connection import SessionLocal
from app.backend.middleware.request_id import RequestIDMiddleware
from app.backend.api import complaints, ai, operations, analytics, intelligence, multimodal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (req_id=%(request_id)s): %(message)s",
    defaults={"request_id": "system"}
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schema and defaults...")
    init_db()
    yield
    logger.info("Shutting down RailHelpAI backend...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Railway Complaint Intelligence & Operations Platform API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Centralized exception handler to return clean error JSON without stack traces."""
    req_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unhandled exception for request {req_id}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred. Please contact system support.",
            "request_id": req_id
        }
    )


@app.get("/health", tags=["Health"])
@app.get("/health/live", tags=["Health"])
@app.get("/api/v1/health", tags=["Health"])
def health_live():
    """Liveness check endpoint."""
    return {"status": "healthy", "app_name": settings.APP_NAME, "version": "1.0.0"}


@app.get("/health/ready", tags=["Health"])
@app.get("/api/v1/health/ready", tags=["Health"])
def health_ready():
    """Readiness check verifying database & ML model readiness."""
    db_ok = False
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_ok = True
        db.close()
    except Exception:
        db_ok = False

    models_ok = os.path.exists("models/complaint_classifier_v1.0.joblib")

    if db_ok and models_ok:
        return {
            "status": "ready",
            "components": {"database": "connected", "ml_models": "loaded"}
        }
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "components": {"database": "ok" if db_ok else "failed", "ml_models": "ok" if models_ok else "missing"}
            }
        )


# Include API routers
app.include_router(complaints.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai.router, prefix=settings.API_V1_PREFIX)
app.include_router(operations.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(intelligence.router, prefix=settings.API_V1_PREFIX)
app.include_router(multimodal.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
