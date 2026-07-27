import http

import xai_grok.errors as errors


class UnauthorizedUserErrorProvider:

    _NO_API_KEY_PROVIDED_MESSAGE = "No API Key provided"
    _INVALID_API_KEY_PROVIDED_MESSAGE = "Invalid API Key provided"

    def provide_error(self, response) -> None:
        if response.status_code not in (
            http.client.BAD_REQUEST,
            http.client.UNAUTHORIZED,
            http.client.FORBIDDEN,
        ):
            return
        try:
            parsed_response_body = response.json()
        except ValueError:
            parsed_response_body = response.text
        if isinstance(parsed_response_body, dict):
            error = parsed_response_body.get("error", parsed_response_body)
            error_message = (
                error.get("message", str(error))
                if isinstance(error, dict)
                else str(error)
            )
        else:
            error_message = str(parsed_response_body)
        if self._NO_API_KEY_PROVIDED_MESSAGE.lower() in error_message.lower():
            raise errors.NoAPIKeyProvidedError(str(parsed_response_body))
        if self._INVALID_API_KEY_PROVIDED_MESSAGE.lower() in error_message.lower():
            raise errors.InvalidAPIKeyProvidedError(str(parsed_response_body))
        if response.status_code in (http.client.UNAUTHORIZED, http.client.FORBIDDEN):
            raise errors.UnauthorizedUserError(str(parsed_response_body))
