# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from unittest import TestCase
from requests.exceptions import HTTPError

from hamcrest import (
    assert_that,
    calling,
    raises,
)
from mock import Mock, patch

from ..command import ProvdCommand
from ..exceptions import (
    ProvdError,
    ProvdServiceUnavailable,
)

SOME_ERROR_BODY = {
    'message': 'some message',
    'error_id': 'some-error-id',
    'details': {},
    'timestamp': 'some-date',
}


class TestProvdCommand(TestCase):

    @patch('wazo_provd_client.command.RESTCommand.raise_from_response')
    def test_raise_from_response_no_error(self, parent_raise):
        response = Mock(status_code=200)

        ProvdCommand.raise_from_response(response)

        parent_raise.assert_called_once_with(response)

    def test_raise_from_response_503(self):
        response = Mock(status_code=503)

        assert_that(
            calling(ProvdCommand.raise_from_response).with_args(response),
            raises(ProvdServiceUnavailable)
        )

    @patch('wazo_provd_client.command.RESTCommand.raise_from_response')
    def test_raise_from_response_invalid_error(self, parent_raise):
        response = Mock(status_code=599)

        ProvdCommand.raise_from_response(response)

        parent_raise.assert_called_once_with(response)

    def test_raise_from_response_default_error(self):
        response = Mock(status_code=404)

        assert_that(
            calling(ProvdCommand.raise_from_response).with_args(response),
            raises(ProvdError)
        )
