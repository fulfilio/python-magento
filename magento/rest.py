# coding: utf-8
try:
    import requests
    import json
except ImportError:
    pass


class Client(object):

    def __init__(self, url, token, verify_ssl=True):
        self._url = url
        self._token = token
        self._verify_ssl = verify_ssl

    def call(self, resource_path, arguments):
        url = '%s/%s' % (self._url, resource_path)
        res = requests.get(
            url, params=arguments, verify=self._verify_ssl,
            headers={'Authorization': 'Bearer %s' % self._token})
        res.raise_for_status()
        return res.json()
