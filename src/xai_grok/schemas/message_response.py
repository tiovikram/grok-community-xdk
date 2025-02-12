import typing

import pydantic

from xai_grok.schemas.message_response_text_content import MessageResponseTextContent
from xai_grok.schemas.message_response_tool_use_content import MessageResponseToolUseContent
from xai_grok.schemas.message_usage import MessageUsage


class MessageResponse(pydantic.BaseModel):
    content: typing.List[
        typing.Union[MessageResponseTextContent, MessageResponseToolUseContent]
    ]
    id: str
    model: str
    role: str
    stop_reason: typing.Optional[str] = None
    stop_sequence: typing.Optional[str] = None
    type: str
    usage: MessageUsage
