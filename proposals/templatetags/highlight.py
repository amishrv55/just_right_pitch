# proposals/templatetags/highlight.py
from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def highlight(text, search):
    """
    Highlights all case-insensitive matches of any search word in `text` with yellow background.
    Multiple words in `search` are supported.
    """
    if not search:
        return text

    # Split search query into individual words, remove empty ones
    search_terms = [re.escape(word) for word in search.strip().split() if word]
    if not search_terms:
        return text

    # Create a regex pattern matching any of the search words
    pattern = re.compile(r"(" + "|".join(search_terms) + r")", re.IGNORECASE)

    highlighted = pattern.sub(
        lambda m: f'<mark style="background-color: yellow;">{m.group(0)}</mark>',
        text
    )
    return mark_safe(highlighted)
