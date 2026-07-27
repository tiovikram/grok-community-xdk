import typing

from xai_grok.schemas.api_model import APIModel


class SearchRequest(APIModel):
    query: str
    source: typing.Any


class SearchResponse(APIModel):
    matches: typing.List[typing.Any]
