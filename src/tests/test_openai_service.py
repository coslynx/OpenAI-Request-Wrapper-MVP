"""This file defines unit tests for the OpenAIService class."""

import pytest
import unittest.mock as mock
from typing import Dict, Optional

from src.services.openai_service import OpenAIService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TestOpenAIService:
    """Test suite for the OpenAIService class."""

    @pytest.fixture
    def openai_service(self) -> OpenAIService:
        """Fixture to create an instance of OpenAIService for testing."""
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"}):
            service = OpenAIService()
            return service

    def test_init(self, openai_service: OpenAIService):
        """Test initialization of OpenAIService."""
        assert openai_service.api_key == "test_api_key"
        assert openai.api_key == "test_api_key"

    @pytest.mark.asyncio
    async def test_generate_text_success(self, openai_service: OpenAIService, monkeypatch):
        """Test successful text generation using OpenAI API."""
        mock_response = {
            "choices": [
                {"text": "This is a test response."}
            ]
        }
        monkeypatch.setattr(openai.Completion, "acreate", mock.AsyncMock(return_value=mock_response))

        prompt = "Write a short story about a cat."
        model = "gpt-3.5-turbo"
        parameters: Optional[Dict] = {"temperature": 0.7}

        response = await openai_service.generate_text(model=model, prompt=prompt, parameters=parameters)
        assert response == "This is a test response."

    @pytest.mark.asyncio
    async def test_generate_text_api_error(self, openai_service: OpenAIService, monkeypatch):
        """Test handling of OpenAI API error."""
        monkeypatch.setattr(openai.Completion, "acreate", mock.AsyncMock(side_effect=openai.error.APIError("Test API error")))

        prompt = "Write a short story about a cat."
        model = "gpt-3.5-turbo"
        parameters: Optional[Dict] = {"temperature": 0.7}

        with pytest.raises(openai.error.APIError):
            await openai_service.generate_text(model=model, prompt=prompt, parameters=parameters)