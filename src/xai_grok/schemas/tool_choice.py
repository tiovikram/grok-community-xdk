import typing

import pydantic

from xai_grok.schemas.function_tool_choice import FunctionToolChoice


class ToolChoice(pydantic.BaseModel):
    type: typing.Literal["function"]
    function: typing.Optional[FunctionToolChoice] = None
