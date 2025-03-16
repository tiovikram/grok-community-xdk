import typing

from xai_grok.schemas.message import Message
from xai_grok.schemas.tool_call import ToolCall


class ToolCallMessage(Message):
    role: typing.Literal["assistant"]
    toolCalls: typing.Optional[typing.List[ToolCall]]
