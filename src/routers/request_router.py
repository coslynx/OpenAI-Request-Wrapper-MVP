from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Optional

from .models import Request
from .schemas import RequestCreate, RequestOut, ErrorResponse
from .services.openai_service import OpenAIService
from .utils.auth import authenticate_user, get_current_user
from .utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/request", response_model=RequestOut, responses={401: {"model": ErrorResponse}, 400: {"model": ErrorResponse}})
async def create_request(request: Request, request_data: RequestCreate):
    """
    Handles API requests for generating text using OpenAI models.

    Args:
        request: The FastAPI request object.
        request_data: Pydantic model containing request data (model, prompt, parameters, api_key).

    Returns:
        JSON response containing the generated text, status, and request ID.

    Raises:
        HTTPException: If authentication fails, invalid input is provided, or an OpenAI API error occurs.
    """
    current_user = await authenticate_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        request_record = Request(
            model=request_data.model,
            prompt=request_data.prompt,
            parameters=request_data.parameters,
            user_id=current_user.id
        )
        db = request.app.state.db
        db.add(request_record)
        await db.commit()
        await db.refresh(request_record)

        openai_service = OpenAIService()
        response = await openai_service.generate_text(
            model=request_record.model,
            prompt=request_record.prompt,
            parameters=request_record.parameters
        )

        request_record.response = response
        await db.commit()
        await db.refresh(request_record)

        return RequestOut(
            status="success",
            result=response,
            request_id=request_record.id
        )
    except Exception as e:
        logger.error(f"Error processing OpenAI request: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/request/{request_id}", response_model=RequestOut, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}})
async def get_request(request: Request, request_id: int):
    """
    Retrieves the status and response for a specific request.

    Args:
        request: The FastAPI request object.
        request_id: The ID of the request to retrieve.

    Returns:
        JSON response containing the generated text, status, and request ID.

    Raises:
        HTTPException: If authentication fails or the request is not found.
    """
    current_user = await authenticate_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    db = request.app.state.db
    request_record = await db.get(Request, request_id)
    if not request_record:
        raise HTTPException(status_code=404, detail="Request not found")
    return RequestOut(
        status=request_record.status,
        result=request_record.response,
        request_id=request_record.id
    )