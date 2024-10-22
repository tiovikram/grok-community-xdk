import typing

import pydantic

from xai_grok.schemas.logprob import Logprob


class Logprobs(pydantic.BaseModel):
    content: typing.Optional[typing.List[Logprob]] = None
