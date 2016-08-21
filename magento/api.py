# -*- coding: utf-8 -*-
'''
    magento.api

    Generic API for magento

    :license: BSD, see LICENSE for more details
'''
import sys
from threading import RLock

PROTOCOLS = []
try:
    if sys.version_info <= (2,):
        from xmlrpclib import ServerProxy
    else:
        from xmlrpc.client import ServerProxy
except ImportError:
    pass
else:
    PROTOCOLS.append('xmlrpc')

try:
    from suds.client import Client
except ImportError:
    pass
else:
    PROTOCOLS.append('soap')

from . import rest
try:
    import requests
    import json
except ImportError:
    pass
else:
    PROTOCOLS.append('rest')

from magento.utils import expand_url, camel_2_snake


class ClientApiMeta(type):
    """
    A Metaclass that automatically injects objects that inherit from API
    as properties.
    """
    def __new__(meta, name, bases, dct):
        abstract = dct.get('__abstract__', False)
        Klass = super(ClientApiMeta, meta).__new__(meta, name, bases, dct)

        if not abstract:
            setattr(
                API, camel_2_snake(name),
                property(lambda self: self.get_instance_of(Klass))
            )

        return Klass


class API(object):
    """
    Generic API to connect to magento
    """
    __metaclass__ = ClientApiMeta
    __abstract__ = True

    def __init__(self, url, username, password,
                 version='1.3.2.4', full_url=False,
                 protocol='xmlrpc', transport=None,
                 verify_ssl=True):
        """
        This is the Base API class which other APIs have to subclass. By
        default the inherited classes also get the properties of this
        class which will allow the use of the API with the `with` statement

        A typical example to extend the API for your subclass is given below::

           from magento.api import API

            class Core(API):

                def websites(self):
                    return self.call('ol_websites.list', [])

                def stores(self):
                    return self.call('ol_groups.list', [])

                def store_views(self):
                    return self.call('ol_storeviews.list', [])

        The above real life example extends the API for the custom API
        implementation for the magento extension

            magento-community/Openlabs_OpenERPConnector

        Example usage ::

            from magento.api import API

            with API(url, username, password) as magento_api:
                return magento_api.call('customer.list', [])

        .. note:: Python with statement has to be imported from __future__
        in older versions of python. *from __future__ import with_statement*

        If you want to use the API as a normal class, then you have to manually
        end the session. A typical example is below::

            from magento.api import API

            api = API(url, username, password)
            api.connect()
            try:
                return api.call('customer.list', [])
            finally:
                api.client.endSession(api.session)

        :param url: URL to the magento instance.
                    By default the URL is treated as a base url
                    of the domain to which the api part of the URL
                    is added. If you want to specify the complete
                    URL, set the full_url flag as True.
        :param username: API username of the Web services user. Note
                    that this is NOT magento admin username
        :param password: API password of the Web services user.
        :param version: The version of magento the connection is being made to.
                        It is recommended to specify this as there could be
                        API specific changes in certain calls. Default value is
                        1.3.2.4
        :param full_url: If set to true, then the `url` is expected to
                    be a complete URL
        :param protocol: 'xmlrpc' and 'soap' are valid values
        :param transport: optional xmlrpclib.Transport subclass for
                    use in xmlrpc requests
        :param verify_ssl: for REST API, skip SSL validation if False
        """
        assert protocol \
            in PROTOCOLS, "protocol must be %s" % ' OR '.join(PROTOCOLS)
        self.url = str(full_url and url or expand_url(url, protocol))
        self.username = username
        self.password = password
        self.protocol = protocol
        self.version = version
        self.transport = transport
        self.session = None
        self.client = None
        self.verify_ssl = verify_ssl
        self.lock = RLock()

    def connect(self):
        """
        Connects to the service
        but does not login. This could be used as a connection test
        """
        if self.protocol == 'xmlrpc':
            if self.transport:
                self.client = ServerProxy(
                    self.url, allow_none=True, transport=self.transport)
            else:
                self.client = ServerProxy(self.url, allow_none=True)
        elif self.protocol == 'rest':
            # Use an authentication token as the password
            self.client = rest.Client(self.url, self.password,
                                      verify_ssl=self.verify_ssl)
        else:
            self.client = Client(self.url)

    def __enter__(self):
        """
        Entry point for with statement
        Logs in and creates a session
        """
        if self.client is None:
            self.connect()
        if self.protocol == 'xmlrpc':
            self.session = self.client.login(
                self.username, self.password)
        elif self.protocol == 'rest':
            self.session = True
        else:
            self.session = self.client.service.login(
                self.username, self.password)
        return self

    def __exit__(self, type, value, traceback):
        """
        Exit point

        Closes session with magento
        """
        if self.protocol == 'xmlrpc':
            self.client.endSession(self.session)
        elif self.protocol == 'soap':
            self.client.service.endSession(self.session)
        self.session = None

    def call(self, resource_path, arguments):
        """
        Proxy for SOAP call API
        """
        if self.protocol == 'xmlrpc':
            return self.client.call(self.session, resource_path, arguments)
        elif self.protocol == 'rest':
            return self.client.call(resource_path, arguments)
        else:
            return self.client.service.call(
                self.session, resource_path, arguments)

    def multiCall(self, calls):
        """
        Proxy for multicalls
        """
        if self.protocol == 'xmlrpc':
            return self.client.multiCall(self.session, calls)
        else:
            return self.client.service.multiCall(self.session, calls)

    _missing = []

    def get_instance_of(self, Klass):
        """
        Return an instance of the client API with the same auth credentials
        that the API server was instanciated with. The created instance is
        cached, so subsequent requests get an already existing instance.

        :param Klass: The klass for which the instance has to be created.
        """
        with self.lock:
            value = self.__dict__.get(Klass.__name__, self._missing)
            if value is self._missing:
                value = Klass(
                    self.url,
                    self.username,
                    self.password,
                    self.version,
                    True,
                    self.protocol,
                )
                self.__dict__[Klass.__name__] = value.__enter__()
            return value
