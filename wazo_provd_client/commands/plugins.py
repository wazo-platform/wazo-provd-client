# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from wazo_provd_client.command import ProvdCommand


class PluginsCommand(ProvdCommand):
    resource = 'pg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def update(self):
        url = '{base}/install/update'.format(base=self.base)
        r = self.session.post(url, data=json.dumps({}), headers=self._headers)
        self.raise_from_response(r)

    def install(self, id_):
        url = '{base}/install/install'.format(base=self.base)
        r = self.session.post(url, data=json.dumps({'id': id_}), headers=self._headers)
        self.raise_from_response(r)

    def uninstall(self, id_):
        url = '{base}/install/uninstall'.format(base=self.base)
        r = self.session.post(url, data=json.dumps({'id': id_}), headers=self._headers)
        self.raise_from_response(r)

    def list_installed(self, **params):
        url = '{base}/install/installed'.format(base=self.base)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installable(self, **params):
        url = '{base}/install/installable'.format(base=self.base)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()
