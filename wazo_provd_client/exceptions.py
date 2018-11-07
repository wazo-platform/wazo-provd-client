# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from requests import HTTPError, codes


class ProvdError(HTTPError):

    def __init__(self, response):
        self.status_code = response.status_code
        self.message = response.text
        valid_provd_errors = (codes.bad_request, codes.unsupported_media_type,
                              codes.not_found, codes.server_error)
        if self.status_code not in valid_provd_errors:
            raise InvalidProvdError()

        exception_message = '{e.message}'.format(e=self)
        super(ProvdError, self).__init__(exception_message, response=response)


class ProvdServiceUnavailable(ProvdError):
    pass


class InvalidProvdError(Exception):
    pass
