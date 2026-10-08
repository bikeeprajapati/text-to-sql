from datetime import datetime, timezone


def utc_now() -> datetime:
    """Current UTC time as a naive datetime, matching our TIMESTAMP WITHOUT TIME ZONE columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)