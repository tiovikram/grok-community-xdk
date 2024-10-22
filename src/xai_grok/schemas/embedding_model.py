import typing

from xai_grok.schemas.model import Model


class EmbeddingModel(Model):
    version: str
    input_modalities: typing.List[str]
    prompt_text_token_price: float
    prompt_image_token_price: float
