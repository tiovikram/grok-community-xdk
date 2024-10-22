import typing

import pydantic

from xai_grok.schemas.language_model import LanguageModel


class LanguageModels(pydantic.BaseModel):
    models: typing.List[LanguageModel]
