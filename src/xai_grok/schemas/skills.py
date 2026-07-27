import typing

from xai_grok.schemas.api_model import APIModel


class Skill(APIModel):
    id: str
    created_at: int
    default_version: typing.Any
    description: str
    latest_version: typing.Any
    name: str
    object: str


class SkillList(APIModel):
    data: typing.List[Skill]
    first_id: typing.Optional[str]
    has_more: bool
    last_id: typing.Optional[str]
    object: str


class DeletedSkill(APIModel):
    id: str
    deleted: bool
    object: str
