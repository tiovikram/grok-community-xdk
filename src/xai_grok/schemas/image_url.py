import typing
import pydantic


class ImageUrl(pydantic.BaseModel):
    detail: typing.Optional[str]
    url: str
