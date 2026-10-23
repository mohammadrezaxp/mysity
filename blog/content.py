"""Safe rich text for both existing database content and new editor/API input."""

import bleach
from bleach.css_sanitizer import CSSSanitizer

TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "p",
    "br",
    "div",
    "span",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "img",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
    "hr",
    "pre",
    "blockquote",
    "s",
    "u",
    "sub",
    "sup",
}
ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title", "width", "height"],
    "*": ["style"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan"],
}
CSS = CSSSanitizer(
    allowed_css_properties=[
        "color",
        "background-color",
        "text-align",
        "font-size",
        "font-weight",
        "font-style",
        "text-decoration",
        "white-space",
    ]
)


def clean_html(value):
    return bleach.clean(
        value or "",
        tags=TAGS,
        attributes=ATTRIBUTES,
        protocols=["http", "https", "mailto"],
        css_sanitizer=CSS,
        strip=True,
    )
