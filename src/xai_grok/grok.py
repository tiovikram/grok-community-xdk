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
        self.logger.warning("Using legacy endpoint: POST https://api.x.ai/v1/messages")
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump_json(exclude_none=True),
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
        endpoint = f"v1/embedding-model/{model_id}"
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
            request_body=request.model_dump_json(exclude_none=True),
        )
        if response.status_code == http.client.BAD_REQUEST:
            raise errors.InvalidRequestError(response.text)
        if response.status_code == http.client.UNPROCESSABLE_ENTITY:
            raise errors.IncompleteRequestError(response.text)
        return self._parse_response_as_type(
            response, schemas.EmbeddingResponse, endpoint=endpoint
        )

    def language_model(self, model_id: str) -> schemas.LanguageModel:
        endpoint = f"v1/langauge-models/{model_id}"
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

    def tokenize_text(
        self, request: schemas.TokenizeTextRequest
    ) -> schemas.TokenizeTextResponse:
        endpoint = f"v1/tokenize-text"
        response = self._send_request(
            http.HTTPMethod.POST,
            endpoint,
            request_body=request.model_dump_json(exclude_none=True),
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
        additional_headers: dict = {},
        request_body: dict = None,
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.grok_api_key}",
            "Content-Type": "application/json",
        } | additional_headers
        if method == http.HTTPMethod.GET:
            response = self.requests.get(
                f"{self.GROK_API_BASE_URL}/{endpoint}", headers=headers
            )
        elif method == http.HTTPMethod.POST:
            response = self.requests.post(
                f"{self.GROK_API_BASE_URL}/{endpoint}",
                headers=headers,
                json=request_body,
            )
        else:
            raise UnsupportedHttpMethod(http_method)

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
