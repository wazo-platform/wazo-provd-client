# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client.client import BaseClient


class Client(BaseClient):
    namespace = 'wazo_provd_client.commands'

    def __init__(self,
                 host,
                 port=8666,
                 version='0.2',
                 **kwargs):
        super(Client, self).__init__(
            host=host,
            port=port,
            version=version,
            **kwargs)
