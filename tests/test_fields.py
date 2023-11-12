"""Tests for the fields module."""
import pytest
from rest_framework.exceptions import ValidationError

from drf_base64_binaryfield.fields import Base64BinaryField


@pytest.mark.parametrize(
    "input, url_safe, expected_output",
    [
        ("aGVsbG8=", True, b"hello"),
        ("PACRV1bz4tuzvD/XijtuUA==", True, b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP"),
        ("Rv3zUQznxPdQuME/ZU6lPQ==", True, b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5="),
        ("aGVsbG8=", False, b"hello"),
        ("PACRV1bz4tuzvD/XijtuUA==", False, b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP"),
        ("Rv3zUQznxPdQuME/ZU6lPQ==", False, b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5="),
        ("FFy/3kt/WZoarO39+Y6lAA==", False, b"\x14\\\xbf\xdeK\x7fY\x9a\x1a\xac\xed\xfd\xf9\x8e\xa5\x00"),
        ("FFy_3kt_WZoarO39-Y6lAA==", True, b"\x14\\\xbf\xdeK\x7fY\x9a\x1a\xac\xed\xfd\xf9\x8e\xa5\x00"),
    ],
)
def test_base64_binary_field_to_internal_value_happy(input, url_safe, expected_output):
    """Check that the field converts base64 to binary correctly, with support for web-safe decoding."""
    field = Base64BinaryField(url_safe=url_safe)
    assert field.to_internal_value(input) == expected_output


@pytest.mark.parametrize(
    "input",
    ["#(*@)", "aGVsbG8", "asd/sd/", "123098"],
)
@pytest.mark.parametrize("url_safe", [True, False])
def test_base64_binary_field_to_internal_value_invalid(input, url_safe):
    """Check that the field raises a ValidationError when the input is invalid base64."""
    field = Base64BinaryField(url_safe=url_safe)
    with pytest.raises(ValidationError) as exc_info:
        field.to_internal_value(input)
    assert exc_info.value.detail[0].code == "invalid_format"


@pytest.mark.parametrize(
    "input, url_safe, expected_output",
    [
        (b"hello", False, "aGVsbG8="),
        (b"hello", True, "aGVsbG8="),
        (b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP", False, "PACRV1bz4tuzvD/XijtuUA=="),
        (b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP", True, "PACRV1bz4tuzvD_XijtuUA=="),
        (b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5=", False, "Rv3zUQznxPdQuME/ZU6lPQ=="),
        (b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5=", True, "Rv3zUQznxPdQuME_ZU6lPQ=="),
        (b"\x14\\\xbf\xdeK\x7fY\x9a\x1a\xac\xed\xfd\xf9\x8e\xa5\x00", False, "FFy/3kt/WZoarO39+Y6lAA=="),
        (b"\x14\\\xbf\xdeK\x7fY\x9a\x1a\xac\xed\xfd\xf9\x8e\xa5\x00", True, "FFy_3kt_WZoarO39-Y6lAA=="),
    ],
)
def test_base64_binary_field_to_representation_happy(input, url_safe, expected_output):
    """Check that the field converts binary to base64 correctly, with support for web-safe encoding."""
    field = Base64BinaryField(url_safe=url_safe)
    assert field.to_representation(input) == expected_output


def test_base64_binary_field_to_representation_invalid():
    """Check that the field raises a ValidationError when the input is not binary."""
    field = Base64BinaryField()
    with pytest.raises(ValidationError) as exc_info:
        field.to_representation(1)
    assert exc_info.value.detail[0].code == "invalid_type"


@pytest.mark.parametrize(
    "url_safe",
    [True, False],
)
def test_fields_invalid_type(url_safe):
    """Check that the field raises a ValidationError when the input is not a string."""
    field = Base64BinaryField(url_safe=url_safe)
    with pytest.raises(ValidationError) as exc_info:
        field.to_internal_value(1)
    assert exc_info.value.detail[0].code == "invalid_type"


@pytest.mark.parametrize("input", ["😀", "¯\\_(ツ)_//¯", "(＾▽＾)", "◼︎", "№", "☾", "″", "⟹"])
def test_fields_non_ascii_chars(input):
    """Check that the field raises a ValidationError when the input contains non-ascii characters."""
    field = Base64BinaryField()
    with pytest.raises(ValidationError) as exc_info:
        field.to_internal_value(input)
    assert exc_info.value.detail[0].code == "invalid_characters"


@pytest.mark.parametrize(
    "input, max_size, should_raise",
    [
        ("aGVsbG8=", 10, False),
        ("PACRV1bz4tuzvD/XijtuUA==", 10, True),
    ],
)
def test_fields_respect_max_size(input, max_size, should_raise):
    """Check that the field respects max_size validators."""
    field = Base64BinaryField(max_size=max_size)

    if should_raise:
        with pytest.raises(ValidationError):
            field.run_validators(input)
    else:
        field.run_validators(input)


@pytest.mark.parametrize(
    "input, min_size, should_raise",
    [
        ("aGVsbG8=", 10, True),
        ("PACRV1bz4tuzvD/XijtuUA==", 10, False),
        ("Rv3zUQznxPdQuME/ZU6lPQ==", 10, False),
    ],
)
def test_fields_respect_min_size(input, min_size, should_raise):
    """Check that the field respects min_size validators."""
    # Check that the field respects min_size.
    field = Base64BinaryField(min_size=min_size)

    if should_raise:
        with pytest.raises(ValidationError):
            field.run_validators(input)
    else:
        field.run_validators(input)
