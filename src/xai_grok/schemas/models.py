import typing

import pydantic

from xai_grok.schemas.model import Model


class Models(pydantic.BaseModel):
    data: typing.List[Model]
