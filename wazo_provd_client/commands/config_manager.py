# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json, base64

from wazo_provd_client.command import ProvdCommand


class ConfigManagerCommand(ProvdCommand):
    resource = 'cfg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def __init__(self, client):
        super().__init__(client)
        self.base_url = '{}/configs'.format(self.base_url)

    def list_registrar(self, **params):
        params.update(self._prepare_query({'X_type': 'registrar'}))
        r = self.session.get(self.base_url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_device(self, **params):
        params.update(self._prepare_query({'X_type': 'device'}))
        r = self.session.get(self.base_url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get(self, id):
        r = self.session.get('{}/{}'.format(self.base_url, id),
                             headers=self._headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def create(self, data):
        r = self.session.post(self.base_url,
                              data=json.dumps({'config': data}),
                              headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def update(self, id, data):
        r = self.session.put('{}/{}'.format(self.base_url, id),
                             data=json.dumps({'config': data}),
                             headers=self._headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, id):
        r = self.session.put('{}/{}'.format(self.base_url, id),
                             headers=self._headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def autocreate(self):
        r = self.session.post('{}/autocreate'.format(self.base_url),
                              data=json.dumps({}),
                              headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def _prepare_query(self, query):
        query = base64.b64encode(json.dumps(query).encode('utf-8'))
        return {'q64': query}
