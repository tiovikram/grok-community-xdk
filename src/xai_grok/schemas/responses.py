import typing

from xai_grok.schemas.api_model import APIModel


class ModelRequest(APIModel):
    input: typing.Any
    model: typing.Optional[str] = None


class ModelResponse(APIModel):
    created_at: int
    id: str
    model: str
    object: str
    output: typing.List[typing.Any]
    parallel_tool_calls: bool
    text: typing.Any
    tool_choice: typing.Any
    tools: typing.List[typing.Any]
    status: str
    store: bool
    metadata: typing.Any
    background: bool
    service_tier: typing.Any
    truncation: typing.Any
    top_logprobs: int
    presence_penalty: float
    frequency_penalty: float


class CompactRequest(APIModel):
    input: typing.Any
    model: str


class CompactResponse(APIModel):
    object: str
    id: str
    created_at: int
    model: str
    output: typing.List[typing.Any]


class DeleteStoredCompletionResponse(APIModel):
    id: str
    object: str
    deleted: bool


class ListInputItemsResponse(APIModel):
    object: str
    data: typing.List[typing.Any]
    has_more: bool
