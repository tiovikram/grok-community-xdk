from xai_grok.errors.unauthorized_user_error import UnauthorizedUserError


class NoAPIKeyProvidedError(UnauthorizedUserError):

    def __init__(self, message: str):
        super().__init__(message)
