# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

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

    @staticmethod
    def _build_find_query(selector=None, fields=None, skip=0, limit=0, sort=None):
        query_dict = {}
        if selector:
            query_dict['q'] = json.dumps(selector)
        if fields:
            query_dict['fields'] = ','.join(fields)
        if skip:
            query_dict['skip'] = skip
        if limit:
            query_dict['limit'] = limit
        if sort:
            key, direction = sort
            query_dict['sort'] = key
            if direction == 1:
                query_dict['sort_ord'] = 'ASC'
            elif direction == -1:
                query_dict['sort_ord'] = 'DESC'
            else:
                raise ValueError('invalid direction {}'.format(direction))

        return query_dict
