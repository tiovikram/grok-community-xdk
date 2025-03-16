import pydantic


class TokenizeTextRequest(pydantic.BaseModel):
    model: str
    text: str
