# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_provd_client.command import ProvdCommand


class DevicesCommand(ProvdCommand):
    resource = 'dev_mgr'
    _headers = {
        'Content-Type': 'application/vnd.proformatique.provd+json'
    }

    def get_all(self):
        url = '{base}/devices'.format(base=self.base_url)
        r = self.session.get(url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def get(self, device_id):
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=device_id)
        r = self.session.get(url)
        self.raise_from_response(r)
        return r.json()

    def update(self, device_id, data):
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=device_id)
        data = {'device': data}
        data['device']['id'] = device_id
        r = self.session.put(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def create(self, data):
        url = '{base}/devices'.format(base=self.base_url)
        r = self.session.post(url, json={'device': data}, headers=self._headers)
        self.raise_from_response(r)
        return r.json()

    def delete(self, device_id):
        url = '{base}/devices/{id_}'.format(base=self.base_url, id_=device_id)
        r = self.session.delete(url)
        self.raise_from_response(r)

    def synchronize(self, device_id):
        url = '{base}/synchronize'.format(base=self.base_url)
        data = {'id': device_id}
        r = self.session.post(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def reconfigure(self, device_id):
        url = '{base}/reconfigure'.format(base=self.base_url)
        data = {'id': device_id}
        r = self.session.post(url, json=data, headers=self._headers)
        self.raise_from_response(r)

    def insert_from_dhcp(self, data):
        url = '{base}/dhcpinfo'.format(base=self.base_url)
        r = self.session.post(url, json={'dhcp_info': data}, headers=self._headers)
        self.raise_from_response(r)
