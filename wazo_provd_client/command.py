# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from xivo_lib_rest_client.command import RESTCommand

from .exceptions import ProvdError
from .exceptions import ProvdServiceUnavailable
from .exceptions import InvalidProvdError
from . import operation


class ProvdCommand(RESTCommand):

    def _fix_location_url(self, location):
        location_parts = location.split('/')
        return '/'.join(location_parts[3:])  # We do not want /provd/{pg,dev,cfg}_mgr/ prefix

    def get_operation(self, location):
        location = self._fix_location_url(location)
        url = '{base}/{location}'.format(base=self.base_url, location=location)
        r = self.session.get(url)
        self.raise_from_response(r)
        return operation.parse_operation(r.json()['status'])

    def delete_operation(self, location):
        location = self._fix_location_url(location)
        url = '{base}/{location}'.format(base=self.base_url, location=location)
        r = self.session.delete(url)
        self.raise_from_response(r)

    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise ProvdServiceUnavailable(response)

        try:
            raise ProvdError(response)
        except InvalidProvdError:
            RESTCommand.raise_from_response(response)

    @staticmethod
    def _build_list_params(search=None, fields=None, offset=0, limit=0, order=None, direction=None, *args):
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

        return params
