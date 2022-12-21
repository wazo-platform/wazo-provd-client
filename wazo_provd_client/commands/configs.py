# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import json

from wazo_provd_client.command import ProvdCommand


class ConfigsCommand(ProvdCommand):
    resource = 'cfg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def list_registrar(self, **params):
        url = f'{self.base_url}/configs'
        params.update(self._prepare_query({'X_type': 'registrar'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_device(self, **params):
        url = f'{self.base_url}/configs'
        params.update(self._prepare_query({'X_type': 'device'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list(self, *args, **kwargs):
        url = f'{self.base_url}/configs'
        r = self.session.get(url, params=self._build_list_params(*args, **kwargs))
        self.raise_from_response(r)
        return r.json()

    def get_all(self):
        url = f'{self.base_url}/configs'
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def get(self, id_):
        url = f'{self.base_url}/configs/{id_}'
        r = self.session.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()['config']

    def get_raw(self, id_):
        url = f'{self.base_url}/configs/{id_}/raw'
        r = self.session.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()['raw_config']

    def create(self, data):
        url = f'{self.base_url}/configs'
        r = self.session.post(url, json={'config': data}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def update(self, data):
        id_ = data['id']
        url = f'{self.base_url}/configs/{id_}'
        r = self.session.put(url, json={'config': data}, headers=self._headers)
        self.raise_from_response(r)

    def delete(self, id_):
        url = f'{self.base_url}/configs/{id_}'
        r = self.session.delete(url)
        self.raise_from_response(r)

    def autocreate(self):
        url = f'{self.base_url}/autocreate'
        r = self.session.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def _prepare_query(self, query):
        query = base64.b64encode(json.dumps(query).encode('utf-8'))
        return {'q64': query}
