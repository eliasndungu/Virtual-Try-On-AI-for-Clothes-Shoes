"""Utility functions."""

import secrets
import string
from typing import Optional


def generate_api_key(length: int = 32) -> str:
    """Generate a random API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_filename(prefix: str = "", extension: str = "jpg") -> str:
    """Generate a unique filename."""
    random_string = secrets.token_hex(16)
    if prefix:
        return f"{prefix}_{random_string}.{extension}"
    return f"{random_string}.{extension}"
