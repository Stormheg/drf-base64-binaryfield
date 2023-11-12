from rest_framework import serializers

from drf_base64_binaryfield.fields import Base64BinaryField

from .models import Blob


class ExampleBinarySerializer(serializers.ModelSerializer):
    """Example serializer that uses the Base64BinaryField."""

    blob = Base64BinaryField(url_safe=False, min_size=8, max_size=32, allow_null=True)

    class Meta:
        model = Blob
        fields = "__all__"


class ExampleURLSafeBinarySerializer(ExampleBinarySerializer):
    """Example serializer that uses the Base64BinaryField with web-safe encoding enabled."""

    blob = Base64BinaryField(url_safe=True, min_size=8, max_size=32, allow_null=True)
