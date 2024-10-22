import pydantic


class MessageUsage(pydantic.BaseModel):
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    input_tokens: int
    output_tokens: int
