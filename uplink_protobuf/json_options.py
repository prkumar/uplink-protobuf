# Third party imports
from google.protobuf import json_format
from uplink import decorators

# Local imports
from uplink_protobuf import helpers

__all__ = [
    "include_default_value_fields",
    "preserve_proto_field_names",
    "use_integers_for_enums",
    "ignore_unknown_fields"
]


class _DecodeOption(decorators.MethodAnnotation):
    @property
    def options(self):  # pragma: no cover
        raise NotImplementedError


class _EncodeOption(decorators.MethodAnnotation):
    @property
    def options(self):  # pragma: no cover
        raise NotImplementedError


# noinspection PyPep8Naming
class include_default_value_fields(_EncodeOption):
    """
    Indicates that the JSON output should include fields with their
    default values.

    By default, these fields are omitted if not set.
    """
    _can_be_static = True
    __options = {"including_default_value_fields": True}

    @property
    def options(self):
        return self.__options


# noinspection PyPep8Naming
class preserve_proto_field_names(_EncodeOption):
    """
    Indicates that the JSON output should use the proto field name as
    the JSON name.

    By default, the JSON printer converts the proto field names to
    lowerCamelCase and uses that as the JSON name.
    """
    _can_be_static = True
    __options = {"preserving_proto_field_name": True}

    @property
    def options(self):
        return self.__options


# noinspection PyPep8Naming
class use_integers_for_enums(_EncodeOption):
    """
    Indicates that the JSON output should use the numerical value of a
    proto enum value, instead of the name of the enum value.

    By default, the name of an enum value is used in the JSON
    output.
    """
    _can_be_static = True
    __options = {"use_integers_for_enums": True}

    @property
    def options(self):
        return self.__options


# noinspection PyPep8Naming
class ignore_unknown_fields(_DecodeOption):
    """
    Indicates that the JSON parser should ignore unknown fields in
    parsing.
    """
    _can_be_static = True
    __options = {"ignore_unknown_fields": True}

    @property
    def options(self):
        return self.__options


def parse_json(message_cls, request_definition, body):
    method_annotations = request_definition.method_annotations
    parsing_options = {}
    for opt in helpers.get_values_of_type(method_annotations, _DecodeOption):
        parsing_options.update(opt.options)

    message = message_cls()
    return json_format.ParseDict(body, message, **parsing_options)


def convert_message_to_dict(_, request_definition, message):
    method_annotations = request_definition.method_annotations
    printing_options = {}

    for opt in helpers.get_values_of_type(method_annotations, _EncodeOption):
        printing_options.update(opt.options)

    return json_format.MessageToDict(message, **printing_options)
