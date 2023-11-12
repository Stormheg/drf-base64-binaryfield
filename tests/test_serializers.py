"""Integration tests when the fields are used with a serializer."""
import pytest
from rest_framework import serializers

from drf_base64_binaryfield.fields import Base64BinaryField


class ExampleBinarySerializer(serializers.Serializer):
    """Example serializer that uses the Base64BinaryField."""

    binary = Base64BinaryField()


@pytest.mark.parametrize(
    "input, expected",
    [
        (b"hello", "aGVsbG8="),
        (b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP", "PACRV1bz4tuzvD/XijtuUA=="),
        (b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5=", "Rv3zUQznxPdQuME/ZU6lPQ=="),
    ],
)
def test_serialize_base64(input, expected):
    """Check that the serializer converts binary to base64 correctly."""
    ser = ExampleBinarySerializer(instance={"binary": input})
    assert ser.data["binary"] == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("aGVsbG8=", b"hello"),
        ("PACRV1bz4tuzvD/XijtuUA==", b"<\x00\x91WV\xf3\xe2\xdb\xb3\xbc?\xd7\x8a;nP"),
        ("Rv3zUQznxPdQuME/ZU6lPQ==", b"F\xfd\xf3Q\x0c\xe7\xc4\xf7P\xb8\xc1?eN\xa5="),
    ],
)
def test_deserialize_base64(input, expected):
    """Check that the serializer converts base64 to binary correctly."""
    ser = ExampleBinarySerializer(data={"binary": input})
    assert ser.is_valid()
    assert ser.validated_data["binary"] == expected
