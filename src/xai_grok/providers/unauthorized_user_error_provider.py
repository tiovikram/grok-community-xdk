import http

import xai_grok.errors as errors


class UnauthorizedUserErrorProvider:

    _NO_API_KEY_PROVIDED_MESSAGE = "Invalid Authorization header 'Bearer'"
    _BAD_CREDENTIALS_MESSAGE = "Bad credentials"
    _INVALID_API_KEY_PROVIDED_MESSAGE = "Incorrect API key provided"

    def provide_error(self, response: dict) -> errors.UnauthorizedUserError:
        if response.status_code in (
            http.client.BAD_REQUEST,
            http.client.UNAUTHORIZED,
            http.client.FORBIDDEN,
        ):
            parsed_response_body = response.json()
            error_message = parsed_response_body["error"]
            if (
                self._NO_API_KEY_PROVIDED_MESSAGE in error_message
                or self._BAD_CREDENTIALS_MESSAGE in error_message
            ):
                raise errors.NoAPIKeyProvidedError(str(parsed_response_body))
            if self._INVALID_API_KEY_PROVIDED_MESSAGE in error_message:
                raise errors.InvalidAPIKeyProvidedError(str(parsed_response_body))
