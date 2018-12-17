# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import base64
import json

from wazo_provd_client.command import ProvdCommand


class ParamsCommand(ProvdCommand):
    resource = 'configure'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def list(self):
        url = '{base}'.format(base=self.base_url)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def get(self, param):
        url = '{base}/{param}'.format(base=self.base_url, param=param)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()['param']

    def update(self, param, value):
        url = '{base}/{param}'.format(base=self.base_url, param=param)
        data = {'param': {'value': value}}
        r = self.session.put(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def delete(self, param):
        self.update(param, None)
