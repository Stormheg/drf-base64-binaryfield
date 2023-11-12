"""Tests for the validators module."""

import pytest
from rest_framework.exceptions import ValidationError

from drf_base64_binaryfield.validators import MaxSizeValidator
from drf_base64_binaryfield.validators import MinSizeValidator


@pytest.mark.parametrize(
    "value, min_size, is_valid",
    [
        ("a" * 10, 10, True),
        ("a" * 11, 10, True),
        ("a" * 9, 10, False),
    ],
)
def test_min_size_validator(value, min_size, is_valid):
    """Check that MinSizeValidator works like expected."""
    validator = MinSizeValidator(min_size=min_size)
    if is_valid:
        validator(value)
    else:
        with pytest.raises(ValidationError):
            validator(value)


def test_min_size_validator_custom_message():
    """Check that MinSizeValidator uses a custom message when provided."""
    validator = MinSizeValidator(min_size=10, message="Custom message")
    with pytest.raises(ValidationError) as exc_info:
        validator("a" * 9)
    assert exc_info.value.detail[0].code == "min_size"
    assert exc_info.value.detail == ["Custom message"]


def test_min_size_validator_message():
    """Check that MinSizeValidator uses a default message when not provided."""
    validator = MinSizeValidator(min_size=10)
    with pytest.raises(ValidationError) as exc_info:
        validator("a" * 9)
    assert exc_info.value.detail == ["Ensure the binary encoded in this field is at least 10 bytes. It is 9 bytes."]


@pytest.mark.parametrize(
    "value, max_size, is_valid",
    [
        ("a" * 10, 10, True),
        ("a" * 9, 10, True),
        ("a" * 11, 10, False),
    ],
)
def test_max_size_validator(value, max_size, is_valid):
    """Check that MaxSizeValidator works like expected."""
    validator = MaxSizeValidator(max_size=max_size)
    if is_valid:
        validator(value)
    else:
        with pytest.raises(ValidationError):
            validator(value)


def test_max_size_validator_custom_message():
    """Check that MaxSizeValidator uses a custom message when provided."""
    validator = MaxSizeValidator(max_size=10, message="Custom message")
    with pytest.raises(ValidationError) as exc_info:
        validator("a" * 11)
    assert exc_info.value.detail[0].code == "max_size"
    assert exc_info.value.detail == ["Custom message"]


def test_max_size_validator_message():
    """Check that MaxSizeValidator uses a default message when not provided."""
    validator = MaxSizeValidator(max_size=10)
    with pytest.raises(ValidationError) as exc_info:
        validator("a" * 11)
    assert exc_info.value.detail == [
        "Ensure the binary encoded in this field is no larger than 10 bytes. It is 11 bytes."
    ]
