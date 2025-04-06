"""
Language detection middleware for FastAPI.

Sets request.state.lang and request.state._ (gettext),
and syncs language to contextvars for global i18n support.

Author: Adam Lyu
Date: 2025-04-05
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.i18n import get_translator, set_request_lang

DEFAULT_LANG = "en"
SUPPORTED_LANGUAGES = {"en", "zh", "ja", "ko", "fr", "de", "es", "ru", "it", "pt", "tr"}


class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Detect language from Accept-Language
        lang = request.headers.get("accept-language", DEFAULT_LANG).split(",")[0].lower()
        lang = lang.split("-")[0]  # e.g., zh-CN → zh

        if lang not in SUPPORTED_LANGUAGES:
            lang = DEFAULT_LANG

        # Inject to request.state
        request.state.lang = lang
        request.state._ = get_translator(lang).gettext

        # Set to contextvar for global access (e.g. in exceptions)
        set_request_lang(lang)

        response = await call_next(request)
        return response
