# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests import HTTPError, codes


class ProvdError(HTTPError):
    pass

class ProvdServiceUnavailable(Exception):
    pass


class InvalidProvdError(Exception):
    pass
