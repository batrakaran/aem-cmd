# coding: utf-8
""" Helper functions for parsing legacy services returning html content. """

import re
from xml.dom import minidom


def split(attr):
    """ Split <key>=<val> into tuple (<key>,<val>),
        if only string is passed, return ('id', <val>)"""
    if '=' in attr:
        ret = attr.split('=')
        return ret[0], ret[1]
    else:
        return 'id', attr


def parse_value(src, node_name, attr):
    """ Parse src, if element of type node_name with id=<attr> is found,
        return it's text content. """
    attr_name, attr_val = split(attr)

    # If the AEM link checker for some reason finds invalid links in the response, it will put img elements that are not
    # properly XML terminated, so for this purpose we simply remove all IMG tags there are.
    src = re.sub(r'<img.*?>', '', src)
    doc = minidom.parseString(src)
    for elem in doc.getElementsByTagName(node_name):
        if elem.attributes.get(attr_name) and \
                        elem.attributes.get(attr_name).value == attr_val:
            return elem.childNodes[0].nodeValue
    raise Exception("Failed to locate path in {}".format(attr_name))
