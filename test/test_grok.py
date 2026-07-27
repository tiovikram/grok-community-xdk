import http.client
import unittest

import xai_grok.errors as errors
import xai_grok.schemas as schemas
from xai_grok.grok import Grok

import test_utils


class FakeRequests:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.response


class TestGrok(unittest.TestCase):
    def client(self, response):
        transport = FakeRequests(response)
        return Grok("xai-test-key", transport), transport

    def test_api_key_parses_current_schema(self):
        body = {
            "acls": ["api-key:endpoint:*"],
            "api_key_blocked": False,
            "api_key_disabled": False,
            "api_key_id": "key-id",
            "create_time": "2026-01-01T00:00:00Z",
            "modified_by": "user-id",
            "modify_time": "2026-01-01T00:00:00Z",
            "name": "test",
            "redacted_api_key": "xai-...test",
            "team_blocked": False,
            "team_id": "team-id",
            "user_id": "user-id",
        }
        grok, transport = self.client(test_utils.MockResponse(body))
        result = grok.api_key()
        self.assertEqual("key-id", result.api_key_id)
        method, url, kwargs = transport.calls[0]
        self.assertEqual("GET", method)
        self.assertEqual("https://api.x.ai/v1/api-key", url)
        self.assertEqual("Bearer xai-test-key", kwargs["headers"]["Authorization"])

    def test_chat_completion_preserves_choices_and_sends_json_object(self):
        body = {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello",
                        "refusal": None,
                        "role": "assistant",
                        "tool_calls": None,
                    },
                }
            ],
            "created": 1752854522,
            "id": "response-id",
            "model": "grok-4",
            "object": "chat.completion",
            "service_tier": "default",
        }
        grok, transport = self.client(test_utils.MockResponse(body))
        request = schemas.ChatRequest(
            model="grok-4",
            messages=[{"role": "user", "content": "Say hello"}],
        )
        result = grok.chat_completion(request)
        self.assertEqual("Hello", result.choices[0].message.content)
        method, url, kwargs = transport.calls[0]
        self.assertEqual("POST", method)
        self.assertEqual("https://api.x.ai/v1/chat/completions", url)
        self.assertIsInstance(kwargs["json"], dict)
        self.assertEqual("grok-4", kwargs["json"]["model"])

    def test_query_parameters_omit_none(self):
        body = {"data": [], "has_more": False, "object": "list"}
        grok, transport = self.client(test_utils.MockResponse(body))
        grok.files(limit=10, order="desc")
        self.assertEqual(
            {"limit": 10, "order": "desc"}, transport.calls[0][2]["params"]
        )

    def test_binary_download_is_returned_unchanged(self):
        grok, _ = self.client(test_utils.MockResponse({}, content=b"file bytes"))
        self.assertEqual(b"file bytes", grok.file_content("file-id"))

    def test_http_error_is_translated(self):
        grok, _ = self.client(
            test_utils.MockResponse(
                {"error": {"message": "bad request"}},
                http_status_code=http.client.UNPROCESSABLE_ENTITY,
            )
        )
        with self.assertRaisesRegex(errors.InvalidRequestError, "bad request"):
            grok.models()

    def test_not_found_is_translated(self):
        grok, _ = self.client(
            test_utils.MockResponse({}, http_status_code=http.client.NOT_FOUND)
        )
        with self.assertRaises(errors.ModelNotFoundError):
            grok.model("missing")

    def test_client_covers_every_openapi_operation(self):
        expected_methods = {
            "api_key",
            "chat_completion",
            "deferred_chat_completion",
            "complete",
            "completion",
            "search_documents",
            "embedding_models",
            "embedding_model",
            "embeddings",
            "files",
            "upload_file",
            "file",
            "delete_file",
            "file_content",
            "create_file_public_url",
            "revoke_file_public_url",
            "image_generation_models",
            "image_generation_model",
            "edit_image",
            "generate_image",
            "language_models",
            "language_model",
            "me",
            "messages",
            "models",
            "model",
            "response",
            "compact_response",
            "stored_response",
            "delete_stored_response",
            "response_input_items",
            "skills",
            "upload_skill",
            "skill",
            "delete_skill",
            "skill_content",
            "tokenize_text",
            "video_generation_models",
            "video_generation_model",
            "edit_video",
            "extend_video",
            "generate_video",
            "deferred_video",
        }
        self.assertTrue(expected_methods.issubset(set(dir(Grok))))


if __name__ == "__main__":
    unittest.main()
