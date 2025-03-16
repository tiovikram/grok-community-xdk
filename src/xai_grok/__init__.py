import os

import requests

from xai_grok.grok import Grok as GrokClient
import xai_grok.providers as providers


def Grok(api_key: str = ""):
    user_api_key = api_key if api_key else os.environ["XAI_API_KEY"]
    return GrokClient(user_api_key, requests, providers.UnauthorizedUserErrorProvider())
