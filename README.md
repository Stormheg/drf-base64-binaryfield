# drf-base64-binaryfield

[![PyPI](https://img.shields.io/pypi/v/ kiecutter.project_name }}.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/drf-base64-binaryfield.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/drf-base64-binaryfield)][pypi status]
[![License](https://img.shields.io/pypi/l/drf-base64-binaryfield)][license]

[![Tests](https://github.com/Stormbase/drf-base64-binaryfield/actions/workflows/tests.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Stormbase/drf-base64-binaryfield/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/drf-base64-binaryfield/
[tests]: https://github.com/Stormbase/drf-base64-binaryfield/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Stormbase/drf-base64-binaryfield
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

This package provides a `Base64BinaryField` for use with Django REST Framework serializers.

It allows you to:

- Serialize binary data into base64 strings for use in JSON responses
- Deserialize base64 strings back into binary data
- Optionally use url-safe base64 encoding (replacing `+` and `/` with `-` and `_`)
- Validate the length of the binary data

**Why?** because JSON does not support binary data, and base64 is a common way to represent binary data in JSON.

## Considerations

Base64 encoding isn't very space efficient.

If you need to send a lot of binary data quite often, you may want to consider using a more efficient serialization format instead of JSON, such as [MessagePack](https://msgpack.org/). There is a MessagePack serializer for Django REST Framework available: [django-rest-framework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack).

If you only occasionally need to send binary data then base64 encoding is probably fine for your use case. This package may be suitable for you.

## Requirements

- Python 3.9+
- Django 3.2+
- Django REST Framework 3.14+

## Installation

You can install _drf-base64-binaryfield_ via [pip] from [PyPI]:

```console
$ pip install drf-base64-binaryfield
```

## Usage

In this example, we need to send a cryptographic challenge to the client that consists of raw bytes.
Wouldn't it be convenient if there was a way to send this data as part of JSON response?

We can use `Base64BinaryField` provided by this package to serialize the binary data into a base64 string, which can be sent as part of a JSON response.

```python
from rest_framework import serializers
from drf_base64_binaryfield.fields import Base64BinaryField

class ChallengerSerializer(serializers.Serializer):
    # This field accepts a Python bytes object and serializes it into a base64 string. Or it can deserialize a base64 string back into a bytes object.
    challenge = Base64BinaryField()

serializer = ChallengerSerializer(instance={'challenge': b'\x00\x01\x02\x03'})
print(serializer.data)
# {'challenge': 'AAECAw=='}
```

### Web-safe encoding

If you want to use web-safe base64 encoding, you can set `url_safe=True`:

```python

class CryptographicChallengeSerializer(serializers.Serializer):
    challenge = Base64BinaryField(url_safe=True)
```

### Binary data size validation

This package also supports validating the size of the decoded binary data:

```python
class ExampleSerializer(serializers.Serializer):
    # This field will only accept binary data that is between 16 and 32 bytes long
    example_binary = Base64BinaryField(min_size=16, max_size=32)
```

### Extending `Base64BinaryField`

You can extend `Base64BinaryField` to create your own custom fields. You may want to unpack the binary data into a different format, for example.

```python
import struct

class CustomBinaryField(Base64BinaryField):
    def to_internal_value(self, data):
        binary_data = super().to_internal_value(data)

        # Do something with the binary data...

        # For example: unpack it as a little-endian, 32-bit unsigned integer
        return struct.unpack('<I', binary_data)[0]
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_drf-base64-binaryfield_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@OmenApps]'s [Cookiecutter Django Package] template.

[@omenapps]: https://github.com/OmenApps
[pypi]: https://pypi.org/
[cookiecutter django package]: https://github.com/OmenApps/cookiecutter-django-package
[file an issue]: https://github.com/Stormbase/drf-base64-binaryfield/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/Stormbase/drf-base64-binaryfield/blob/main/LICENSE
[contributor guide]: https://github.com/Stormbase/drf-base64-binaryfield/blob/main/CONTRIBUTING.md
