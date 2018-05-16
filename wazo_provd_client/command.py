# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_lib_rest_client.command import RESTCommand

from .exceptions import ProvdError
from .exceptions import ProvdServiceUnavailable
from .exceptions import InvalidProvdError


class ProvdCommand(RESTCommand):

    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise ProvdServiceUnavailable(response)

        try:
            raise ProvdError(response)
        except InvalidProvdError:
            RESTCommand.raise_from_response(response)
