# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_lib_rest_client.client import BaseClient


class Client(BaseClient):
    namespace = 'wazo_provd_client.commands'

    def __init__(self,
                 host,
                 port=8666,
                 version='',
                 **kwargs):
        super(Client, self).__init__(
            host=host,
            port=port,
            version=version,
            **kwargs)
