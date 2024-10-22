import typing

import pydantic


class CompleteResponse(pydantic.BaseModel):
    completion: str
    id: str
    model: str
    stop_reason: typing.Optional[str] = None
    type: str
