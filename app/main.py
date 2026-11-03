from fastapi import FastAPI

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
def root():
    return {"message": "USSD Registration API is running"}