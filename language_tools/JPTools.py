import re


class JPTools:
    """
    Some basic tools to work with different formats for romanised Japanese text.
    Assumes using Modified Hepburn. Traditional Hepburn (n & m for ん) not supported.
    """
    trans_from = str.maketrans(
        {
            "ā": "aa",
            "ī": "ii",
            "ū": "uu",
            "ē": "ee",
            "ō": "oo",
            "Ā": "Aa",
            "Ī": "Ii",
            "Ū": "Uu",
            "Ē": "Ei",
            "Ō": "Ou",
        }
    )
    trans_to = str.maketrans({v: k for k, v in trans_from.items()})

    @classmethod
    def remove_macrons(cls, text) -> str:
        """
        Converts romanised Japanese text from using macrons to using vowel pairs.
        EG: ā -> aa
        """
        # Use the translate method to replace characters
        translated_text = text.translate(cls.trans_from)
        return translated_text

    @classmethod
    def add_macrons(cls, text) -> str:
        """
        Converts romanised Japanese text from using vowel pairs to macrons.
        EG: aa -> ā
        """
        # Use the translate method to replace characters
        translated_text = text.translate(cls.trans_to)
        return translated_text

    @staticmethod
    def is_macronised(text) -> bool:
        """
        Checks if a given piece of romanised Japanese text is using macrons.
        """
        p = re.compile(r"[āīūēō]", re.IGNORECASE)
        return re.search(p, text)