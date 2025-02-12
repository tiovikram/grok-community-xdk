import typing

import pydantic

from xai_grok.schemas.prompt_tokens_details import PromptTokensDetails


class Usage(pydantic.BaseModel):
    completion_tokens: int
    prompt_tokens: int
    prompt_tokens_details: typing.Optional[PromptTokensDetails] = None
    total_tokens: int
