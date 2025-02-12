import typing

import pydantic


class MessageResponseTextContent(pydantic.BaseModel):
    text: str
    type: typing.Literal["text"]
