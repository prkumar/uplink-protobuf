# Third party imports
from uplink import json, returns

# Local imports
from uplink_protobuf import (
    ProtocolBuffersConverter,
    json_options
)


def patch_is_protocol_buffer_class(mocker, return_value):
    patch = mocker.patch(
        "uplink_protobuf.ProtocolBuffersConverter.is_protocol_buffer_class"
    )
    patch.return_value = return_value


def run_converter_test(
    method, mocker, message_mock, request_definition_mock, converter_args
):
    # Setup
    patch_is_protocol_buffer_class(mocker, True)

    cls = mocker.stub(name="MessageClassStub")
    cls.return_value = message_mock

    # Run
    factory = ProtocolBuffersConverter()
    converter = method(factory, cls, request_definition_mock)
    converter(converter_args)


def run_create_response_body_converter_test(*args, **kwargs):
    run_converter_test(
        ProtocolBuffersConverter.create_response_body_converter, *args, **kwargs
    )


def run_create_request_body_converter_test(*args, **kwargs):
    run_converter_test(
        ProtocolBuffersConverter.create_request_body_converter, *args, **kwargs
    )


def test_create_response_body_converter__from_protobuf(
    mocker, message_mock, request_definition_mock, response_mock
):
    # Setup
    response_mock.content = "Content"
    request_definition_mock.method_annotations = ()

    # Run
    run_create_response_body_converter_test(
        mocker, message_mock, request_definition_mock, response_mock
    )

    # Verify
    message_mock.ParseFromString.assert_called_with("Content")


def test_create_response_body_converter__returns_json(
    mocker, message_mock, request_definition_mock
):
    # Setup
    json_response = {"hello": "world"}
    request_definition_mock.method_annotations = (returns.json(),)
    ParseDict = mocker.patch("google.protobuf.json_format.ParseDict")

    # Run
    run_create_response_body_converter_test(
        mocker, message_mock, request_definition_mock, json_response
    )

    # Verify
    ParseDict.assert_called_with(json_response, message_mock)


def test_create_response_body_converter__from_json(
    mocker, message_mock, request_definition_mock
):
    # Setup
    json_response = {"hello": "world"}
    request_definition_mock.method_annotations = (
        json_options.ignore_unknown_fields(),
        returns.from_json(),
    )
    ParseDict = mocker.patch("google.protobuf.json_format.ParseDict")

    # Run
    run_create_response_body_converter_test(
        mocker, message_mock, request_definition_mock, json_response
    )

    # Verify
    ParseDict.assert_called_with(
        json_response, message_mock, ignore_unknown_fields=True
    )


def test_create_request_body_converter(
    mocker, message_mock, request_definition_mock
):
    # Setup
    request_definition_mock.method_annotations = ()

    # Run
    run_create_request_body_converter_test(
        mocker, message_mock, request_definition_mock, message_mock
    )

    # Verify
    assert message_mock.SerializeToString.called


def test_create_request_body_converter__json(
    mocker, message_mock, request_definition_mock
):
    # Setup
    request_definition_mock.method_annotations = (json(),)
    MessageToDict = mocker.patch("google.protobuf.json_format.MessageToDict")

    # Run
    run_create_request_body_converter_test(
        mocker, message_mock, request_definition_mock, message_mock
    )

    # Verify
    MessageToDict.assert_called_with(message_mock)


def test_create_request_body_converter__to_json(
    mocker, message_mock, request_definition_mock
):
    # Setup
    request_definition_mock.method_annotations = (
        json_options.include_default_value_fields(),
        json_options.preserve_proto_field_names(),
        json_options.use_integers_for_enums(),
        json(),
    )
    MessageToDict = mocker.patch("google.protobuf.json_format.MessageToDict")

    # Run
    run_create_request_body_converter_test(
        mocker, message_mock, request_definition_mock, message_mock
    )

    # Verify
    MessageToDict.assert_called_with(
        message_mock,
        including_default_value_fields=True,
        preserving_proto_field_name=True,
        use_integers_for_enums=True,
    )


def test_create_response_body_converter__not_protocol_buffer_class(
    request_definition_mock
):
    # Run & Verify
    factory = ProtocolBuffersConverter()
    converter = factory.create_response_body_converter(
        object, request_definition_mock
    )
    assert converter is None


def test_create_request_body_converter__not_protocol_buffer_class(
    request_definition_mock
):
    # Run & Verify
    factory = ProtocolBuffersConverter()
    converter = factory.create_request_body_converter(
        object, request_definition_mock
    )
    assert converter is None
