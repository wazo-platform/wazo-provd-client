# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from requests.exceptions import HTTPError
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
            RESTCommand.raise_from_response(response)
        except HTTPError as e:
            raise ProvdError(e, response=response)

    @staticmethod
    def _build_list_params(search=None, fields=None, offset=0, limit=0, order=None, direction=None, *args, **kwargs):
        params = {}
        if args:
            params['q'] = json.dumps(args[0])
        if search:
            params['q'] = json.dumps(search)
        if fields:
            params['fields'] = ','.join(fields)
        if offset:
            params['skip'] = offset
        if limit:
            params['limit'] = limit
        if order and direction:
            params['sort'] = order
            valid_directions = ('asc', 'desc')
            if direction not in valid_directions:
                raise ValueError('Invalid direction {}'.format(direction))
            params['sort_ord'] = direction.upper()
        if kwargs:
            params.update(kwargs)
        return params
