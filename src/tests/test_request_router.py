"""This file contains unit tests for the request_router module.

It tests the core functionality of the request router, including:

- Handling API requests for generating text using OpenAI models
- Validating input data using Pydantic schemas
- Interacting with the OpenAI service
- Storing and retrieving request records in the database

The tests cover various scenarios, including:

- Successful request processing
- Invalid input handling
- OpenAI API error handling
- Authentication checks
- Database interactions

The tests utilize mocking to isolate dependencies and simulate external interactions.
"""

import pytest
import unittest.mock as mock
from typing import Dict, Optional

from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.main import app
from src.routers.request_router import router
from src.models.request import Request
from src.schemas.request_schema import RequestCreate, RequestOut
from src.services.openai_service import OpenAIService
from src.utils.auth import authenticate_user
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MockRequest:
    """A mock FastAPI request object."""

    def __init__(self, user_id=None, db=None):
        self.user_id = user_id
        self.app = mock.MagicMock()
        self.app.state = mock.MagicMock()
        self.app.state.db = db


class TestRequestRouter:
    """Test suite for the request_router module."""

    @pytest.fixture
    def client(self):
        """Fixture to create a TestClient for testing the API."""
        return TestClient(app)

    @pytest.fixture
    def mock_openai_service(self, monkeypatch):
        """Fixture to mock the OpenAIService."""
        mock_openai_service = mock.MagicMock(spec=OpenAIService)
        monkeypatch.setattr("src.routers.request_router.OpenAIService", mock.MagicMock(return_value=mock_openai_service))
        return mock_openai_service

    @pytest.fixture
    def mock_db(self):
        """Fixture to mock the database session."""
        mock_db = mock.MagicMock()
        mock_db.add = mock.MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.get = AsyncMock()
        return mock_db

    @pytest.mark.asyncio
    async def test_create_request_success(self, client, mock_openai_service, mock_db):
        """Test successful request creation and processing."""
        mock_openai_service.generate_text.return_value = "This is a test response."
        mock_db.get.return_value = None
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = 1  # Assuming mock_db.refresh returns an ID of 1

        request_data = RequestCreate(
            model="gpt-3.5-turbo",
            prompt="Write a short story about a cat.",
            parameters={"temperature": 0.7},
        )

        request = MockRequest(user_id=1, db=mock_db)

        response = await client.post(
            "/request", json=request_data.dict(), headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 201
        assert response.json() == RequestOut(
            status="success",
            result="This is a test response.",
            request_id=1,
        ).dict()

        mock_openai_service.generate_text.assert_called_once_with(
            model="gpt-3.5-turbo",
            prompt="Write a short story about a cat.",
            parameters={"temperature": 0.7},
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_request_invalid_input(self, client):
        """Test handling of invalid request input."""
        request_data = {"model": "invalid_model", "prompt": "Write a story."}

        response = await client.post("/request", json=request_data)

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_request_openai_error(self, client, mock_openai_service, mock_db):
        """Test handling of OpenAI API errors."""
        mock_openai_service.generate_text.side_effect = openai.error.APIError("Test API error")
        mock_db.get.return_value = None
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        request_data = RequestCreate(
            model="gpt-3.5-turbo",
            prompt="Write a story.",
            parameters={"temperature": 0.7},
        )

        request = MockRequest(user_id=1, db=mock_db)

        response = await client.post(
            "/request", json=request_data.dict(), headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_request_success(self, client, mock_db):
        """Test successful request retrieval."""
        mock_db.get.return_value = Request(
            id=1,
            model="gpt-3.5-turbo",
            prompt="Write a story.",
            parameters={"temperature": 0.7},
            response="This is a test response.",
            status="success",
            user_id=1,
        )

        request = MockRequest(user_id=1, db=mock_db)

        response = await client.get("/request/1", headers={"Authorization": "Bearer test_token"})

        assert response.status_code == 200
        assert response.json() == RequestOut(
            status="success",
            result="This is a test response.",
            request_id=1,
        ).dict()

        mock_db.get.assert_called_once_with(Request, 1)

    @pytest.mark.asyncio
    async def test_get_request_not_found(self, client, mock_db):
        """Test handling of a request not found."""
        mock_db.get.return_value = None

        request = MockRequest(user_id=1, db=mock_db)

        response = await client.get("/request/1", headers={"Authorization": "Bearer test_token"})

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_request_unauthorized(self, client, mock_openai_service, mock_db):
        """Test handling of unauthorized access."""
        mock_openai_service.generate_text.return_value = "This is a test response."
        mock_db.get.return_value = None
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        request_data = RequestCreate(
            model="gpt-3.5-turbo",
            prompt="Write a short story about a cat.",
            parameters={"temperature": 0.7},
        )

        request = MockRequest(user_id=None, db=mock_db)

        response = await client.post("/request", json=request_data.dict())

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_request_unauthorized(self, client, mock_db):
        """Test handling of unauthorized access for retrieving a request."""
        mock_db.get.return_value = Request(
            id=1,
            model="gpt-3.5-turbo",
            prompt="Write a story.",
            parameters={"temperature": 0.7},
            response="This is a test response.",
            status="success",
            user_id=1,
        )

        request = MockRequest(user_id=None, db=mock_db)

        response = await client.get("/request/1")

        assert response.status_code == 401