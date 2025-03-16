import typing

import pydantic


class MessageMetadata(pydantic.BaseModel):
    user_id: typing.Optional[str] = None
