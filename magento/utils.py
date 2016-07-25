# -*- coding: UTF-8 -*-
'''
    magento.utils

    General purpose utility functions

    :license: BSD, see LICENSE for more details
'''


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

