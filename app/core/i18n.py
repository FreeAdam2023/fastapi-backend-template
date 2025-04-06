"""
i18n (internationalization) utility for language detection and translation.

Supports:
- Language detection from request
- Context-local gettext resolution
- FastAPI middleware integration

Author: Adam Lyu
Date: 2025-04-05
"""

import gettext
import contextvars
from fastapi import Request

# Supported languages
SUPPORTED_LANGUAGES = ["en", "zh"]

# Context variable for request-local language
_lang_ctx = contextvars.ContextVar("lang", default="en")


def set_request_lang(lang: str):
    lang = lang if lang in SUPPORTED_LANGUAGES else "en"
    _lang_ctx.set(lang)


def get_request_lang() -> str:
    return _lang_ctx.get()


def get_translator(locale: str):
    return gettext.translation(
        domain="messages",
        localedir="app/i18n",
        languages=[locale],
        fallback=True,
    )


def get_locale_gettext():
    lang = get_request_lang()
    return get_translator(lang).gettext
