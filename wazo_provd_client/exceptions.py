# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests import HTTPError, codes


class ProvdError(HTTPError):

    def __init__(self, *args, **kwargs):
        response = kwargs.get('response', None)
        self.status_code = getattr(response, 'status_code', None)
        super(ProvdError, self).__init__(*args, **kwargs)


class ProvdServiceUnavailable(Exception):
    pass


class InvalidProvdError(Exception):
    pass
