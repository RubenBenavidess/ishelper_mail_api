from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    headers_enabled=True,
    strategy="fixed-window",
    storage_uri="memory://",
    auto_check=True,
    swallow_errors=False
)

