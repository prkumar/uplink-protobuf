# Static imports
import inspect

# Third party imports
from google.protobuf import message, json_format
from uplink import converters, returns, json

# Local imports
from uplink_protobuf import (
    helpers,
    configure_json_response,
    configure_json_request,
)


__all__ = ["ProtocolBuffersConverter"]


class ProtocolBuffersConverter(converters.Factory):

    # === BEGIN Helpers === #

    @staticmethod
    def is_protocol_buffer_class(cls):
        """
        Returns whether or not the given `cls` is a protobuf message
        subclass.
        """
        return inspect.isclass(cls) and issubclass(cls, message.Message)

    @staticmethod
    def create_json_serializer(**other):
        """
        Builds a callable that converts a protobuf message into a Python
        dictionary.
        """

        def converter(msg):
            return json_format.MessageToDict(msg, **other)

        return converter

    @staticmethod
    def create_json_deserializer(message_cls, **other):
        """
        Builds a callable that converts a JSON response into a protobuf
        message.
        """

        def converter(response):
            msg = message_cls()
            return json_format.ParseDict(response, msg, **other)

        return converter

    # === END Helpers === #

    def create_response_body_converter(self, cls, request_definition):
        if not self.is_protocol_buffer_class(cls):
            # Returning None tells Uplink's converter layer that we
            # can't handle this type, so it can move on to the next
            # factory.
            return None

        method_annotations = request_definition.method_annotations
        options = {}

        if helpers.has_value_of_type(
            method_annotations, configure_json_response
        ):
            # Return callable that can decode JSON response to Protobuf
            # message
            annotation = helpers.get_first_of_type(
                method_annotations, configure_json_response
            )
            options = annotation.options

        if helpers.has_value_of_type(method_annotations, returns.json):
            # Return callable that can decode JSON response to Protobuf
            # message
            return self.create_json_deserializer(cls, **options)

        else:
            # Return callable that can decode Protobuf message from
            # response content.
            def converter(response):
                msg = cls()
                msg.ParseFromString(response.content)

            return converter

    def create_request_body_converter(self, cls, request_definition):

        if not self.is_protocol_buffer_class(cls):
            # Returning None tells Uplink's converter layer that we
            # can't handle this type, so it can move on to the next
            # factory.
            return None

        method_annotations = request_definition.method_annotations
        options = {}

        if helpers.has_value_of_type(
            method_annotations, configure_json_request
        ):
            # Return callable that can encode Protobuf message into
            # JSON.
            annotation = helpers.get_first_of_type(
                method_annotations, configure_json_request
            )
            options = annotation.options

        if helpers.has_value_of_type(method_annotations, json):
            # Return callable that can encode Protobuf message into
            # JSON.
            return self.create_json_serializer(**options)

        else:
            # Return callable that can serialize Protobuf message.
            def converter(msg):
                return msg.SerializeToString()

            return converter
