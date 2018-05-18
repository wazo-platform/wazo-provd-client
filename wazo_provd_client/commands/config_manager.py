# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import base64
import json

from wazo_provd_client.command import ProvdCommand


class ConfigManagerCommand(ProvdCommand):
    resource = 'cfg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def list_registrar(self, **params):
        url = '{base}/configs'.format(base=self.base)
        params.update(self._prepare_query({'X_type': 'registrar'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_device(self, **params):
        url = '{base}/configs'.format(base=self.base)
        params.update(self._prepare_query({'X_type': 'device'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get(self, id_):
        url = '{base}/configs/{id_}'.format(base=self.base, id_=id_)
        r = self.session.get(url, headers=self._headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def create(self, data):
        url = '{base}/configs'.format(base=self.base)
        r = self.session.post(url, data=json.dumps({'config': data}), headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def update(self, id_, data):
        url = '{base}/configs/{id_}'.format(base=self.base, id_=id_)
        r = self.session.put(url, data=json.dumps({'config': data}), headers=self._headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, id_):
        url = '{base}/configs/{id_}'.format(base=self.base, id_=id_)
        r = self.session.put(url, headers=self._headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def autocreate(self):
        url = '{base}/autocreate'.format(base=self.base)
        r = self.session.post(url, data=json.dumps({}), headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def _prepare_query(self, query):
        query = base64.b64encode(json.dumps(query).encode('utf-8'))
        return {'q64': query}
