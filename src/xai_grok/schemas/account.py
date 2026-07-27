from xai_grok.schemas.api_model import APIModel


class GetMeResponse(APIModel):
    user_id: str
    team_id: str
    zdr_status: str
    team_blocked: bool
