import typing

import pydantic


class FunctionToolChoice(pydantic.BaseModel):
    name: typing.Optional[str]
