import typing

import pydantic


class TokenizeTextResponse(pydantic.BaseModel):
    token_ids: typing.List[str]
