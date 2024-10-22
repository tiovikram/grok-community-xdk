import typing

import pydantic


class MessageContent(pydantic.BaseModel):
    cacheControl: typing.Optional[str] = None
    type: str
