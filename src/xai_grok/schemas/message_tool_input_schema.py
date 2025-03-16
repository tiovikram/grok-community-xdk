import typing

import pydantic


class MessageToolInputSchema(pydantic.BaseModel):
    properties: typing.Optional[str] = None
    type: str
