import typing

import pydantic

from xai_grok.schemas.embedding import Embedding
from xai_grok.schemas.embedding_usage import EmbeddingUsage


class EmbeddingResponse(pydantic.BaseModel):
    data: typing.List[Embedding]
    model: str
    object: typing.Literal["list"]
    usage: typing.Optional[EmbeddingUsage] = None
