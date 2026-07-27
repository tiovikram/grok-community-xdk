import http
import logging

import pydantic
import requests

import xai_grok.errors as errors
import xai_grok.providers as providers
import xai_grok.schemas as schemas


class Grok:

    GROK_API_BASE_URL = "https://api.x.ai"

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        api_key: str,
        requests: requests,
        unauthorized_user_error_provider: providers.UnauthorizedUserErrorProvider,
    ):
        self.grok_api_key = api_key
        self.requests = requests
        self.unauthorized_user_error_provider = unauthorized_user_error_provider

    def api_key(self) -> schemas.APIKey:
        endpoint = "v1/api-key"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(response, schemas.APIKey, endpoint=endpoint)

    def chat_completions(self, request: schemas.ChatRequest) -> schemas.ChatResponse:
        endpoint = "v1/chat/completions"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        elif response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.ChatResponse, endpoint=endpoint
        )

    def complete(self, request: schemas.CompleteRequest) -> schemas.CompleteResponse:
        endpoint = "v1/complete"
        self.logger.warning("Using legacy endpoint: POST https://api.x.ai/v1/complete")
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        elif response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.CompleteResponse, endpoint=endpoint
        )

    def completions(self, request: schemas.SampleRequest) -> schemas.SampleResponse:
        endpoint = "v1/completions"
        self.logger.warning(
            "Using legacy endpoint: POST https://api.x.ai/v1/completions. "
            "This endpoint is deprecated, please use POST https://api.x.ai/v1/chat/completions instead."
        )
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        if response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.SampleResponse, endpoint=endpoint
        )

    def embedding_model(self, model_id: str) -> schemas.EmbeddingModel:
        endpoint = f"v1/embedding-models/{model_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        if response.status_code == http.client.NOT_FOUND:
            raise errors.ModelNotFoundError(f"Embedding Model {model_id} not found")
        return self._parse_response_as_type(
            response, schemas.EmbeddingModel, endpoint=endpoint
        )

    def embedding_models(self) -> schemas.EmbeddingModels:
        endpoint = "v1/embedding-models"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.EmbeddingModels, endpoint=endpoint
        )

    def embeddings(
        self, request: schemas.EmbeddingRequest
    ) -> schemas.EmbeddingResponse:
        endpoint = "v1/embeddings"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        if response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.EmbeddingResponse, endpoint=endpoint
        )

    def language_model(self, model_id: str) -> schemas.LanguageModel:
        endpoint = f"v1/language-models/{model_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        if response.status_code == http.client.NOT_FOUND:
            raise (errors.ModelNotFoundError(f"Language Model {model_id} not found"))
        return self._parse_response_as_type(
            response, schemas.LanguageModel, endpoint=endpoint
        )

    def language_models(self) -> schemas.LanguageModels:
        endpoint = "v1/language-models"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.LanguageModels, endpoint=endpoint
        )

    def messages(self, request: schemas.MessageRequest) -> schemas.MessageResponse:
        endpoint = "v1/messages"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        if response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.MessageResponse, endpoint=endpoint
        )

    def model(self, model_id: str) -> schemas.Model:
        endpoint = f"v1/models/{model_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        if response.status_code == http.client.NOT_FOUND:
            raise errors.ModelNotFoundError(f"Model {model_id} not found")
        return self._parse_response_as_type(response, schemas.Model, endpoint=endpoint)

    def models(self) -> schemas.Models:
        endpoint = "v1/models"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(response, schemas.Models, endpoint=endpoint)

    def deferred_chat_completion(self, request_id: str) -> schemas.ChatResponse:
        endpoint = f"v1/chat/deferred-completion/{request_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.ChatResponse, endpoint=endpoint
        )

    def me(self) -> schemas.GetMeResponse:
        endpoint = "v1/me"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.GetMeResponse, endpoint=endpoint
        )

    def search_documents(
        self, request: schemas.SearchRequest
    ) -> schemas.SearchResponse:
        endpoint = "v1/documents/search"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.SearchResponse, endpoint=endpoint
        )

    def responses(self, request: schemas.ModelRequest) -> schemas.ModelResponse:
        endpoint = "v1/responses"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.ModelResponse, endpoint=endpoint
        )

    def compact_response(
        self, request: schemas.CompactRequest
    ) -> schemas.CompactResponse:
        endpoint = "v1/responses/compact"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.CompactResponse, endpoint=endpoint
        )

    def stored_response(self, response_id: str) -> schemas.ModelResponse:
        endpoint = f"v1/responses/{response_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.ModelResponse, endpoint=endpoint
        )

    def delete_stored_response(
        self, response_id: str
    ) -> schemas.DeleteStoredCompletionResponse:
        endpoint = f"v1/responses/{response_id}"
        response = self._send_request(http.HTTPMethod.DELETE, endpoint)
        return self._parse_response_as_type(
            response, schemas.DeleteStoredCompletionResponse, endpoint=endpoint
        )

    def response_input_items(
        self,
        response_id: str,
        limit: int = None,
        order: str = None,
        after: str = None,
    ) -> schemas.ListInputItemsResponse:
        endpoint = f"v1/responses/{response_id}/input_items"
        params = {"limit": limit, "order": order, "after": after}
        response = self._send_request(
            http.HTTPMethod.GET,
            endpoint,
            params={key: value for key, value in params.items() if value is not None},
        )
        return self._parse_response_as_type(
            response, schemas.ListInputItemsResponse, endpoint=endpoint
        )

    def files(
        self,
        limit: int = None,
        order: str = None,
        sort_by: str = None,
        pagination_token: str = None,
        after: str = None,
        filter: str = None,
    ) -> schemas.ListFilesResponse:
        endpoint = "v1/files"
        params = {
            "limit": limit,
            "order": order,
            "sort_by": sort_by,
            "pagination_token": pagination_token,
            "after": after,
            "filter": filter,
        }
        response = self._send_request(
            http.HTTPMethod.GET,
            endpoint,
            params={key: value for key, value in params.items() if value is not None},
        )
        return self._parse_response_as_type(
            response, schemas.ListFilesResponse, endpoint=endpoint
        )

    def upload_file(
        self,
        filename: str,
        content: bytes,
        expires_after: int = None,
        purpose: str = None,
    ) -> schemas.File:
        endpoint = "v1/files"
        form = {"expires_after": expires_after, "purpose": purpose}
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            data={key: value for key, value in form.items() if value is not None},
            files={"file": (filename, content)},
        )
        return self._parse_response_as_type(response, schemas.File, endpoint=endpoint)

    def file(self, file_id: str) -> schemas.File:
        endpoint = f"v1/files/{file_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(response, schemas.File, endpoint=endpoint)

    def delete_file(self, file_id: str) -> schemas.DeleteFileResponse:
        endpoint = f"v1/files/{file_id}"
        response = self._send_request(http.HTTPMethod.DELETE, endpoint)
        return self._parse_response_as_type(
            response, schemas.DeleteFileResponse, endpoint=endpoint
        )

    def file_content(self, file_id: str, format: str = None) -> bytes:
        endpoint = f"v1/files/{file_id}/content"
        response = self._send_request(
            http.HTTPMethod.GET,
            endpoint,
            params={"format": format} if format else None,
        )
        return response.content

    def create_file_public_url(
        self, file_id: str, request: schemas.CreatePublicUrlRequest
    ) -> schemas.CreatePublicUrlResponse:
        endpoint = f"v1/files/{file_id}/public-url"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.CreatePublicUrlResponse, endpoint=endpoint
        )

    def revoke_file_public_url(self, file_id: str) -> schemas.RevokePublicUrlResponse:
        endpoint = f"v1/files/{file_id}/public-url/revoke"
        response = self._send_request(http.HTTPMethod.POST, endpoint)
        return self._parse_response_as_type(
            response, schemas.RevokePublicUrlResponse, endpoint=endpoint
        )

    def image_generation_models(self) -> schemas.ImageGenerationModels:
        endpoint = "v1/image-generation-models"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.ImageGenerationModels, endpoint=endpoint
        )

    def image_generation_model(self, model_id: str) -> schemas.ImageGenerationModel:
        endpoint = f"v1/image-generation-models/{model_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.ImageGenerationModel, endpoint=endpoint
        )

    def generate_image(
        self, request: schemas.GenerateImageRequest
    ) -> schemas.GeneratedImageResponse:
        endpoint = "v1/images/generations"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.GeneratedImageResponse, endpoint=endpoint
        )

    def edit_image(
        self, request: schemas.EditImageRequest
    ) -> schemas.GeneratedImageResponse:
        endpoint = "v1/images/edits"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.GeneratedImageResponse, endpoint=endpoint
        )

    def skills(
        self, limit: int = None, after: str = None, order: str = None
    ) -> schemas.SkillList:
        endpoint = "v1/skills"
        params = {"limit": limit, "after": after, "order": order}
        response = self._send_request(
            http.HTTPMethod.GET,
            endpoint,
            params={key: value for key, value in params.items() if value is not None},
        )
        return self._parse_response_as_type(
            response, schemas.SkillList, endpoint=endpoint
        )

    def upload_skill(self, filename: str, content: bytes) -> schemas.Skill:
        endpoint = "v1/skills"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            files=[("files", (filename, content))],
        )
        return self._parse_response_as_type(response, schemas.Skill, endpoint=endpoint)

    def skill(self, skill_id: str) -> schemas.Skill:
        endpoint = f"v1/skills/{skill_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(response, schemas.Skill, endpoint=endpoint)

    def delete_skill(self, skill_id: str) -> schemas.DeletedSkill:
        endpoint = f"v1/skills/{skill_id}"
        response = self._send_request(http.HTTPMethod.DELETE, endpoint)
        return self._parse_response_as_type(
            response, schemas.DeletedSkill, endpoint=endpoint
        )

    def skill_content(self, skill_id: str) -> bytes:
        endpoint = f"v1/skills/{skill_id}/content"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return response.content

    def video_generation_models(self) -> schemas.VideoGenerationModels:
        endpoint = "v1/video-generation-models"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.VideoGenerationModels, endpoint=endpoint
        )

    def video_generation_model(self, model_id: str) -> schemas.VideoGenerationModel:
        endpoint = f"v1/video-generation-models/{model_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.VideoGenerationModel, endpoint=endpoint
        )

    def generate_video(
        self, request: schemas.GenerateVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._video_request("v1/videos/generations", request)

    def edit_video(
        self, request: schemas.EditVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._video_request("v1/videos/edits", request)

    def extend_video(
        self, request: schemas.ExtendVideoRequest
    ) -> schemas.StartDeferredResponse:
        return self._video_request("v1/videos/extensions", request)

    def _video_request(
        self, endpoint: str, request: pydantic.BaseModel
    ) -> schemas.StartDeferredResponse:
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        return self._parse_response_as_type(
            response, schemas.StartDeferredResponse, endpoint=endpoint
        )

    def deferred_video(self, request_id: str) -> schemas.VideoResponse:
        endpoint = f"v1/videos/{request_id}"
        response = self._send_request(http.HTTPMethod.GET, endpoint)
        return self._parse_response_as_type(
            response, schemas.VideoResponse, endpoint=endpoint
        )

    def tokenize_text(
        self, request: schemas.TokenizeTextRequest
    ) -> schemas.TokenizeTextResponse:
        endpoint = f"v1/tokenize-text"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        elif response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.TokenizeTextResponse, endpoint=endpoint
        )

    def _send_request(
        self,
        method: http.HTTPMethod,
        endpoint: str,
        additional_headers: dict = None,
        request_body: dict = None,
        params: dict = None,
        data: dict = None,
        files=None,
    ) -> requests.Response:
        headers = {"Authorization": f"Bearer {self.grok_api_key}"}
        if files is None:
            headers["Content-Type"] = "application/json"
        if additional_headers:
            headers.update(additional_headers)
        if method == http.HTTPMethod.GET:
            response = self.requests.get(
                f"{self.GROK_API_BASE_URL}/{endpoint}",
                headers=headers,
                params=params,
            )
        elif method == http.HTTPMethod.POST:
            response = self.requests.post(
                f"{self.GROK_API_BASE_URL}/{endpoint}",
                headers=headers,
                json=request_body,
                data=data,
                files=files,
            )
        elif method == http.HTTPMethod.DELETE:
            response = self.requests.delete(
                f"{self.GROK_API_BASE_URL}/{endpoint}", headers=headers
            )
        else:
            raise errors.UnsupportedHttpMethodError(method)

        self.unauthorized_user_error_provider.provide_error(response)
        return response

    def _parse_response_as_type(
        self, response: requests.Response, return_type: "class", endpoint: str = ""
    ) -> pydantic.BaseModel:
        """
        Parse the HTTP response as a specified return type

        args:
            response: the HTTP response
            return_type: the desired return type
            request_url: the URL the request was sent to
        raises:
            errors.FailedToParseResponseError: if response data cannot be parsed
            as desired return type
        returns: an instance of the desired return type
        """
        try:
            return return_type(**response.json())
        except pydantic.ValidationError as e:
            raise errors.FailedToParseResponseError(
                f"Unable to parse {self.GROK_API_BASE_URL + '/' + endpoint if endpoint else ''} API response {response.text} as type {return_type.__name__}"
            )
