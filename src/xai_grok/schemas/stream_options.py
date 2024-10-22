import pydantic


class StreamOptions(pydantic.BaseModel):
    include_usage: bool
