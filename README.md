# wazo-provd-client

A python client library to access xivo-provd

## Usage

```python
from wazo_provd_client import Client

c = Client('localhost', verify_certificate=False)
```

### Plugins Command

```python
# Update plugins list
c.plugins.update()

# Get plugin info
plugin = c.plugins.get('xivo-aastra-2.6.0.2019')

# Get list of installed plugins
plugins_installed = c.plugins.list_installed(search='aastra')

# Get list of installable plugins
plugins_installable = c.plugins.list_installable()

    # example of result
    [{
        'null': {
            'capabilities': {'*, *, *': {'sip.lines': 0}},
            'description': 'Plugin that offers no configuration service and rejects TFTP/HTTP requests.',
            'dsize': 943,
            'sha1sum': '873bf36b8024c74a85ee60f983254542fe16c32d',
            'version': '1.0'
       },
        'zero': {
            'capabilities': {'*, *, *': {'sip.lines': 0}},
            'description': 'Plugin that offers no configuration service and serves TFTP/HTTP requests in its var/tftpboot directory.',
            'dsize': 1043,
            'sha1sum': 'b41a34b3b0b70512057a75465e0e76338b62a5b2',
            'version': '1.0'
       }
    }]

# Install a plugin
c.plugins.install('zero')

# Uninstall a plugin
c.plugins.uninstall('zero')

# Upgrade a plugin
c.plugins.upgrade('xivo-aastra-2.6.0.2019')

# List packages installed for a plugin
packages_installed = c.plugins.get_packages_installed('xivo-aastra-2.6.0.2019')

# List packages installable for a plugin
packages_installable = c.plugins.get_packages_installable('xivo-aastra-2.6.0.2019')

# Install a package for a plugin
c.plugins.install_package('xivo-aastra-2.6.0.2019', '6730i-fw')

# Uninstall a package for a plugin
c.plugins.uninstall_package('xivo-aastra-2.6.0.2019', '6730i-fw')

# Upgrade a package for a plugin
c.plugins.uninstall_package('xivo-aastra-2.6.0.2019', '6730i-fw')
```

### Configs Command

```python
# Get list of template config line
config_registrars = c.configs.list_registrar()

    # example of result
    [{
        'X_type': 'registrar',
        'displayname': 'local',
        'id': 'default',
        'parent_ids': [],
        'proxy_backup': None,
        'proxy_main': '10.33.0.10',
        'raw_config': {'X_key': 'xivo'},
        'registrar_backup': None,
        'registrar_main': '10.33.0.10',
        'uuid': 'default'
    },
    {
        'X_type': 'registrar',
        'displayname': 'test22',
        'id': 'ce474e86abb04bd781e59a4461c27da5',
        'parent_ids': [],
        'proxy_backup': None,
        'proxy_main': '1.2.3.4',
        'raw_config': {'X_key': 'xivo'},
        'registrar_backup': None,
        'registrar_main': '1.2.3.4'
    }]


# Get list of template config device
config_devices = c.configs.list_device()

    # example of result
    [{
    'X_type': 'device',
    'uuid': '7169eb2d07564d9fb1cddac0e4fbe010',
    'id': '7169eb2d07564d9fb1cddac0e4fbe010',
    'label': 'test22',
    'parent_ids': [],
    'raw_config': {'X_key': 'xivo',
              'admin_password': 'admin passwd',
              'admin_username': 'admin username',
              'config_encryption_enabled': True,
              'locale': 'fr_FR',
              'ntp_enabled': True,
              'ntp_ip': None,
              'protocol': 'SIP',
              'sip_dtmf_mode': 'SIP-INFO',
              'sip_subscribe_mwi': True,
              'timezone': 'America/Porto_Acre',
              'user_password': 'user passwd',
              'user_username': 'user name'}
    }]


# Get config by id
config = c.configs.get(id)

    # example of result
    {
    'X_type': 'device',
    'uuid': '7169eb2d07564d9fb1cddac0e4fbe010',
    'id': '7169eb2d07564d9fb1cddac0e4fbe010',
    'label': 'test22',
    'parent_ids': [],
    'raw_config': {'X_key': 'xivo',
              'admin_password': 'admin passwd',
              'admin_username': 'admin username',
              'config_encryption_enabled': True,
              'locale': 'fr_FR',
              'ntp_enabled': True,
              'ntp_ip': None,
              'protocol': 'SIP',
              'sip_dtmf_mode': 'SIP-INFO',
              'sip_subscribe_mwi': True,
              'timezone': 'America/Porto_Acre',
              'user_password': 'user passwd',
              'user_username': 'user name'}
    }

# Create a config
config_id = c.configs.create(resource)

# Update a config
c.configs.update(id, resource)

# Delete a config
c.configs.delete(id)

# Create config for autoprov
config_id = c.configs.autocreate()
```

## Tests

### Running unit tests

```
pip install tox
tox --recreate -e py35
```

## How to implement a new command

Someone trying to implement a new command to the client would have to implement a new class,
sub-classing the RESTCommand (available in xivo-lib-rest-client). The new class must be in the
setup.py in the entry points under `wazo_provd_client.commands`. The name of the entry point is used
as the handle on the client. For example, if your new entry point entry looks like this:

```python
entry_points={
    'wazo_provd_client.commands': [
        'foo = package.to.foo:FooCommand'
    ]
}
```

then your command will be accessible from the client like this:

```python
c = Client(...)

c.foo.bar()  # bar is a method of the FooCommand class
```
