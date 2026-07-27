import typing

from xai_grok.schemas.api_model import APIModel


class VideoGenerationModel(APIModel):
    id: str
    fingerprint: str
    created: int
    object: str
    owned_by: str
    version: str
    input_modalities: typing.List[str]
    output_modalities: typing.List[str]
    aliases: typing.List[str]


class VideoGenerationModels(APIModel):
    models: typing.List[VideoGenerationModel]


class GenerateVideoRequest(APIModel):
    prompt: typing.Optional[str] = None
    model: typing.Optional[str] = None
    duration: typing.Optional[int] = 8
    aspect_ratio: typing.Optional[str] = None
    resolution: typing.Optional[str] = None
    image: typing.Optional[typing.Any] = None
    reference_images: typing.Optional[typing.List[typing.Any]] = None
    user: typing.Optional[str] = None


class EditVideoRequest(APIModel):
    prompt: str
    video: typing.Any
    model: typing.Optional[str] = None
    user: typing.Optional[str] = None


class ExtendVideoRequest(EditVideoRequest):
    duration: typing.Optional[int] = None


class StartDeferredResponse(APIModel):
    request_id: str


class VideoResponse(APIModel):
    status: str
