"""Password strength analyzer with entropy calculation."""

import math
from dataclasses import dataclass
from src.config import (
    LOWERCASE, UPPERCASE, DIGITS, SYMBOLS,
    ENTROPY_WEAK, ENTROPY_FAIR, ENTROPY_STRONG, ENTROPY_VERY_STRONG,
)


@dataclass
class PasswordAnalysis:
    password: str
    entropy: float
    strength_label: str
    strength_bar: str
    strength_color: str
    charset_size: int
    length: int
    has_upper: bool
    has_lower: bool
    has_digits: bool
    has_symbols: bool


class PasswordAnalyzer:
    """Analyzes password strength using entropy and character composition."""

    def _calculate_charset_size(self, password: str) -> int:
        size = 0
        if any(c in LOWERCASE for c in password):
            size += len(LOWERCASE)
        if any(c in UPPERCASE for c in password):
            size += len(UPPERCASE)
        if any(c in DIGITS for c in password):
            size += len(DIGITS)
        if any(c in SYMBOLS for c in password):
            size += len(SYMBOLS)
        return size

    def _calculate_entropy(self, password: str, charset_size: int) -> float:
        if charset_size == 0 or len(password) == 0:
            return 0.0
        return len(password) * math.log2(charset_size)

    def _get_strength(self, entropy: float) -> tuple[str, str, str]:
        if entropy < ENTROPY_WEAK:
            return "WEAK", "███░░░░░░░░░", "red"
        elif entropy < ENTROPY_FAIR:
            return "FAIR", "█████░░░░░░░", "yellow"
        elif entropy < ENTROPY_STRONG:
            return "STRONG", "████████░░░░", "green"
        elif entropy < ENTROPY_VERY_STRONG:
            return "VERY STRONG", "██████████░░", "bright_green"
        else:
            return "MAXIMUM", "████████████", "cyan"

    def analyze(self, password: str) -> PasswordAnalysis:
        charset_size = self._calculate_charset_size(password)
        entropy = self._calculate_entropy(password, charset_size)
        label, bar, color = self._get_strength(entropy)
        return PasswordAnalysis(
            password=password,
            entropy=round(entropy, 1),
            strength_label=label,
            strength_bar=bar,
            strength_color=color,
            charset_size=charset_size,
            length=len(password),
            has_upper=any(c in UPPERCASE for c in password),
            has_lower=any(c in LOWERCASE for c in password),
            has_digits=any(c in DIGITS for c in password),
            has_symbols=any(c in SYMBOLS for c in password),
        )
