import json
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to manage correctly some specific types.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%d/%m/%Y %H:%M:%S")
        return super().default(obj)
