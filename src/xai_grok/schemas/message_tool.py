import typing

import pydantic

from xai_grok.schemas.message_tool_input_schema import MessageToolInputSchema


class MessageTool(pydantic.BaseModel):
    cache_control: typing.Optional[str] = None
    description: typing.Optional[str] = None
    input_schema: MessageToolInputSchema
    name: str
