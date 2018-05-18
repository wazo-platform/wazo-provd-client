wazo-provd-client
=================

A python client library to access xivo-provd

## Usage

```python
from wazo_provd_client import Client

c = Client('localhost', verify_certificate=False)

c.plugins.update()
plugins_installed = c.plugins.list_installed(search='aastra')
plugins_installable = c.plugins.list_installable()
```

## Tests

Running unit tests
------------------

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
