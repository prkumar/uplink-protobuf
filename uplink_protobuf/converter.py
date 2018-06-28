# Static imports
import functools
import inspect

# Third party imports
from google.protobuf import message
from uplink import converters, returns, json

# Local imports
from uplink_protobuf import helpers, json_options


__all__ = ["ProtocolBuffersConverter"]


class ProtocolBuffersConverter(converters.Factory):
    __DECODING_STRATEGIES = {
        returns.json: json_options.parse_json
    }

    __ENCODING_STRATEGIES = {
        json: json_options.convert_message_to_dict
    }

    # === BEGIN Helpers === #

    @staticmethod
    def is_protocol_buffer_class(cls):
        """
        Returns whether or not the given `cls` is a protobuf message
        subclass.
        """
        return inspect.isclass(cls) and issubclass(cls, message.Message)

    @staticmethod
    def _get_strategy(cls, request_definition, strategies):
        if not ProtocolBuffersConverter.is_protocol_buffer_class(cls):
            # Returning None tells Uplink's converter layer that we
            # can't handle this type, so it can move on to the next
            # factory.
            return None

        strategy_keys = tuple(strategies.keys())
        method_annotations = request_definition.method_annotations

        try:
            key = helpers.get_first_of_type(method_annotations, strategy_keys)
        except StopIteration:
            raise KeyError
        else:
            target_strategy = strategies[type(key)]
            return functools.partial(target_strategy, cls, request_definition)

    # === END Helpers === #

    def create_response_body_converter(self, cls, request_definition):
        try:
            return self._get_strategy(
                cls, request_definition, self.__DECODING_STRATEGIES
            )
        except KeyError:
            # Return default callable that can decode Protobuf message
            # from response content.
            def converter(response):
                msg = cls()
                msg.ParseFromString(response.content)
                return msg

            return converter

    def create_request_body_converter(self, cls, request_definition):
        try:
            return self._get_strategy(
                cls, request_definition, self.__ENCODING_STRATEGIES
            )
        except KeyError:
            # Return callable that can serialize Protobuf message.
            def converter(msg):
                return msg.SerializeToString()

            return converter
