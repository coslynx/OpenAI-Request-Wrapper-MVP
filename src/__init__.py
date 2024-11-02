from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from typing import Dict

from .routers import request_router, auth_router, user_router
from .database import engine, Base
from .models import User, Request
from .utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(request_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Define custom error handling (optional)
@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    logger.error(f"Uncaught exception: {exc}")
    return JSONResponse(
        status_code=500, content={"message": str(exc)}
    )