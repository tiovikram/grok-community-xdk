import typing

import pydantic


class EmbeddingRequest(pydantic.BaseModel):
    dimensions: typing.Optional[int] = None
    encoding_format: typing.Optional[str] = None
    input: typing.Union[int, typing.List[int], typing.List[str], str]
    model: str
    preview: typing.Optional[bool] = None
    user: typing.Optional[str] = None
