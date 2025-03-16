import typing

import pydantic

from xai_grok.schemas.stream_options import StreamOptions


class SampleRequest(pydantic.BaseModel):
    best_of: typing.Optional[int] = None
    echo: typing.Optional[bool] = None
    frequency_penalty: typing.Optional[float] = None
    logit_bias: typing.Optional[typing.Dict[int, float]] = None
    logprobs: typing.Optional[bool] = None
    max_tokens: typing.Optional[int] = None
    model: str
    n: typing.Optional[int] = None
    presence_penalty: typing.Optional[float] = None
    prompt: typing.Union[str, typing.List[str]]
    seed: typing.Optional[int] = None
    stop: typing.Optional[typing.List[str]] = None
    stream: typing.Optional[bool] = None
    stream_options: typing.Optional[StreamOptions] = None
    suffix: typing.Optional[str] = None
    temperature: typing.Optional[float] = None
    top_p: typing.Optional[float] = None
    user: typing.Optional[str] = None
