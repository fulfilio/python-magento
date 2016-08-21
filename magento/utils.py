# -*- coding: UTF-8 -*-
'''
    magento.utils

    General purpose utility functions

    :license: BSD, see LICENSE for more details
'''
import re


def expand_url(url, protocol):
    """
    Expands the given URL to a full URL by adding
    the magento soap/wsdl parts

    :param url: URL to be expanded
    :param service: 'xmlrpc' or 'soap'
    """
    if protocol == 'soap':
        ws_part = 'api/?wsdl'
    elif protocol == 'xmlrpc':
        ws_part = 'index.php/api/xmlrpc'
    else:
        ws_part = 'index.php/rest/V1'
    return url.endswith('/') and url + ws_part or url + '/' + ws_part


def camel_2_snake(name):
    "Converts CamelCase to camel_case"
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
