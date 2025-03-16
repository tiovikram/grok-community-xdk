import typing

from xai_grok.schemas.message_content import MessageContent


class MessageToolResultContent(MessageContent):
    content: str
    toolUseId: str
    type: typing.Literal["tool_result"]
    isError: typing.Optional[bool] = None
