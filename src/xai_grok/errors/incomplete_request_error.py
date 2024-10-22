class IncompleteRequestError(Exception):
    """
    Error occurs when request body is missing fields

    params:
        message: the error message
    """

    def __init__(self, message: str):
        super().__init__(message)
