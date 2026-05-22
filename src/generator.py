"""Cryptographic password generation engine using Python's secrets module."""

import secrets
from src.config import (
    LOWERCASE, UPPERCASE, DIGITS, SYMBOLS,
    CONSONANTS, VOWELS, MIN_LENGTH, MAX_LENGTH,
)


class PasswordGenerator:
    """Generates cryptographically secure passwords."""

    def __init__(
        self,
        length: int = 16,
        use_upper: bool = True,
        use_lower: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        pronounceable: bool = False,
    ):
        if length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}")
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.pronounceable = pronounceable

    def _build_charset(self) -> str:
        charset = ""
        if self.use_lower:
            charset += LOWERCASE
        if self.use_upper:
            charset += UPPERCASE
        if self.use_digits:
            charset += DIGITS
        if self.use_symbols:
            charset += SYMBOLS
        if not charset:
            raise ValueError("At least one character type must be enabled")
        return charset

    def _generate_standard(self) -> str:
        charset = self._build_charset()
        return "".join(secrets.choice(charset) for _ in range(self.length))

    def _generate_pronounceable(self) -> str:
        pairs_needed = self.length // 2
        extra = self.length % 2
        parts = []
        for _ in range(pairs_needed):
            consonant = secrets.choice(CONSONANTS)
            vowel = secrets.choice(VOWELS)
            if self.use_upper and secrets.randbelow(2):
                consonant = consonant.upper()
                vowel = vowel.upper()
            parts.append(consonant)
            parts.append(vowel)
        if extra:
            if self.use_digits and secrets.randbelow(2):
                parts.append(secrets.choice(DIGITS))
            elif self.use_symbols and secrets.randbelow(2):
                parts.append(secrets.choice(SYMBOLS))
            else:
                parts.append(secrets.choice(CONSONANTS + VOWELS))
        password = "".join(parts)
        password_list = list(password)
        if self.use_digits and not any(c in DIGITS for c in password_list):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(DIGITS)
        if self.use_symbols and not any(c in SYMBOLS for c in password_list):
            pos = secrets.randbelow(len(password_list))
            password_list[pos] = secrets.choice(SYMBOLS)
        return "".join(password_list)

    def generate(self) -> str:
        if self.pronounceable:
            return self._generate_pronounceable()
        return self._generate_standard()

    def generate_multiple(self, count: int = 1) -> list[str]:
        if count < 1:
            raise ValueError("Count must be at least 1")
        return [self.generate() for _ in range(count)]
