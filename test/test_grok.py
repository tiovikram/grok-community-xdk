import http.client
import unittest
from unittest import mock

import requests

from grok import Grok
from grok import errors
from grok import providers
from grok import schemas

import test_utils


class TestGrok(unittest.TestCase):

    def setUp(self):
        self.mock_requests = mock.Mock(spec_set=requests)
        self.mock_unauthorized_user_error_provider = mock.Mock(
            spec_set=providers.UnauthorizedUserErrorProvider
        )

        self.grok = Grok(
            "xai-sample-api-key",
            self.mock_requests,
            self.mock_unauthorized_user_error_provider,
        )

    def test_v1_api_key_with_valid_api_key(self):
        # Arrange
        mock_response_data = {
            "redacted_api_key": "xG1k...b14o",
            "user_id": "59fbe5f2-040b-46d5-8325-868bb8f23eb2",
            "name": "My API Key",
            "create_time": "2024-01-01T12:55:18.139305Z",
            "modify_time": "2024-08-28T17:20:12.343321Z",
            "modified_by": "3d38b4dc-4eb7-4785-ae26-c3fa8997ffc7",
            "team_id": "5ea6f6bd-7815-4b8a-9135-28b2d7ba6722",
            "acls": ["api-key:model:*", "api-key:endpoint:*"],
            "api_key_id": "ae1e1841-4326-4b36-a8a9-8a1a7237db11",
            "team_blocked": False,
            "api_key_blocked": False,
            "api_key_disabled": False,
        }
        expected_response = schemas.APIKey(**mock_response_data)
        v1_api_key_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=v1_api_key_response
        )

        # Act
        actual_response = self.grok.api_key()

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_api_key_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.api_key()

    def test_v1_embedding_model_with_valid_model(self):
        # Arrange
        mock_response_data = {
            "id": "v1",
            "created": 1725148800,
            "object": "model",
            "owned_by": "xai",
            "version": "0.1.0",
            "input_modalities": ["text"],
            "prompt_text_token_price": 100,
            "prompt_image_token_price": 0,
        }
        expected_response = schemas.EmbeddingModel(**mock_response_data)
        v1_embedding_model_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=v1_embedding_model_response
        )

        # Act
        actual_response = self.grok.embedding_model("v1")

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_embedding_model_with_invalid_api_key(self):
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.embedding_model("grok-2-1212")

    def test_v1_embedding_model_with_invalid_model(self):
        # Arrange
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=test_utils.MockResponse({}, http.client.NOT_FOUND)
        )

        # Act / Assert
        with self.assertRaises(errors.ModelNotFoundError) as context_manager:
            self.grok.embedding_model("grok-invalid-model")

    def test_v1_embedding_models_with_valid_api_key(self):
        # Arrange
        mock_response_data = {
            "models": [
                {
                    "id": "v1",
                    "created": 1725148800,
                    "object": "model",
                    "owned_by": "xai",
                    "version": "0.1.0",
                    "input_modalities": ["text"],
                    "prompt_text_token_price": 100,
                    "prompt_image_token_price": 0,
                }
            ]
        }
        expected_response = schemas.EmbeddingModels(**mock_response_data)
        v1_embedding_models_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=v1_embedding_models_response
        )

        # Act
        actual_response = self.grok.embedding_models()

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_embedding_models_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.embedding_models()

    def test_v1_language_model_with_valid_language_model(self):
        # Arrange
        mock_response_data = {
            "id": "grok-beta",
            "created": 1726444800,
            "object": "model",
            "owned_by": "xai",
            "version": "1.0.0",
            "input_modalities": ["text"],
            "output_modalities": ["text"],
            "prompt_text_token_price": 500000,
            "prompt_image_token_price": 0,
            "completion_text_token_price": 1500000,
        }
        expected_response = schemas.LanguageModel(**mock_response_data)
        v1_language_model_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=v1_language_model_response
        )

        # Act
        actual_response = self.grok.language_model("grok-beta")

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_language_model_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.language_model("grok-beta")

    def test_v1_language_model_with_invalid_model(self):
        # Arrange
        self.mock_requests.get = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.NOT_FOUND
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.ModelNotFoundError):
            self.grok.language_model("grok-invalid-language-model")

    def test_v1_language_models_with_valid_api_key(self):
        # Arrange
        mock_response_data = {
            "models": [
                {
                    "id": "grok-beta",
                    "created": 1726444800,
                    "object": "model",
                    "owned_by": "xai",
                    "version": "1.0.0",
                    "input_modalities": ["text"],
                    "output_modalities": ["text"],
                    "prompt_text_token_price": 250000,
                    "prompt_image_token_price": 0,
                    "completion_text_token_price": 1000000,
                }
            ]
        }
        expected_response = schemas.LanguageModels(**mock_response_data)
        v1_language_models_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(
            spec_set=[], return_value=v1_language_models_response
        )

        # Act
        actual_response = self.grok.language_models()

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_language_models_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.language_models()

    def test_v1_model_with_valid_api_key(self):
        # Arrange
        mock_response_data = {
            "id": "grok-beta",
            "created": 1726444800,
            "object": "model",
            "owned_by": "xai",
        }
        expected_response = schemas.Model(**mock_response_data)
        v1_model_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(spec_set=[], return_value=v1_model_response)

        # Act
        actual_response = self.grok.model("grok-beta")

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_model_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.model("grok-beta")

    def test_v1_model_with_invalid_model(self):
        # Arrange
        self.mock_requests.get = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.NOT_FOUND
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.ModelNotFoundError):
            self.grok.model("grok-invalid-model")

    def test_v1_models_with_valid_api_key(self):
        # Arrange
        mock_response_data = {
            "data": [
                {
                    "id": "grok-beta",
                    "created": 1725148800,
                    "object": "model",
                    "owned_by": "xai",
                }
            ]
        }
        expected_response = schemas.Models(**mock_response_data)
        v1_models_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.get = mock.Mock(spec_set=[], return_value=v1_models_response)

        # Act
        actual_response = self.grok.models()

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_models_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.models()

    def test_v1_tokenize_text_with_valid_request(self):
        # Arrange
        mock_response_data = {"token_ids": ["string"]}
        expected_response = schemas.TokenizeTextResponse(**mock_response_data)
        v1_tokenize_text_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_tokenize_text_response
        )

        # Act
        actual_response = self.grok.tokenize_text(
            schemas.TokenizeTextRequest(text="hello world", model="grok-beta")
        )

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_tokenize_text_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.tokenize_text(
                schemas.TokenizeTextRequest(text="hello world", model="grok-beta")
            )

    def test_v1_tokenize_text_with_invalid_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.BAD_REQUEST
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.tokenize_text(
                schemas.TokenizeTextRequest(text="hello world", model="grok-beta")
            )

    def test_v1_tokenize_text_with_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.UNPROCESSABLE_ENTITY
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.tokenize_text(
                schemas.TokenizeTextRequest(text="hello world", model="grok-beta")
            )

    def test_v1_chat_completion_with_valid_api_key(self):
        # Arrange
        chat_request = schemas.ChatRequest(
            **{
                "messages": [
                    {"role": "system", "content": "You are a test assistant."},
                    {
                        "role": "user",
                        "content": "Testing. Just say hi and nothing else.",
                    },
                ],
                "model": "grok-2-mini",
            }
        )
        mock_response_data = {
            "id": "c6f2d009-77ca-40d9-9de5-6d19716e1b4d",
            "object": "chat.completion",
            "created": 1728646283,
            "model": "grok-2-mini",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hi"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 25,
                "completion_tokens": 2,
                "total_tokens": 27,
                "prompt_tokens_details": {
                    "text_tokens": 17,
                    "audio_tokens": 0,
                    "image_tokens": 8,
                    "cached_tokens": 0,
                },
            },
            "system_fingerprint": "fp_9877325691",
        }
        expected_response = schemas.ChatResponse(**mock_response_data)
        v1_chat_completion_response = test_utils.MockResponse(mock_response_data)
        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_chat_completion_response
        )

        # Act
        actual_response = self.grok.chat_completions(chat_request)

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_chat_completion_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.chat_completions(
                schemas.ChatRequest(model="grok-beta", messages=[])
            )

    def test_v1_chat_completion_with_valid_api_key_and_bad_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.BAD_REQUEST
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.chat_completions(
                schemas.ChatRequest(model="grok-beta", messages=[])
            )

    def test_v1_chat_completion_with_valid_api_key_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse(
                {}, http_status_code=http.client.UNPROCESSABLE_ENTITY
            ),
        )

        # Act / Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.chat_completions(
                schemas.ChatRequest(model="grok-beta", messages=[])
            )

    def test_v1_complete_with_valid_request(self):
        # Arrange
        complete_request = schemas.CompleteRequest(
            **{
                "model": "grok-2-latest",
                "max_tokens_to_sample": 8,
                "temperature": 0.1,
                "prompt": "\n\nHuman: Hello, how are you?\n\nAssistant:",
            }
        )

        mock_response_data = {
            "type": "completion",
            "id": "8d3e45c6-f882-4d40-bb4a-54c6af166e18",
            "completion": "Hello there! I'm Grok",
            "stop_reason": "max_tokens",
            "model": "grok-2-latest",
        }

        expected_response = schemas.CompleteResponse(**mock_response_data)
        v1_complete_response = test_utils.MockResponse(mock_response_data)

        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_complete_response
        )

        # Act
        actual_response = self.grok.complete(complete_request)

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_complete_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.complete(
                schemas.CompleteRequest(
                    max_tokens_to_sample=0, model="grok-beta", prompt=""
                )
            )

    def test_v1_complete_with_valid_api_key_invalid_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.BAD_REQUEST),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.complete(
                schemas.CompleteRequest(
                    max_tokens_to_sample=0, model="grok-beta", prompt=""
                )
            )

    def test_v1_complete_with_valid_api_key_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.UNPROCESSABLE_ENTITY),
        )

        # Act / Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.complete(
                schemas.CompleteRequest(
                    max_tokens_to_sample=0, model="grok-beta", prompt=""
                )
            )

    def test_v1_completions_with_valid_request(self):
        # Arrange
        completions_request = schemas.SampleRequest(
            **{"prompt": "1, 2, 3, 4, ", "model": "grok-2-latest", "max_tokens": 3}
        )

        mock_response_data = {
            "id": "3a34a6a3-82b2-46d9-874d-99dbca084813",
            "object": "text_completion",
            "created": 1728652460,
            "model": "grok-2-latest",
            "choices": [{"index": 0, "text": "5, ", "finish_reason": "length"}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 3, "total_tokens": 15},
            "system_fingerprint": "fp_8933231290",
        }

        expected_response = schemas.SampleResponse(**mock_response_data)
        v1_completions_response = test_utils.MockResponse(
            mock_response_data, http.client.OK
        )

        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_completions_response
        )

        # Act
        actual_response = self.grok.completions(completions_request)

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_completions_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.completions(
                schemas.SampleRequest(model="grok-beta", prompt="test prompt")
            )

    def test_v1_completions_with_valid_api_key_invalid_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.BAD_REQUEST),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.completions(
                schemas.SampleRequest(model="grok-beta", prompt="test prompt")
            )

    def test_v1_completions_with_valid_api_key_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.UNPROCESSABLE_ENTITY),
        )

        # Act/ Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.completions(
                schemas.SampleRequest(model="grok-beta", prompt="test prompt")
            )

    def test_v1_embeddings_with_valid_request(self):
        # Arrange
        embedding_request = schemas.EmbeddingRequest(
            **{
                "input": ["This is an example content to embed..."],
                "model": "v1",
                "encoding_format": "float",
            }
        )

        mock_response_data = {
            "object": "list",
            "model": "v1",
            "data": [
                {
                    "index": 0,
                    "embedding": [0.01567895, 0.063257694, 0.045925662],
                    "object": "embedding",
                }
            ],
            "usage": {"prompt_tokens": 1, "total_tokens": 1},
        }

        expected_response = schemas.EmbeddingResponse(**mock_response_data)
        v1_embeddings_response = test_utils.MockResponse(mock_response_data)

        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_embeddings_response
        )

        # Act
        actual_response = self.grok.embeddings(embedding_request)

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_embeddings_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.embeddings(
                schemas.EmbeddingRequest(
                    model="grok-beta", input=["Example Embedding text"]
                )
            )

    def test_v1_embeddings_with_valid_api_key_invalid_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.BAD_REQUEST),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.embeddings(
                schemas.EmbeddingRequest(
                    model="grok-beta", input=["Example Embedding text"]
                )
            )

    def test_v1_embeddings_with_valid_api_key_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.UNPROCESSABLE_ENTITY),
        )

        # Act / Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.embeddings(
                schemas.EmbeddingRequest(
                    model="grok-beta", input=["Example Embedding text"]
                )
            )

    def test_v1_messages_with_valid_request(self):
        # Arrange
        message_request = schemas.MessageRequest(
            **{
                "model": "grok-2-latest",
                "max_tokens": 32,
                "messages": [{"role": "user", "content": "Hello, world"}],
            }
        )

        mock_response_data = {
            "id": "107baefc-993f-4632-b504-3f0c90d089aa",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "Hello! How can I assist you today?"}],
            "model": "grok-2-latest",
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 9,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "output_tokens": 10,
            },
        }

        expected_response = schemas.MessageResponse(**mock_response_data)
        v1_messages_response = test_utils.MockResponse(mock_response_data)

        self.mock_requests.post = mock.Mock(
            spec_set=[], return_value=v1_messages_response
        )

        # Act
        actual_response = self.grok.messages(message_request)

        # Assert
        self.assertEqual(expected_response, actual_response)

    def test_v1_messages_with_invalid_api_key(self):
        # Arrange
        self.mock_unauthorized_user_error_provider.provide_error = mock.Mock(
            spec_set=[], side_effect=errors.InvalidAPIKeyProvidedError("")
        )

        # Act / Assert
        with self.assertRaises(errors.UnauthorizedUserError):
            self.grok.messages(
                schemas.MessageRequest(max_tokens=0, messages=[], model="grok-beta")
            )

    def test_v1_messages_with_valid_api_key_invalid_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.BAD_REQUEST),
        )

        # Act / Assert
        with self.assertRaises(errors.InvalidRequestError):
            self.grok.messages(
                schemas.MessageRequest(max_tokens=0, messages=[], model="grok-beta")
            )

    def test_v1_messages_with_valid_api_key_incomplete_request(self):
        # Arrange
        self.mock_requests.post = mock.Mock(
            spec_set=[],
            return_value=test_utils.MockResponse({}, http.client.UNPROCESSABLE_ENTITY),
        )

        # Act / Assert
        with self.assertRaises(errors.IncompleteRequestError):
            self.grok.messages(
                schemas.MessageRequest(max_tokens=0, messages=[], model="grok-beta")
            )
