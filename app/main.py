from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app import models
from app.database import Base, engine
from app.routers import users

app = FastAPI(
    title="USSD Registration API",
    description="API for managing USSD user registrations",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "healthy"}

    except Exception:  # noqa: BLE001
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )
    
def root():
    return {"message": "USSD Registration API is running"}