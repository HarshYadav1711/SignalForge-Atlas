from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from configs.settings import AppSettings

VALID_DECISIONS = {"STRONG_BUY", "WEAK_BUY", "SKIP"}


def _build_prompt(direction: str, probability: float) -> str:
    return (
        "You are a strict classifier.\n"
        "Input:\n"
        "{\n"
        f'  "direction": "{direction}",\n'
        f'  "probability": {probability}\n'
        "}\n"
        "Output rules:\n"
        "- Return ONLY one token: STRONG_BUY or WEAK_BUY or SKIP\n"
        "- No punctuation\n"
        "- No explanation\n"
        "- No extra text"
    )


def _is_free_model(model_name: str) -> bool:
    return model_name.strip().endswith(":free")


def _request_reasoning(settings: AppSettings, direction: str, probability: float) -> str:
    @retry(
        reraise=True,
        stop=stop_after_attempt(settings.request_retry_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError, ValueError)),
    )
    def _run() -> str:
        if not settings.openrouter_api_key:
            raise ValueError("Missing OpenRouter API key")
        if not _is_free_model(settings.openrouter_model):
            raise ValueError("OpenRouter model must be free-tier")

        payload = {
            "model": settings.openrouter_model,
            "messages": [{"role": "user", "content": _build_prompt(direction, probability)}],
            "temperature": 0,
            "max_tokens": 4,
        }
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        with httpx.Client(timeout=settings.request_timeout_seconds) as client:
            response = client.post(f"{settings.openrouter_base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
            .upper()
        )
        token = content.split()[0] if content else ""
        if token not in VALID_DECISIONS:
            raise ValueError("Model response not in allowed decisions")
        return token

    return _run()


def classify_signal(settings: AppSettings, direction: str, probability: float) -> str:
    safe_direction = "UP" if str(direction).upper() == "UP" else "DOWN"
    safe_probability = max(0.0, min(1.0, float(probability)))
    try:
        return _request_reasoning(settings, safe_direction, safe_probability)
    except Exception:
        return "SKIP"
