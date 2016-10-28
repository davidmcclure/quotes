

import re


def clean_text(text: str) -> str:

    """
    Clean a raw text string.
    """

    return re.sub('\s{2,}|\n', ' ', text.strip())
