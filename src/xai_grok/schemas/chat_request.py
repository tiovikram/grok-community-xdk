import typing
import pydantic

from xai_grok.schemas.message import Message
from xai_grok.schemas.stream_options import StreamOptions
from xai_grok.schemas.tool import Tool
from xai_grok.schemas.tool_choice import ToolChoice


class ChatRequest(pydantic.BaseModel):
    frequency_penalty: typing.Optional[float] = None
    logit_bias: typing.Optional[typing.Dict[str, float]] = None
    logprobs: typing.Optional[bool] = None
    max_tokens: typing.Optional[int] = None
    messages: typing.List[Message]
    model: str
    n: typing.Optional[int] = None
    presence_penalty: typing.Optional[float] = None
    seed: typing.Optional[int] = None
    stop: typing.Optional[typing.List[str]] = None
    stream: typing.Optional[bool] = None
    stream_options: typing.Optional[StreamOptions] = None
    temperature: typing.Optional[float] = None
    tool_choice: typing.Optional[ToolChoice] = None
    tools: typing.Optional[typing.List[Tool]] = None
    top_logprobs: typing.Optional[int] = None
    top_p: typing.Optional[float] = None
    user: typing.Optional[str] = None
