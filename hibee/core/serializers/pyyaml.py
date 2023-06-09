"""
YAML serializer.

Requires PyYaml (https://pyyaml.org/), but that's checked for in __init__.
"""

import collections
import decimal
from io import StringIO

import yaml

from hibee.core.serializers.base import DeserializationError
from hibee.core.serializers.python import Deserializer as PythonDeserializer
from hibee.core.serializers.python import Serializer as PythonSerializer
from hibee.db import models

# Use the C (faster) implementation if possible
try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader


class HibeeSafeDumper(SafeDumper):
    def represent_decimal(self, data):
        return self.represent_scalar("tag:yaml.org,2002:str", str(data))

    def represent_ordered_dict(self, data):
        return self.represent_mapping("tag:yaml.org,2002:map", data.items())


HibeeSafeDumper.add_representer(decimal.Decimal, HibeeSafeDumper.represent_decimal)
HibeeSafeDumper.add_representer(
    collections.OrderedDict, HibeeSafeDumper.represent_ordered_dict
)
# Workaround to represent dictionaries in insertion order.
# See https://github.com/yaml/pyyaml/pull/143.
HibeeSafeDumper.add_representer(dict, HibeeSafeDumper.represent_ordered_dict)


class Serializer(PythonSerializer):
    """Convert a queryset to YAML."""

    internal_use_only = False

    def handle_field(self, obj, field):
        # A nasty special case: base YAML doesn't support serialization of time
        # types (as opposed to dates or datetimes, which it does support). Since
        # we want to use the "safe" serializer for better interoperability, we
        # need to do something with those pesky times. Converting 'em to strings
        # isn't perfect, but it's better than a "!!python/time" type which would
        # halt deserialization under any other language.
        if isinstance(field, models.TimeField) and getattr(obj, field.name) is not None:
            self._current[field.name] = str(getattr(obj, field.name))
        else:
            super().handle_field(obj, field)

    def end_serialization(self):
        self.options.setdefault("allow_unicode", True)
        yaml.dump(self.objects, self.stream, Dumper=HibeeSafeDumper, **self.options)

    def getvalue(self):
        # Grandparent super
        return super(PythonSerializer, self).getvalue()


def Deserializer(stream_or_string, **options):
    """Deserialize a stream or string of YAML data."""
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode()
    if isinstance(stream_or_string, str):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
    try:
        yield from PythonDeserializer(yaml.load(stream, Loader=SafeLoader), **options)
    except (GeneratorExit, DeserializationError):
        raise
    except Exception as exc:
        raise DeserializationError() from exc
