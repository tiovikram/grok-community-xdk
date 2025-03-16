import typing

import pydantic

from xai_grok.schemas.function import Function


class ToolCall(pydantic.BaseModel):
    id: str
    function: Function
    index: typing.Optional[int]
    type: typing.Optional[str]
