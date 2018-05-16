# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from wazo_provd_client.command import ProvdCommand


class PluginManagerCommand(ProvdCommand):
    resource = 'pg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def __init__(self, client):
        super().__init__(client)
        self.base_url = '{}/install'.format(self.base_url)

    def update(self):
        r = self.session.post('{}/update'.format(self.base_url),
                              data=json.dumps({}),
                              headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

    def install(self, id):
        r = self.session.post('{}/install'.format(self.base_url),
                              data=json.dumps({'id': id}),
                              headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

    def uninstall(self, id):
        r = self.session.post('{}/uninstall'.format(self.base_url),
                              data=json.dumps({'id': id}),
                              headers=self._headers)
        if r.status_code != 201:
            self.raise_from_response(r)

    def list_installed(self, **params):
        r = self.session.get('{}/installed'.format(self.base_url),
                             params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installable(self, **params):
        r = self.session.get('{}/installable'.format(self.base_url),
                             params=params)
        self.raise_from_response(r)
        return r.json()
