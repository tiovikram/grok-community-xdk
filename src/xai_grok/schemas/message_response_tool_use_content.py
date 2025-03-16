import typing

import pydantic


class MessageResponseToolUseContent(pydantic.BaseModel):
    id: str
    input: str
    name: str
    type: typing.Literal["tool_use"]
