"""This module defines the OpenAIService class, which is responsible for interacting with the OpenAI API."""

import openai
import os
from typing import Dict, Optional

from .utils.logger import get_logger

logger = get_logger(__name__)

class OpenAIService:
    """A class that handles interactions with the OpenAI API."""

    def __init__(self):
        """Initializes the OpenAIService with the API key from the environment variable."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = self.api_key

    async def generate_text(self, model: str, prompt: str, parameters: Optional[Dict] = None) -> str:
        """Generates text using the specified OpenAI model.

        Args:
            model: The name of the OpenAI model to use (e.g., "gpt-3.5-turbo").
            prompt: The input text for the model to process.
            parameters: A dictionary of additional parameters for the API call (e.g., temperature, max_tokens).

        Returns:
            The generated text from the OpenAI API.

        Raises:
            openai.error.APIError: If there's an error interacting with the OpenAI API.
        """
        try:
            response = await openai.Completion.acreate(
                model=model,
                prompt=prompt,
                **parameters or {}
            )
            return response.choices[0].text.strip()
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise