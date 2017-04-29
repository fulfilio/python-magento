# coding: utf-8
try:
    import requests
    from requests import HTTPError
    import json
except ImportError:
    pass


class Client(object):

    def __init__(self, url, token, verify_ssl=True):
        self._url = url
        self._token = token
        self._verify_ssl = verify_ssl

    def call(self, resource_path, arguments, http_method=None, storeview=None):
        url = '%s/%s' % (self._url, resource_path)
        if storeview:
            # https://github.com/magento/magento2/issues/3864
            url = url.replace('/rest/V1/', '/rest/%s/V1/' % storeview)
        if http_method is None:
            http_method = 'get'
        function = getattr(requests, http_method)
        headers = {'Authorization': 'Bearer %s' % self._token}
        kwargs = {'headers': headers}
        if http_method == 'get':
            kwargs['params'] = arguments
        elif arguments is not None:
            kwargs['data'] = json.dumps(arguments)
            headers['Content-Type'] = 'application/json'
        res = function(url, **kwargs)
        if (res.status_code == 400 and res._content):
            raise HTTPError(
                url, res.status_code, res._content, headers, __name__)
        res.raise_for_status()
        return res.json()
