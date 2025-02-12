import typing

from xai_grok.schemas.message_content import MessageContent
from xai_grok.schemas.message_image_source import MessageImageSource


class MessageImageContent(MessageContent):
    type: typing.Literal["image"]
    source: MessageImageSource
