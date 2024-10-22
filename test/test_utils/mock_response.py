import http.client
import json
import typing


class MockResponse:

    def __init__(self, body: typing.Dict, http_status_code: int = http.client.OK):
        self.body = body
        self.http_status_code = http_status_code

    @property
    def text(self):
        return str(self.body)

    @property
    def status_code(self):
        return self.http_status_code

    def json(self):
        return self.body
