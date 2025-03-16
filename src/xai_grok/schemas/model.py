import datetime

import pydantic


class Model(pydantic.BaseModel):
    id: str
    created: datetime.datetime
    object: str
    owned_by: str
