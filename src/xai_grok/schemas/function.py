import pydantic


class Function(pydantic.BaseModel):
    name: str
    arguments: str
