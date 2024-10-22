import typing

import pydantic

from xai_grok.schemas.choice_message import ChoiceMessage
from xai_grok.schemas.logprobs import Logprobs


class Choice(pydantic.BaseModel):
    finish_reason: typing.Optional[str] = None
    index: int
    logprobs: typing.Optional[Logprobs] = None
    message: ChoiceMessage
