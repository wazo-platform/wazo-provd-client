# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_provd_client.command import ProvdCommand
from wazo_provd_client.operation import OperationInProgress


class PluginsCommand(ProvdCommand):
    resource = 'pg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def update(self):
        url = '{base}/install/update'.format(base=self.base_url)
        r = self.session.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def get(self, id_):
        url = '{base}/plugins/{id_}/info'.format(base=self.base_url, id_=id_)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def upgrade(self, id_):
        url = '{base}/install/upgrade'.format(base=self.base_url)
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def install(self, id_):
        url = '{base}/install/install'.format(base=self.base_url)
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def uninstall(self, id_):
        url = '{base}/install/uninstall'.format(base=self.base_url)
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)

    def list_installed(self, **params):
        url = '{base}/install/installed'.format(base=self.base_url)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installable(self, **params):
        url = '{base}/install/installable'.format(base=self.base_url)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installed(self, plugin, **params):
        url = '{base}/plugins/{plugin}/install/installed'.format(base=self.base_url, plugin=plugin)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installable(self, plugin, **params):
        url = '{base}/plugins/{plugin}/install/installable'.format(base=self.base_url, plugin=plugin)
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def install_package(self, plugin, package):
        url = '{base}/plugins/{plugin}/install/install'.format(base=self.base_url, plugin=plugin)
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def uninstall_package(self, plugin, package):
        url = '{base}/plugins/{plugin}/install/uninstall'.format(base=self.base_url, plugin=plugin)
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)

    def upgrade_package(self, plugin, package):
        url = '{base}/plugins/{plugin}/install/upgrade'.format(base=self.base_url, plugin=plugin)
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])
