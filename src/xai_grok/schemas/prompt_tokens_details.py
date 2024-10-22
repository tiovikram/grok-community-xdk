import pydantic


class PromptTokensDetails(pydantic.BaseModel):
    audio_tokens: int
    cached_tokens: int
    image_tokens: int
    text_tokens: int
