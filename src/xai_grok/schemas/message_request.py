import typing

import pydantic

from xai_grok.schemas.message import Message
from xai_grok.schemas.message_metadata import MessageMetadata
from xai_grok.schemas.message_text_content import MessageTextContent
from xai_grok.schemas.message_tool_choice import MessageToolChoice
from xai_grok.schemas.message_tool import MessageTool


class MessageRequest(pydantic.BaseModel):
    max_tokens: int
    messages: typing.List[Message]
    metadata: typing.Optional[MessageMetadata] = None
    model: str
    stop_sequences: typing.Optional[typing.List[str]] = None
    stream: typing.Optional[bool] = None
    system: typing.Optional[typing.Union[str, typing.List[MessageTextContent]]] = None
    temperature: typing.Optional[float] = None
    tool_choice: typing.Optional[typing.List[MessageTool]] = None
    top_k: typing.Optional[int] = None
    top_p: typing.Optional[float] = None
