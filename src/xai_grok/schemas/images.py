import typing

from xai_grok.schemas.api_model import APIModel


class ImageGenerationModel(APIModel):
    id: str
    fingerprint: str
    max_prompt_length: int
    created: int
    object: str
    owned_by: str
    version: str
    input_modalities: typing.List[str]
    output_modalities: typing.List[str]
    image_price: float
    aliases: typing.List[str]


class ImageGenerationModels(APIModel):
    models: typing.List[ImageGenerationModel]


class GenerateImageRequest(APIModel):
    prompt: typing.Optional[str] = None
    model: typing.Optional[str] = None
    n: typing.Optional[int] = 1
    response_format: typing.Optional[str] = "url"
    aspect_ratio: typing.Optional[str] = None
    resolution: typing.Optional[str] = None
    user: typing.Optional[str] = None


class EditImageRequest(GenerateImageRequest):
    prompt: str
    image: typing.Optional[typing.Any] = None
    images: typing.Optional[typing.List[typing.Any]] = None


class GeneratedImageResponse(APIModel):
    data: typing.List[typing.Any]
