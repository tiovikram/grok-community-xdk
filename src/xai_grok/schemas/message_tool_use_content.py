import typing

from xai_grok.schemas.message_content import MessageContent


class MessageToolUseContent(MessageContent):
    type: typing.Literal["tool_use"]
    id: str
    input: str
    name: str
