# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from unittest import TestCase

from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)
from mock import Mock

from ..exceptions import InvalidProvdError, ProvdError


class TestProvdError(TestCase):

    def test_when_response_has_no_json_then_raise_invalid(self):
        response = Mock()
        response.json.side_effect = ValueError

        assert_that(calling(ProvdError).with_args(response),
                    raises(InvalidProvdError))

    def test_when_response_is_missing_keys_then_raise_invalid(self):
        response = Mock()
        response.json.return_value = {}

        assert_that(calling(ProvdError).with_args(response),
                    raises(InvalidProvdError))

    def test_when_response_is_valid_then_return(self):
        response = Mock()
        response.json.return_value = {
            'message': 'message',
            'error_id': 'error_id',
            'details': 'details',
            'timestamp': 'timestamp',
        }

        error = ProvdError(response)

        assert_that(error.response, equal_to(response))
