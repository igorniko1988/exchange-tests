import json

SENSITIVE_KEYS = {"password", "access_token", "refresh_token"}
SENSITIVE_HEADERS = {"authorization"}
MASK = "***"


def mask_body(raw) -> str:
    if raw is None:
        return ""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="replace")
    try:
        data = json.loads(raw)
    except ValueError:
        return raw
    return json.dumps(_mask(data), indent=2, ensure_ascii=False)


def _mask(value):
    if isinstance(value, dict):
        return {k: MASK if k in SENSITIVE_KEYS else _mask(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_mask(v) for v in value]
    return value


def mask_headers(headers) -> str:
    return "\n".join(
        f"{k}: {MASK if k.lower() in SENSITIVE_HEADERS else v}" for k, v in headers.items()
    )
