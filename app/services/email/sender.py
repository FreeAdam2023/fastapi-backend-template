"""
Email template rendering and multi-language email sending.

Author: Adam Lyu
Date: 2025-04-05
"""

import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.services.email.client import mailer
from app.core.i18n import get_translator

# Load email template path
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")

template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH),
    autoescape=select_autoescape(["html", "xml"])
)


def render_template_with_fallback(name: str, lang: str, context: dict) -> str:
    """
    Render an email template with language fallback.

    Priority: name_{lang}.html -> name_en.html

    :param name: template name prefix
    :param lang: preferred language code (e.g., 'en', 'fr')
    :param context: template context variables
    :return: rendered HTML string
    :raises RuntimeError: if no valid template is found
    """
    for try_lang in [lang, "en"]:
        try:
            template_file = f"{name}_{try_lang}.html"
            template = template_env.get_template(template_file)
            return template.render(**context)
        except Exception as e:
            continue
    raise RuntimeError(f"Failed to load template: {name} (lang: {lang})")


async def send_verification_email(to_email: str, verify_url: str, lang: str = "en"):
    """
    Send email verification link.

    :param to_email: recipient email address
    :param verify_url: verification URL
    :param lang: preferred language
    """
    _ = get_translator(lang).gettext

    subject = _("Please verify your email")
    text_content = _("Click the link below to verify your email:\n{url}").format(url=verify_url)
    html_content = render_template_with_fallback("verify_email", lang, {"verify_url": verify_url})

    await mailer.send(to_email, subject, text_content, html=html_content)


async def send_welcome_email(to_email: str, username: str, lang: str = "en"):
    """
    Send welcome email after registration.

    :param to_email: recipient email address
    :param username: recipient's username
    :param lang: preferred language
    """
    _ = get_translator(lang).gettext

    subject = _("Welcome to Versegates!")
    text_content = _("Hello {username}, welcome to Versegates!").format(username=username)
    html_content = render_template_with_fallback("welcome", lang, {"username": username})

    await mailer.send(to_email, subject, text_content, html=html_content)
