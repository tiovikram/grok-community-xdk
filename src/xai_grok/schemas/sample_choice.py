import pydantic


class SampleChoice(pydantic.BaseModel):
    finish_reason: str
    index: int
    text: str
