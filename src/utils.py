import datetime

def get_timestamp():
    """Returns the current time in ISO 8601 format."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()