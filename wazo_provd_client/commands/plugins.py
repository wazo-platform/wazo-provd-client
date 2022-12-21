# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_provd_client.command import ProvdCommand
from wazo_provd_client.operation import OperationInProgress


class PluginsCommand(ProvdCommand):
    resource = 'pg_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def update(self):
        url = f'{self.base_url}/install/update'
        r = self.session.post(url, json={}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def get(self, id_):
        url = f'{self.base_url}/plugins/{id_}/info'
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()['plugin_info']

    def upgrade(self, id_):
        url = f'{self.base_url}/install/upgrade'
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def install(self, id_):
        url = f'{self.base_url}/install/install'
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def uninstall(self, id_):
        url = f'{self.base_url}/install/uninstall'
        r = self.session.post(url, json={'id': id_}, headers=self._headers)
        self.raise_from_response(r)

    def list(self, **params):
        url = f'{self.base_url}/plugins'
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installed(self, **params):
        url = f'{self.base_url}/install/installed'
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def list_installable(self, **params):
        url = f'{self.base_url}/install/installable'
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installed(self, plugin, **params):
        url = f'{self.base_url}/plugins/{plugin}/install/installed'
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def get_packages_installable(self, plugin, **params):
        url = f'{self.base_url}/plugins/{plugin}/install/installable'
        r = self.session.get(url, params=params)
        self.raise_from_response(r)
        return r.json()

    def install_package(self, plugin, package):
        url = f'{self.base_url}/plugins/{plugin}/install/install'
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def uninstall_package(self, plugin, package):
        url = f'{self.base_url}/plugins/{plugin}/install/uninstall'
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)

    def upgrade_package(self, plugin, package):
        url = f'{self.base_url}/plugins/{plugin}/install/upgrade'
        r = self.session.post(url, json={'id': package}, headers=self._headers)
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])
