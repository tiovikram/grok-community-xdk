import typing

import pydantic


class CompleteRequestMetadata(pydantic.BaseModel):
    user_id: typing.Optional[str] = None
