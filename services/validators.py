import re


def is_valid_xj_id(value: str) -> bool:
    return bool(re.fullmatch(r"\d{7}", value.strip()))


def normalize_phone(value: str) -> str:
    return value.strip()

