import typing

import pydantic

from xai_grok.schemas.complete_request_metadata import CompleteRequestMetadata


class CompleteRequest(pydantic.BaseModel):
    max_tokens_to_sample: int
    metadata: typing.Optional[CompleteRequestMetadata] = None
    model: str
    prompt: str
    stop_sequences: typing.List[str] = None
    stream: typing.Optional[bool] = None
    temperature: typing.Optional[float] = None
    top_k: typing.Optional[int] = None
    top_p: typing.Optional[float] = None
