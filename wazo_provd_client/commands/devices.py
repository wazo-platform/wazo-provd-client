# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_provd_client.command import ProvdCommand
from wazo_provd_client.operation import OperationInProgress


class DevicesCommand(ProvdCommand):
    resource = 'dev_mgr'
    _headers = {'Content-Type': 'application/vnd.proformatique.provd+json'}

    def _build_headers(self, kwargs):
        headers = {}
        # The requests session will use self.tenant_uuid by default
        tenant_uuid = kwargs.pop('tenant_uuid', None)
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid
        return headers

    def _build_headers_with_global_headers(self, kwargs):
        headers = dict(self._headers)
        headers.update(self._build_headers(kwargs))
        return headers

    def get(self, device_id, **kwargs):
        url = f'{self.base_url}/devices/{device_id}'
        r = self.session.get(url, headers=self._build_headers(kwargs), params=kwargs)
        self.raise_from_response(r)
        return r.json()['device']

    def list(self, *args, **kwargs):
        url = f'{self.base_url}/devices'
        r = self.session.get(
            url,
            headers=self._build_headers(kwargs),
            params=self._build_list_params(*args, **kwargs),
        )
        self.raise_from_response(r)
        return r.json()

    def update(self, data, **kwargs):
        device_id = data.get('id')
        url = f'{self.base_url}/devices/{device_id}'
        data = {'device': data}
        r = self.session.put(
            url,
            json=data,
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    def create(self, data, **kwargs):
        url = f'{self.base_url}/devices'
        data = {'device': data}
        r = self.session.post(
            url,
            json=data,
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return r.json()

    def delete(self, id_, **kwargs):
        url = f'{self.base_url}/devices/{id_}'
        r = self.session.delete(
            url, headers=self._build_headers_with_global_headers(kwargs), params=kwargs
        )
        self.raise_from_response(r)

    def synchronize(self, id_, **kwargs):
        url = f'{self.base_url}/synchronize'
        data = {'id': id_}
        r = self.session.post(
            url,
            json=data,
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
        return OperationInProgress(self, r.headers['Location'])

    def reconfigure(self, id_, **kwargs):
        url = f'{self.base_url}/reconfigure'
        data = {'id': id_}
        r = self.session.post(
            url,
            json=data,
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)

    def create_from_dhcp(self, data, **kwargs):
        url = f'{self.base_url}/dhcpinfo'
        r = self.session.post(
            url,
            json={'dhcp_info': data},
            headers=self._build_headers_with_global_headers(kwargs),
            params=kwargs,
        )
        self.raise_from_response(r)
