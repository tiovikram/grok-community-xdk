import typing

import pydantic


class MessageToolChoice(pydantic.BaseModel):
    name: typing.Optional[str] = None
    type: str
