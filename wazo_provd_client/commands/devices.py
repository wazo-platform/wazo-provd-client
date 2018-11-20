# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_provd_client.command import ProvdCommand


class DevicesCommand(ProvdCommand):
    resource = 'dev_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def get(self, device_id):
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=device_id)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def list(self, *args, **kwargs):
        url = '{base}/devices'.format(base=self.base_url)
        r = self.session.get(url, params=self._build_list_params(*args, **kwargs))
        self.raise_from_response(r)
        return r.json()

    def update(self, data):
        device_id = data.get('id')
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=device_id)
        data = {'device': data}
        r = self.session.put(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def create(self, data):
        url = '{base}/devices'.format(base=self.base_url)
        r = self.session.post(url, json={'device': data}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def delete(self, id_):
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=id_)
        r = self.session.delete(url)
        self.raise_from_response(r)

    def synchronize(self, id_):
        url = '{base}/synchronize'.format(base=self.base_url)
        data = {'id': id_}
        r = self.session.post(url, json=data, headers=self._headers)
        self.raise_from_response(r)
        return r.headers['Location']

    def reconfigure(self, id_):
        url = '{base}/reconfigure'.format(base=self.base_url)
        data = {'id': id_}
        r = self.session.post(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def create_from_dhcp(self, data):
        url = '{base}/dhcpinfo'.format(base=self.base_url)
        r = self.session.post(url, json={'dhcp_info': data}, headers=self._headers)
        self.raise_from_response(r)
