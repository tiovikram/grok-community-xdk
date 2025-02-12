import datetime
import typing

import pydantic

from xai_grok.schemas.sample_choice import SampleChoice
from xai_grok.schemas.usage import Usage


class SampleResponse(pydantic.BaseModel):
    choices: typing.List[SampleChoice]
    created: datetime.datetime
    id: str
    model: str
    object: str
    system_fingerprint: typing.Optional[str] = None
    usage: typing.Optional[Usage] = None
