import datetime
import typing

import pydantic

from xai_grok.schemas.choice import Choice
from xai_grok.schemas.usage import Usage


class ChatResponse(pydantic.BaseModel):
    id: str
    object: str
    created: datetime.datetime
    model: str
    choices: typing.List[Choice]
    system_fingerprint: typing.Optional[str] = None
    usage: typing.Optional[Usage] = None
