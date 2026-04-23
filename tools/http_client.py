from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


def _retry_decorator(attempts: int):
    return retry(
        reraise=True,
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError, ValueError)),
    )


def fetch_json(
    url: str,
    params: dict[str, Any] | None = None,
    timeout_seconds: int = 12,
    retry_attempts: int = 3,
) -> Any:
    """Fetch and parse JSON with timeout and retry protection."""
    @_retry_decorator(retry_attempts)
    def _run() -> Any:
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    return _run()
