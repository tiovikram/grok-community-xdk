import pydantic


class MessageImageSource(pydantic.BaseModel):
    data: str
    media_type: str
    type: str
