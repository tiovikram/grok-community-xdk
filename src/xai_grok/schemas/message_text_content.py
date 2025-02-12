import typing

from xai_grok.schemas.message_content import MessageContent


class MessageTextContent(MessageContent):
    type: typing.Literal["text"]
    text: str
