import pydantic


class APIModel(pydantic.BaseModel):
    """Base for evolving xAI payloads while retaining typed known fields."""

    model_config = pydantic.ConfigDict(extra="allow")
