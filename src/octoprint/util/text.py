__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2020 The OctoPrint Project - Released under terms of the AGPLv3 License"

import re

from emoji import demojize

from octoprint.util import to_unicode
from octoprint.vendor.awesome_slugify import Slugify

_UNICODE_VARIATIONS = re.compile("[\uFE00-\uFE0F]", re.U)
_SLUGIFIES = {}


def sanitize(text, safe_chars="-_.", demoji=True):
    """
    Sanitizes text by running it through slugify and optionally emoji translating.

    Examples:

    >>> sanitize("Hello World!") # doctest: +ALLOW_UNICODE
    'Hello-World'
    >>> sanitize("Hello World!", safe_chars="-_. ") # doctest: +ALLOW_UNICODE
    'Hello World'
    >>> sanitize("\u2764") # doctest: +ALLOW_UNICODE
    'red_heart'
    >>> sanitize("\u2764\ufe00") # doctest: +ALLOW_UNICODE
    'red_heart'
    >>> sanitize("\u2764", demoji=False) # doctest: +ALLOW_UNICODE
    ''

    Args:
        text: the text to sanitize
        safe_chars: characters to consider safe and to keep after sanitization
        emoji: whether to also convert emoji to text

    Returns: the sanitized text
    """
    slugify = _SLUGIFIES.get(safe_chars)
    if slugify is None:
        slugify = Slugify()
        slugify.safe_chars = safe_chars
        _SLUGIFIES[safe_chars] = slugify

    text = to_unicode(text)
    if demoji:
        text = remove_unicode_variations(text)
        text = demojize(text, delimiters=("", ""))
    return slugify(text)


def remove_unicode_variations(text):
    return _UNICODE_VARIATIONS.sub("", text)
