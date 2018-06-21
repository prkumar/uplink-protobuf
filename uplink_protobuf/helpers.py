# Standard library imports
import inspect

# Third party imports
from google.protobuf import message, json_format


def is_protocol_buffer_class(cls):
    return inspect.isclass(cls) and issubclass(cls, message.Message)


def get_first_of_type(iterable, type_):
    return next(i for i in iterable if isinstance(i, type_))


def has_value_of_type(iterable, type_):
    return any(isinstance(i, type_) for i in iterable)


def create_json_serializer(**other):
    def converter(msg):
        return json_format.MessageToDict(msg, **other)

    return converter


def create_json_deserializer(cls, **other):
    def converter(response):
        msg = cls()
        return json_format.ParseDict(response, msg, **other)

    return converter
