import typing

from xai_grok.schemas.api_model import APIModel


class File(APIModel):
    bytes: int
    created_at: int
    filename: str
    id: str
    object: str


class ListFilesResponse(APIModel):
    data: typing.List[File]


class DeleteFileResponse(APIModel):
    id: str
    deleted: bool
    object: str


class CreatePublicUrlRequest(APIModel):
    expires_after: typing.Optional[int] = None


class CreatePublicUrlResponse(APIModel):
    public_url: str


class RevokePublicUrlResponse(APIModel):
    id: str
    revoked: bool
