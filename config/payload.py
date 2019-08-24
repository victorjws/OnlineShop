import json
from datetime import datetime

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler


def custom_jwt_payload_handler(user):
    payload = jwt_payload_handler(user)
    payload['nickname'] = user.nickname
    payload['expiration'] = (datetime.utcnow() + (api_settings.JWT_EXPIRATION_DELTA / 2)).timestamp()
    return payload
