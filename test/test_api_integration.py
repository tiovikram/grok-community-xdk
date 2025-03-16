import http.client
import os
import unittest
from unittest import mock

import requests

from xai_grok.grok import Grok
from xai_grok import errors
from xai_grok import providers
from xai_grok import schemas


class TestAPIIntegration(unittest.TestCase):

    def setUp(self):
        if xai_api_key := os.environ["XAI_API_KEY"]:
            self.grok = Grok(
                xai_api_key, requests, providers.UnauthorizedUserErrorProvider()
            )
        else:
            raise Error(
                "Environment variable XAI_API_KEY not set. Failed to instantiate xAI Grok client. Please get an xAI API key from https://console.x.ai"
            )

    def test_v1_api_key(self):
        # Act
        api_key = self.grok.api_key()

        # Assert
        self.assertIsInstance(api_key, schemas.APIKey)

    def test_v1_api_key_no_api_key(self):
        # Arrange
        grok = Grok("", requests, providers.UnauthorizedUserErrorProvider())

        # Act / Assert
        with self.assertRaises(errors.NoAPIKeyProvidedError):
            grok.api_key()

    def test_v1_api_key_with_invalid_api_key(self):
        # Arrange
        grok = Grok(
            "xai-invalid-api-key", requests, providers.UnauthorizedUserErrorProvider()
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidAPIKeyProvidedError):
            grok.api_key()

    def test_v1_chat_completions(self):
        # Arrange
        chat_request = schemas.ChatRequest(
            **{
                "messages": [
                    {"role": "system", "content": "You're an assistant"},
                    {"role": "user", "content": "Hi"},
                ],
                "model": "grok-2-latest",
            }
        )

        # Act
        chat_response = self.grok.chat_completions(chat_request)

        # Assert
        self.assertIsInstance(chat_response, schemas.ChatResponse)

    def test_v1_complete(self):
        pass  # NOTE: This endpoint does not work for request specified in xAI API docs (https://api.x.ai/docs/)

    def test_v1_completions(self):
        # Arrange
        sample_request = schemas.SampleRequest(
            **{"prompt": "1, 2, 3, 4, ", "model": "grok-2-latest", "max_tokens": 3}
        )

        # Act
        sample_response = self.grok.completions(sample_request)

        # Assert
        self.assertIsInstance(sample_response, schemas.SampleResponse)

    def test_v1_embedding_model(self):
        pass  # NOTE: No embedding models available to currently test against

    def test_v1_embedding_models(self):
        # Act
        embedding_models = self.grok.embedding_models()

        # Assert
        self.assertIsInstance(embedding_models, schemas.EmbeddingModels)

    def test_v1_embeddings(self):
        pass  # NOTE: No embedding models available to currently test against

    def test_v1_language_model(self):
        pass  # NOTE: This endpoint does not work on xAI API

    def test_vl_language_models(self):
        # Act
        language_models = self.grok.language_models()

        # Assert
        self.assertIsInstance(language_models, schemas.LanguageModels)

    def test_v1_messages(self):
        # Arrange
        message_request = schemas.MessageRequest(
            **{
                "model": "grok-2-latest",
                "max_tokens": 32,
                "messages": [{"role": "user", "content": "Hello, world"}],
            }
        )

        # Act
        message_response = self.grok.messages(message_request)

        # Assert
        self.assertIsInstance(message_response, schemas.MessageResponse)

    def test_v1_model(self):
        # Act
        model = self.grok.model("grok-2")

        # Assert
        self.assertIsInstance(model, schemas.Model)

    def test_v1_models(self):
        # Act
        models = self.grok.models()

        # Assert
        self.assertIsInstance(models, schemas.Models)

    def test_v1_tokenize_text(self):
        pass  # NOTE: This endpoint does not work for request specified in xAI  API docs (https://api.x.ai/docs/)
