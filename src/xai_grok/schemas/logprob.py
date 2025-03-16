import typing

import pydantic

from xai_grok.schemas.top_logprob import TopLogprob


class Logprob(pydantic.BaseModel):
    bytes: typing.Optional[typing.List[int]] = None
    logprob: float
    token: str
    top_logprobs: typing.List[TopLogprob]
