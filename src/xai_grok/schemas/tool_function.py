import typing

import pydantic


class ToolFunction(pydantic.BaseModel):
    description: typing.Optional[str] = None
    name: str
    parameters: typing.Dict[typing.Any, typing.Any]
    strict: typing.Optional[bool] = None
