import typing

import pydantic

from xai_grok.schemas.model import Model


class LanguageModel(Model):
    version: str
    input_modalities: typing.List[str]
    output_modalities: typing.List[str]
    prompt_text_token_price: float
    prompt_image_token_price: float
    completion_text_token_price: float
