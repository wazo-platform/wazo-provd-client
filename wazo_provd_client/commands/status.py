# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_provd_client.command import ProvdCommand


class StatusCommand(ProvdCommand):
    resource = 'status'
    _headers = {'Content-Type': 'application/vnd.proformatique.provd+json'}

    def get(self):
        r = self.session.get(self.base_url, headers=self._headers)
        self.raise_from_response(r)
        return r.json()
