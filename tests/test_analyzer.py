"""Tests for password analyzer module."""

import pytest
from src.analyzer import PasswordAnalyzer


class TestPasswordAnalyzer:

    def setup_method(self):
        self.analyzer = PasswordAnalyzer()

    def test_weak_password(self):
        result = self.analyzer.analyze("abc")
        assert result.strength_label == "WEAK"

    def test_strong_password(self):
        result = self.analyzer.analyze("k#M9$vRp2&xL7!nQ4@wZ")
        assert result.strength_label in ("STRONG", "VERY STRONG", "MAXIMUM")

    def test_entropy_calculation(self):
        result = self.analyzer.analyze("abcdefgh")
        assert result.entropy > 35
        assert result.entropy < 40

    def test_charset_detection(self):
        result = self.analyzer.analyze("Abc123!@#")
        assert result.has_upper is True
        assert result.has_lower is True
        assert result.has_digits is True
        assert result.has_symbols is True

    def test_no_upper(self):
        result = self.analyzer.analyze("abc123!@#")
        assert result.has_upper is False

    def test_length_recorded(self):
        result = self.analyzer.analyze("test1234")
        assert result.length == 8

    def test_empty_password(self):
        result = self.analyzer.analyze("")
        assert result.entropy == 0.0
        assert result.strength_label == "WEAK"
