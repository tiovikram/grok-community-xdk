import http


class UnsupportedHttpMethodError(Exception):

    def __init__(self, http_method: http.HTTPMethod):
        super().__init__(f"Unsupported HTTP Method: {http_method}")
