import pydantic


class EmbeddingUsage(pydantic.BaseModel):
    prompt_tokens: int
    total_tokens: int
