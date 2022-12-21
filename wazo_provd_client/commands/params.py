# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import json

from wazo_provd_client.command import ProvdCommand


class ParamsCommand(ProvdCommand):
    resource = 'configure'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def list(self):
        url = f'{self.base_url}'
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def get(self, param):
        url = f'{self.base_url}/{param}'
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()['param']

    def update(self, param, value):
        url = f'{self.base_url}/{param}'
        data = {'param': {'value': value}}
        r = self.session.put(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def delete(self, param):
        self.update(param, None)
