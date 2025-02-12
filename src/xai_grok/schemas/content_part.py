import typing

import pydantic

from xai_grok.schemas.image_url import ImageUrl


class ContentPart(pydantic.BaseModel):
    detail: typing.Optional[str] = None
    image_url: typing.Optional[ImageUrl] = None
    text: typing.Optional[str] = None
    text_file: typing.Optional[str] = None
    type: str
