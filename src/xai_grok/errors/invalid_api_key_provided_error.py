from xai_grok.errors.unauthorized_user_error import UnauthorizedUserError


class InvalidAPIKeyProvidedError(UnauthorizedUserError):

    def __init__(self, message: str):
        super().__init__(message)
