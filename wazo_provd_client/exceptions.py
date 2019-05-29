# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests import HTTPError, codes


class ProvdError(HTTPError):

    def __init__(self, *args, **kwargs):
        response = kwargs.get('response', None)
        self.status_code = getattr(response, 'status_code', None)
        self.message = getattr(response, 'text', None)
        valid_provd_errors = (
            codes.bad_request,
            codes.unsupported_media_type,
            codes.not_found,
            codes.server_error,
            codes.unauthorized,
        )
        if self.status_code not in valid_provd_errors:
            raise InvalidProvdError()

        exception_message = '{e.message}'.format(e=self)
        super(ProvdError, self).__init__(exception_message, *args, **kwargs)


class ProvdServiceUnavailable(Exception):
    pass


class InvalidProvdError(Exception):
    pass
