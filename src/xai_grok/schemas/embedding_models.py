import typing

import pydantic

from xai_grok.schemas.embedding_model import EmbeddingModel


class EmbeddingModels(pydantic.BaseModel):
    models: typing.List[EmbeddingModel]
