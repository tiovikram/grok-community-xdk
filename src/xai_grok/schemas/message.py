import typing

import pydantic

from xai_grok.schemas.message_text_content import MessageTextContent
from xai_grok.schemas.message_image_content import MessageImageContent
from xai_grok.schemas.message_tool_use_content import MessageToolUseContent
from xai_grok.schemas.message_tool_result_content import MessageToolResultContent


class Message(pydantic.BaseModel):
    content: typing.Union[
        typing.List[
            typing.Union[
                MessageTextContent,
                MessageImageContent,
                MessageToolUseContent,
                MessageToolResultContent,
            ]
        ],
        str,
    ]
    role: str
