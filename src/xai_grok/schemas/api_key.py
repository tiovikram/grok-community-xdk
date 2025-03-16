import datetime
import typing

import pydantic


class APIKey(pydantic.BaseModel):
    acls: typing.List[str]
    api_key_blocked: bool
    api_key_disabled: bool
    api_key_id: str
    create_time: datetime.datetime
    modified_by: str
    modify_time: typing.Union[datetime.datetime, typing.Literal[""]]
    name: str
    redacted_api_key: str
    team_id: str
    team_blocked: bool
    user_id: str
