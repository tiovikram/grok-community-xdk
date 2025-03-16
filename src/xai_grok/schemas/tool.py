import typing

import pydantic

from xai_grok.schemas.tool_function import ToolFunction


class Tool(pydantic.BaseModel):
    function: ToolFunction
    type: typing.Literal["function"]
