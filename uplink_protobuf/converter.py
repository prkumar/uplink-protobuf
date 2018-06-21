# Third party imports
from uplink import converters, returns, json

# Local imports
from uplink_protobuf import helpers
from uplink_protobuf.decorators import protobuf


__all__ = ["ProtocolBuffersConverter"]


class ProtocolBuffersConverter(converters.ConverterFactory):

    def make_response_body_converter(self, cls, argument_annotations,
                                     method_annotations):
        if not helpers.is_protocol_buffer_class(cls):
            # We cannot handle this type.
            return None

        # Method annotations are passed in as list iterator. This is
        # fixed in Uplink v0.6.0
        method_annotations = list(method_annotations)

        if helpers.has_value_of_type(method_annotations, protobuf.from_json):
            # Grab the first _FromJson annotation
            annotation = helpers.get_first_of_type(
                method_annotations, protobuf.from_json)
            return helpers.create_json_deserializer(cls, **annotation.options)

        elif helpers.has_value_of_type(method_annotations, returns.json):
            # Return from JSON
            return helpers.create_json_deserializer(cls)

        else:
            def converter(response):
                msg = cls()
                msg.ParseFromString(response.content)
            return converter

    def make_request_body_converter(self, cls, argument_annotations,
                                    method_annotations):

        if not helpers.is_protocol_buffer_class(cls):
            # We cannot handle this type.
            return None

        # Method annotations are passed in as list iterator. This is
        # fixed in Uplink v0.6.0
        method_annotations = list(method_annotations)

        if helpers.has_value_of_type(method_annotations, protobuf.send_json):
            annotation = helpers.get_first_of_type(
                method_annotations, protobuf.send_json)
            return helpers.create_json_serializer(**annotation.options)

        elif helpers.has_value_of_type(method_annotations, json):
            return helpers.create_json_serializer()

        else:
            def converter(msg):
                return msg.SerializeToString()
            return converter
