#!/usr/bin/env python3
# Copyright 2018 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_provd_client',
    version='1.0',

    description='a simple client library for the wazo-provd HTTP interface',

    author='Wazo Authors',
    author_email='dev@wazo.community',

    url='http://wazo.community',

    packages=find_packages(),

    entry_points={
        'wazo_provd_client.commands': [
            'configs = wazo_provd_client.commands.configs:ConfigsCommand',
            'plugins = wazo_provd_client.commands.plugins:PluginsCommand',
            'devices = wazo_provd_client.commands.devices:DevicesCommand',
            'params = wazo_provd_client.commands.params:ParamsCommand',
        ],
    }
)
