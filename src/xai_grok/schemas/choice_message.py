import typing

import pydantic

from xai_grok.schemas.tool_call import ToolCall


class ChoiceMessage(pydantic.BaseModel):
    role: str
    content: typing.Optional[str] = None
    refusal: typing.Optional[str] = None
    tool_calls: typing.Optional[typing.List[ToolCall]] = None
