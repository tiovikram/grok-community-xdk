from __future__ import annotations

import http
from pathlib import Path
from typing import Any, BinaryIO, TypeVar

import pydantic
import requests as requests_module

import xai_grok.errors as errors
import xai_grok.providers as providers
import xai_grok.schemas as schemas

ResponseModel = TypeVar("ResponseModel", bound=pydantic.BaseModel)


class Grok:
    """Typed client for xAI's REST API."""

    GROK_API_BASE_URL = "https://api.x.ai"

    def __init__(
        self,
        api_key: str,
        requests: Any = requests_module,
        unauthorized_user_error_provider: (
            providers.UnauthorizedUserErrorProvider | None
        ) = None,
        timeout: float = 60.0,
    ):
        self.grok_api_key = api_key
        self.requests = requests
        self.unauthorized_user_error_provider = (
            unauthorized_user_error_provider
            or providers.UnauthorizedUserErrorProvider()
        )
        self.timeout = timeout

    # Identity and model discovery

    def api_key(self) -> schemas.ApiKey:
        return self._get("v1/api-key", schemas.ApiKey)

    def me(self) -> schemas.GetMeResponse:
        return self._get("v1/me", schemas.GetMeResponse)

    def models(self) -> schemas.ListModelsResponse:
        return self._get("v1/models", schemas.ListModelsResponse)

    def model(self, model_id: str) -> schemas.Model:
        return self._get(f"v1/models/{model_id}", schemas.Model)

    def language_models(self) -> schemas.ListLanguageModelsResponse:
        return self._get("v1/language-models", schemas.ListLanguageModelsResponse)

    def language_model(self, model_id: str) -> schemas.LanguageModel:
        return self._get(f"v1/language-models/{model_id}", schemas.LanguageModel)

    def embedding_models(self) -> schemas.ListEmbeddingModelsResponse:
        return self._get("v1/embedding-models", schemas.ListEmbeddingModelsResponse)

    def embedding_model(self, model_id: str) -> schemas.EmbeddingModel:
        return self._get(f"v1/embedding-models/{model_id}", schemas.EmbeddingModel)

    def image_generation_models(self) -> schemas.ListImageGenerationModelsResponse:
        return self._get(
            "v1/image-generation-models", schemas.ListImageGenerationModelsResponse
        )

    def image_generation_model(self, model_id: str) -> schemas.ImageGenerationModel:
        return self._get(
            f"v1/image-generation-models/{model_id}", schemas.ImageGenerationModel
        )

    def video_generation_models(self) -> schemas.ListVideoGenerationModelsResponse:
        return self._get(
            "v1/video-generation-models", schemas.ListVideoGenerationModelsResponse
        )

    def video_generation_model(self, model_id: str) -> schemas.VideoGenerationModel:
        return self._get(
            f"v1/video-generation-models/{model_id}", schemas.VideoGenerationModel
        )

    # Text, chat, messages, and Responses API

    def chat_completion(self, request: schemas.ChatRequest) -> schemas.ChatResponse:
        return self._post("v1/chat/completions", request, schemas.ChatResponse)

    def deferred_chat_completion(self, request_id: str) -> schemas.ChatResponse:
        return self._get(
            f"v1/chat/deferred-completion/{request_id}", schemas.ChatResponse
        )

    def complete(self, request: schemas.CompleteRequest) -> schemas.CompleteResponse:
        return self._post("v1/complete", request, schemas.CompleteResponse)

    def completion(self, request: schemas.SampleRequest) -> schemas.SampleResponse:
        return self._post("v1/completions", request, schemas.SampleResponse)

    def messages(self, request: schemas.MessageRequest) -> schemas.MessageResponse:
        return self._post("v1/messages", request, schemas.MessageResponse)

    def response(self, request: schemas.ModelRequest) -> schemas.ModelResponse:
        return self._post("v1/responses", request, schemas.ModelResponse)

    def compact_response(
        self, request: schemas.CompactRequest
    ) -> schemas.CompactResponse:
        return self._post("v1/responses/compact", request, schemas.CompactResponse)

    def stored_response(self, response_id: str) -> schemas.ModelResponse:
        return self._get(f"v1/responses/{response_id}", schemas.ModelResponse)

    def delete_stored_response(
        self, response_id: str
    ) -> schemas.DeleteStoredCompletionResponse:
        return self._delete(
            f"v1/responses/{response_id}", schemas.DeleteStoredCompletionResponse
        )

    def response_input_items(
        self,
        response_id: str,
        *,
        limit: int | None = None,
        order: str | None = None,
        after: str | None = None,
    ) -> schemas.ListInputItemsResponse:
        return self._get(
            f"v1/responses/{response_id}/input_items",
            schemas.ListInputItemsResponse,
            params=self._without_none(limit=limit, order=order, after=after),
        )

    def tokenize_text(
        self, request: schemas.TokenizeRequest
    ) -> schemas.TokenizeResponse:
        return self._post("v1/tokenize-text", request, schemas.TokenizeResponse)

    def embeddings(
        self, request: schemas.EmbeddingRequest
    ) -> schemas.EmbeddingResponse:
        return self._post("v1/embeddings", request, schemas.EmbeddingResponse)

    def search_documents(
        self, request: schemas.SearchRequest
    ) -> schemas.SearchResponse:
        return self._post("v1/documents/search", request, schemas.SearchResponse)

    # Image and video generation

    def generate_image(
        self, request: schemas.GenerateImageRequest
    ) -> schemas.GeneratedImageResponse:
        return self._post(
            "v1/images/generations", request, schemas.GeneratedImageResponse
        )

    def edit_image(
        self, request: schemas.EditImageRequest
    ) -> schemas.GeneratedImageResponse:
        return self._post("v1/images/edits", request, schemas.GeneratedImageResponse)

    def generate_video(
        self, request: schemas.GenerateVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._post(
            "v1/videos/generations", request, schemas.StartDeferredResponse
        )

    def edit_video(
        self, request: schemas.EditVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._post("v1/videos/edits", request, schemas.StartDeferredResponse)

    def extend_video(
        self, request: schemas.ExtendVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._post(
            "v1/videos/extensions", request, schemas.StartDeferredResponse
        )

    def deferred_video(self, request_id: str) -> schemas.VideoResponse:
        return self._get(f"v1/videos/{request_id}", schemas.VideoResponse)

    # Files

    def files(
        self,
        *,
        limit: int | None = None,
        order: str | None = None,
        sort_by: str | None = None,
        pagination_token: str | None = None,
        after: str | None = None,
        filter: str | None = None,
    ) -> schemas.ListFilesResponse:
        return self._get(
            "v1/files",
            schemas.ListFilesResponse,
            params=self._without_none(
                limit=limit,
                order=order,
                sort_by=sort_by,
                pagination_token=pagination_token,
                after=after,
                filter=filter,
            ),
        )

    def upload_file(
        self,
        file: str | Path | BinaryIO | bytes,
        *,
        filename: str | None = None,
        expires_after: int | None = None,
        purpose: str | None = None,
    ) -> schemas.File:
        payload, resolved_name, close = self._file_part(file, filename)
        try:
            response = self._send_request(
                http.HTTPMethod.POST,
                "v1/files",
                data=self._without_none(expires_after=expires_after, purpose=purpose),
                files={"file": (resolved_name, payload)},
            )
            return self._parse_response_as_type(response, schemas.File, "v1/files")
        finally:
            if close:
                payload.close()

    def file(self, file_id: str) -> schemas.File:
        return self._get(f"v1/files/{file_id}", schemas.File)

    def delete_file(self, file_id: str) -> schemas.DeleteFileResponse:
        return self._delete(f"v1/files/{file_id}", schemas.DeleteFileResponse)

    def file_content(self, file_id: str, *, format: str | None = None) -> bytes:
        response = self._send_request(
            http.HTTPMethod.GET,
            f"v1/files/{file_id}/content",
            params=self._without_none(format=format),
        )
        return response.content

    def create_file_public_url(
        self, file_id: str, request: schemas.CreatePublicUrlRequest
    ) -> schemas.CreatePublicUrlResponse:
        return self._post(
            f"v1/files/{file_id}/public-url",
            request,
            schemas.CreatePublicUrlResponse,
        )

    def revoke_file_public_url(self, file_id: str) -> schemas.RevokePublicUrlResponse:
        return self._post_empty(
            f"v1/files/{file_id}/public-url/revoke",
            schemas.RevokePublicUrlResponse,
        )

    # Skills

    def skills(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
        order: str | None = None,
    ) -> schemas.SkillList:
        return self._get(
            "v1/skills",
            schemas.SkillList,
            params=self._without_none(limit=limit, after=after, order=order),
        )

    def upload_skill(self, files: list[str | Path | BinaryIO | bytes]) -> schemas.Skill:
        parts: list[tuple[str, tuple[str, Any]]] = []
        opened: list[BinaryIO] = []
        for file in files:
            payload, filename, close = self._file_part(file)
            parts.append(("files", (filename, payload)))
            if close:
                opened.append(payload)
        try:
            response = self._send_request(
                http.HTTPMethod.POST, "v1/skills", files=parts
            )
            return self._parse_response_as_type(response, schemas.Skill, "v1/skills")
        finally:
            for handle in opened:
                handle.close()

    def skill(self, skill_id: str) -> schemas.Skill:
        return self._get(f"v1/skills/{skill_id}", schemas.Skill)

    def delete_skill(self, skill_id: str) -> schemas.DeletedSkill:
        return self._delete(f"v1/skills/{skill_id}", schemas.DeletedSkill)

    def skill_content(self, skill_id: str) -> bytes:
        response = self._send_request(
            http.HTTPMethod.GET, f"v1/skills/{skill_id}/content"
        )
        return response.content

    # HTTP and parsing helpers

    def _get(
        self,
        endpoint: str,
        return_type: type[ResponseModel],
        *,
        params: dict[str, Any] | None = None,
    ) -> ResponseModel:
        response = self._send_request(http.HTTPMethod.GET, endpoint, params=params)
        return self._parse_response_as_type(response, return_type, endpoint)

    def _post(
        self,
        endpoint: str,
        request: pydantic.BaseModel,
        return_type: type[ResponseModel],
    ) -> ResponseModel:
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            json=request.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
        return self._parse_response_as_type(response, return_type, endpoint)

    def _post_empty(
        self, endpoint: str, return_type: type[ResponseModel]
    ) -> ResponseModel:
        response = self._send_request(http.HTTPMethod.POST, endpoint)
        return self._parse_response_as_type(response, return_type, endpoint)

    def _delete(self, endpoint: str, return_type: type[ResponseModel]) -> ResponseModel:
        response = self._send_request(http.HTTPMethod.DELETE, endpoint)
        return self._parse_response_as_type(response, return_type, endpoint)

    def _send_request(
        self,
        method: http.HTTPMethod,
        endpoint: str,
        *,
        additional_headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> requests_module.Response:
        headers = {"Authorization": f"Bearer {self.grok_api_key}"}
        if additional_headers:
            headers.update(additional_headers)
        kwargs.setdefault("timeout", self.timeout)
        response = self.requests.request(
            method.value,
            f"{self.GROK_API_BASE_URL}/{endpoint}",
            headers=headers,
            **kwargs,
        )
        self.unauthorized_user_error_provider.provide_error(response)
        if response.status_code == http.client.NOT_FOUND:
            raise errors.ModelNotFoundError(f"Resource not found: {endpoint}")
        if response.status_code >= 400:
            raise errors.InvalidRequestError(self._error_message(response))
        return response

    def _parse_response_as_type(
        self,
        response: requests_module.Response,
        return_type: type[ResponseModel],
        endpoint: str = "",
    ) -> ResponseModel:
        try:
            return return_type.model_validate(response.json())
        except (ValueError, pydantic.ValidationError) as exc:
            raise errors.FailedToParseResponseError(
                f"Unable to parse {self.GROK_API_BASE_URL}/{endpoint} response "
                f"as {return_type.__name__}: {response.text}"
            ) from exc

    @staticmethod
    def _without_none(**values: Any) -> dict[str, Any]:
        return {key: value for key, value in values.items() if value is not None}

    @staticmethod
    def _error_message(response: requests_module.Response) -> str:
        try:
            body = response.json()
        except ValueError:
            return response.text
        if isinstance(body, dict):
            error = body.get("error", body)
            if isinstance(error, dict):
                return str(error.get("message", error))
            return str(error)
        return str(body)

    @staticmethod
    def _file_part(
        file: str | Path | BinaryIO | bytes, filename: str | None = None
    ) -> tuple[BinaryIO | bytes, str, bool]:
        if isinstance(file, (str, Path)):
            path = Path(file)
            return path.open("rb"), filename or path.name, True
        if isinstance(file, bytes):
            return file, filename or "upload.bin", False
        return file, filename or getattr(file, "name", "upload.bin"), False
