# wazo-provd-client

A python client library to access wazo-provd

## Usage

```python
from wazo_provd_client import Client

c = Client('localhost')

c.status.get()
{"rest_api": "ok"}
```

### Operation in progress

The devices and plugins commands provide some methods that are asynchronous. To get
the state of an operation, provd provides a resource called an Operation In Progress.
Every asynchronous method returns the OperationInProgress object that it created.
One important thing to know about this mechanism is that *provd does not delete the
resource it created*. To avoid resource leaking, you must use the delete method on
the object returned or use the OperationInProgress as a context manager.

### Devices command

```python
# Get device info
device = c.devices.get('device_id')

# Example results
{
    'added': 'auto',
    'ip': '10.34.0.123',
    'configured': False,
    'mac': '00:11:22:33:44:55',
    'config': 'autoprov1234567890',
    'id': '5dad2f2b3725438baa400bea8a55f2ae'
}

# Get a list of devices
device_list = c.devices.list(search={'ip': '10.10.10.10'})

# Example results
{
    'devices': [
        {
            'added': 'auto',
            'ip': '10.34.0.123',
            'configured': False,
            'mac': '00:11:22:33:44:55',
            'config': 'autoprov1234567890',
            'id': '5dad2f2b3725438baa400bea8a55f2ae'
        }
    ]
}


# Update device info
# The value must be a dictionary containing at least the id key
c.devices.update({'id': '1234567890abcdef', 'ip': '10.10.10.10'})

# Create a device
device_id = c.devices.create({'ip': '10.10.10.10', 'mac': '00:11:22:33:44:55', 'plugin': 'zero'})

# Example results
{'id': '1234567890abcdef'}

# Delete a device
c.devices.delete('1234567890abcdef')

# Synchronize a device and get its operation in progress
operation_location = c.devices.synchronize('1234567890abcdef')

# Reconfigure device
c.devices.reconfigure('1234567890abcdef')

# Create device from DHCP request
c.devices.create_from_dhcp(
    {
        "ip": "string",
        "mac": "string",
        "op": "commit",
        "options": [
            "string"
        ]
    }
)
```

### Plugins Command

```python
# Update plugin list
c.plugins.update()

# Get plugin info
plugin = c.plugins.get('wazo-aastra-3.3.1-SP4')

# Get a list of installed plugin names
installed_plugin_names = c.plugins.list()

# Get a list of installed plugins
plugins_installed = c.plugins.list_installed()

# Get a list of installable plugins
plugins_installable = c.plugins.list_installable()

# Example results
{
    'pkgs': {
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
    }
}

# Install a plugin and get its operation in progress
operation_progress = c.plugins.install('zero')

# Update the status of the operation in progress
operation_progress.update()

# Delete the operation in progress
operation_progress.delete()

# or you can also use it directly as a context manager
with c.plugins.install('zero') as operation:
    operation.update()

# Uninstall a plugin
c.plugins.uninstall('zero')

# Upgrade a plugin and get its operation in progress
operation_progress = c.plugins.upgrade('wazo-aastra-3.3.1-SP4')

# List packages installed for a plugin
packages_installed = c.plugins.get_packages_installed('wazo-aastra-3.3.1-SP4')

# List packages installable for a plugin
packages_installable = c.plugins.get_packages_installable('wazo-aastra-3.3.1-SP4')

# Install a package for a plugin and get its operation in progress
operation_progress = c.plugins.install_package('wazo-aastra-3.3.1-SP4', '6730i-fw')

# Uninstall a package for a plugin
c.plugins.uninstall_package('wazo-aastra-3.3.1-SP4', '6730i-fw')

# Upgrade a package for a plugin and get its operation in progress
operation_progress = c.plugins.upgrade_package('wazo-aastra-3.3.1-SP4', '6730i-fw')
```

### Configs Command

```python
# Get list of template config line
config_registrars = c.configs.list_registrar()

# Example results
{
    'configs': [
        {
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
        }
    ]
}


# Get list of template config device
config_devices = c.configs.list_device()

# Example results
{
    'configs': [
        {
        'X_type': 'device',
        'uuid': '7169eb2d07564d9fb1cddac0e4fbe010',
        'id': '7169eb2d07564d9fb1cddac0e4fbe010',
        'label': 'test22',
        'parent_ids': [],
        'raw_config': {
                'X_key': 'xivo',
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
                'user_username': 'user name'
            }
        }
    ]
}


# Get config by id
config = c.configs.get(id)

# Example results
{
    'X_type': 'device',
    'uuid': '7169eb2d07564d9fb1cddac0e4fbe010',
    'id': '7169eb2d07564d9fb1cddac0e4fbe010',
    'label': 'test22',
    'parent_ids': [],
    'raw_config': {
        'X_key': 'xivo',
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
        'user_username': 'user name'
    }
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

### Params Command

```python
# Get list of provd configuration parameters
params = c.params.list()

# Example results
{
    'params': [
        {
            'value': 'http://provd.wazo.community/plugins/2/stable',
            'id': 'plugin_server',
            'links': [
                {
                    'href': '/configure/plugin_server',
                    'rel': 'srv.configure.param',
                }
            ],
            'description': 'The plugins repository URL'
        },
    ]
}
# Get the value of a parameter
value = c.params.get(param_name)

# Update a configuration parameter
c.params.update(param_name, value)

# Unset the value of a parameter
c.params.delete(param_name)
```

## Tests

### Running unit tests

```
pip install tox
tox --recreate -e py311
```

## How to implement a new command

Someone trying to implement a new command to the client would have to implement a new class,
sub-classing the RESTCommand (available in wazo-lib-rest-client). The new class must be in the
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
