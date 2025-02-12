import typing

import pydantic


class Embedding(pydantic.BaseModel):
    embedding: typing.Union[typing.List[float], str]
    index: int
    object: typing.Literal["embedding"]
