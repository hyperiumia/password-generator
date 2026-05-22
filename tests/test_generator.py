"""Tests for password generator module."""

import pytest
from src.generator import PasswordGenerator


class TestPasswordGenerator:

    def test_default_generation(self):
        gen = PasswordGenerator()
        pwd = gen.generate()
        assert len(pwd) == 16

    def test_custom_length(self):
        gen = PasswordGenerator(length=32)
        pwd = gen.generate()
        assert len(pwd) == 32

    def test_minimum_length(self):
        gen = PasswordGenerator(length=4)
        pwd = gen.generate()
        assert len(pwd) == 4

    def test_invalid_length_raises(self):
        with pytest.raises(ValueError):
            PasswordGenerator(length=1)

    def test_max_length_raises(self):
        with pytest.raises(ValueError, match="between"):
            PasswordGenerator(length=200)

    def test_no_character_type_raises(self):
        with pytest.raises(ValueError, match="At least one"):
            gen = PasswordGenerator(use_upper=False, use_lower=False, use_digits=False, use_symbols=False)
            gen.generate()

    def test_only_lowercase(self):
        gen = PasswordGenerator(use_upper=False, use_digits=False, use_symbols=False)
        pwd = gen.generate()
        assert pwd.islower()

    def test_multiple_passwords_are_unique(self):
        gen = PasswordGenerator(length=32)
        passwords = gen.generate_multiple(10)
        assert len(set(passwords)) == 10

    def test_pronounceable_mode(self):
        gen = PasswordGenerator(pronounceable=True, length=20)
        pwd = gen.generate()
        assert len(pwd) == 20

    def test_count_parameter(self):
        gen = PasswordGenerator()
        passwords = gen.generate_multiple(5)
        assert len(passwords) == 5

    def test_invalid_count_raises(self):
        gen = PasswordGenerator()
        with pytest.raises(ValueError):
            gen.generate_multiple(0)
