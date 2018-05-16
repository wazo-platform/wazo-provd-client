# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from requests import HTTPError


class ProvdError(HTTPError):

    def __init__(self, response):
        try:
            body = response.json()
        except ValueError:
            raise InvalidProvdError()

        self.status_code = response.status_code
        try:
            self.message = body['message']
            self.error_id = body['error_id']
            self.details = body['details']
            self.timestamp = body['timestamp']
        except KeyError:
            raise InvalidProvdError()

        exception_message = '{e.message}: {e.details}'.format(e=self)
        super(ProvdError, self).__init__(exception_message, response=response)


class ProvdServiceUnavailable(ProvdError):
    pass


class InvalidProvdError(Exception):
    pass
