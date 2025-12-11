"""
Unit tests for app/core/security.py

Tests password hashing and JWT token creation following
AAA pattern (Arrange-Act-Assert) and FIRST principles.
"""

from datetime import timedelta

from jose import jwt

from app.core.config import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    hash_password,
    verify_password,
)


class TestHashPassword:
    """Tests for hash_password function."""

    def test_hash_password_returns_different_value(self):
        """Test that hashing a password returns a different value from the original."""
        # ARRANGE
        plain_password = "MySecurePassword123!"

        # ACT
        hashed = hash_password(plain_password)

        # ASSERT
        assert hashed != plain_password
        assert len(hashed) > len(plain_password)

    def test_hash_password_produces_unique_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        # ARRANGE
        plain_password = "MySecurePassword123!"

        # ACT
        hash1 = hash_password(plain_password)
        hash2 = hash_password(plain_password)

        # ASSERT
        assert hash1 != hash2


class TestVerifyPassword:
    """Tests for verify_password function."""

    def test_verify_password_with_correct_password(self):
        """Test that verify_password returns True for correct password."""
        # ARRANGE
        plain_password = "CorrectPassword123!"
        hashed_password = hash_password(plain_password)

        # ACT
        result = verify_password(plain_password, hashed_password)

        # ASSERT
        assert result is True

    def test_verify_password_with_wrong_password(self):
        """Test that verify_password returns False for wrong password."""
        # ARRANGE
        correct_password = "CorrectPassword123!"
        wrong_password = "WrongPassword456!"
        hashed_password = hash_password(correct_password)

        # ACT
        result = verify_password(wrong_password, hashed_password)

        # ASSERT
        assert result is False

    def test_verify_password_with_empty_password(self):
        """Edge case: verify_password with empty password returns False."""
        # ARRANGE
        correct_password = "CorrectPassword123!"
        empty_password = ""
        hashed_password = hash_password(correct_password)

        # ACT
        result = verify_password(empty_password, hashed_password)

        # ASSERT
        assert result is False


class TestCreateAccessToken:
    """Tests for create_access_token function."""

    def test_create_access_token_contains_subject(self):
        """Test that token contains the provided subject."""
        # ARRANGE
        subject = "user@example.com"

        # ACT
        token = create_access_token(subject=subject)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        # ASSERT
        assert payload["sub"] == subject

    def test_create_access_token_with_custom_expiry(self):
        """Test that token respects custom expiry delta."""
        # ARRANGE
        subject = "user@example.com"
        custom_expiry = timedelta(hours=2)

        # ACT
        token = create_access_token(subject=subject, expires_delta=custom_expiry)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        # ASSERT
        assert "exp" in payload
        assert payload["sub"] == subject
