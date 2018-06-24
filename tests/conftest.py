# Third party imports
from google.protobuf import message
from uplink.interfaces import RequestDefinition

import pytest


@pytest.fixture
def message_mock(mocker):
    return mocker.Mock(spec=message.Message)


@pytest.fixture
def response_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def request_definition_mock(mocker):
    return mocker.Mock(spec=RequestDefinition)
