import typing

import pydantic

from xai_grok.schemas.content_part import ContentPart
from xai_grok.schemas.role import Role


class ChatMessage(pydantic.BaseModel):
    content: typing.Union[str, ContentPart]
    name: typing.Optional[str] = None
    role: Role
