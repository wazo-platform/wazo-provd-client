# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import base64
import json

from wazo_provd_client.command import ProvdCommand


class ConfigsCommand(ProvdCommand):
    resource = 'cfg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def list_registrar(self, **params):
        url = '{base}/configs'.format(base=self.base_url)
        params.update(self._prepare_query({'X_type': 'registrar'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_device(self, **params):
        url = '{base}/configs'.format(base=self.base_url)
        params.update(self._prepare_query({'X_type': 'device'}))
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def find(self, *args, **kwargs):
        """Return a list of configs matching the given parameters.

        Valid arguments to this methods are, in order:
          selector -- a selector (i.e. a dict)
          fields -- a list of fields
          skip -- a skip value, i.e. the number of documents to skip
          limit -- a limit, i.e. the maximum number of documents to return
          sort -- a tuple (key, direction), where key is the key to do the sort
            and direction is either 1 for ASC and -1 for DESC

        """
        url = '{base}/configs'.format(base=self.base_url)
        r = self.session.get(url, params=self._build_find_query(*args, **kwargs))
        return r.json()

    def get_all(self):
        url = '{base}/configs'.format(base=self.base_url)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def get(self, id_):
        url = '{base}/configs/{id_}'.format(base=self.base_url, id_=id_)
        r = self.session.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def get_raw(self, id_):
        url = '{base}/configs/{id_}/raw'.format(base=self.base_url, id_=id_)
        r = self.session.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def create(self, data):
        url = '{base}/configs'.format(base=self.base_url)
        r = self.session.post(url, json={'config': data}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def update(self, id_, data):
        url = '{base}/configs/{id_}'.format(base=self.base_url, id_=id_)
        r = self.session.put(url, json={'config': data}, headers=self._headers)
        self.raise_from_response(r)

    def delete(self, id_):
        url = '{base}/configs/{id_}'.format(base=self.base_url, id_=id_)
        r = self.session.delete(url)
        self.raise_from_response(r)

    def autocreate(self):
        url = '{base}/autocreate'.format(base=self.base_url)
        r = self.session.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def _prepare_query(self, query):
        query = base64.b64encode(json.dumps(query).encode('utf-8'))
        return {'q64': query}
