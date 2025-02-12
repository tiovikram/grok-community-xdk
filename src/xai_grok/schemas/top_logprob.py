import typing

import pydantic


class TopLogprob(pydantic.BaseModel):
    bytes: typing.Optional[typing.List[int]] = None
    logprob: float
    token: str
