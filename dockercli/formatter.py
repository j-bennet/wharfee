"""
Helper functions to format output for CLI.
"""
from __future__ import unicode_literals
from __future__ import print_function

from tabulate import tabulate

# Python 3 has no 'basestring' or 'long' type we're checking for.
try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str
    long = int


def format_data(data):
    """
    Uses tabulate to format the iterable.
    :return: string (multiline)
    """
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], tuple):
            if is_plain_lists(data):
                text = tabulate(data)
                return text.split('\n')
            else:
                return format_struct(data, spaces=2)
        elif isinstance(data[0], dict):
            data = flatten_rows(data)
            data = truncate_rows(data)
            text = tabulate(data, headers='keys')
            return text.split('\n')
        elif isinstance(data[0], basestring):
            if len(data) == 1:
                return data
            elif is_plain_list(data):
                return data
            else:
                data = truncate_rows(data)
                text = tabulate(data)
                return text.split('\n')
    return data


def format_struct(data, spaces=1, indent=0, lines=None):

    if lines is None:
        lines = []

    if isinstance(data, dict):
        data = [(k, data[k]) for k in sorted(data.keys())]

    def add_item_to_line(current_item, current_line, is_last_item, current_list):
        """ Helper to add item to end of line """
        if len(current_line) == 0:
            current_indent = ' ' * (indent * spaces)
            current_line = current_indent

        current_line += '{0}'.format(current_item)

        if is_last_item:
            current_list.append(current_line)
            current_line = ''
        else:
            current_line += ': '
        return current_line, current_list

    for row in data:
        line = ''
        l = len(row)
        for i in range(l):
            if isinstance(row[i], dict):
                lines.append(line)
                lines = format_struct(row[i], spaces, indent + 1, lines)
            elif isinstance(row[i], list):
                if is_plain_list(row[i]):
                    item = ', '.join(map(lambda x: '{0}'.format(x), row[i]))
                    line, lines = add_item_to_line(item, line, i == (l - 1), lines)
                else:
                    lines.append(line)
                    lines = format_struct(row[i], spaces, indent + 1, lines)
            else:
                line, lines = add_item_to_line(row[i], line, i == (l - 1), lines)

    return lines


def is_plain_lists(lst):
    """
    Check if all items in list of lists are strings or numbers
    :param lst:
    :return: boolean
    """
    for x in lst:
        if not is_plain_list(x):
            return False
    return True


def is_plain_list(lst):
    """
    Check if all items in list are strings or numbers
    :param lst:
    :return: boolean
    """
    for item in lst:
        if not isinstance(item, basestring) and \
                not isinstance(item, (int, long, float, complex)):
            return False
    return True

def flatten_rows(rows):
    """
    Transform all list or dict values in a dict into comma-separated strings.
    :param rows: iterable of dictionaries
    :return:
    """

    for row in rows:
        for k in row.iterkeys():
            if isinstance(row[k], list):
                row[k] = ', '.join(row[k])
            elif isinstance(row[k], dict):
                row[k] = ', '.join(["{0}: {1}".format(x, y)
                                    for x, y in row[k].iteritems()])
    return rows


def truncate_rows(rows, length=30, length_id=10):
    """
    Truncate every string value in a dictionary up to a certain length.
    :param rows: iterable of dictionaries
    :param length: int
    :param length_id: length for dict keys that end with "Id"
    :return:
    """

    def trimto(str, l):
        if isinstance(str, basestring):
            return str[:l+1]
        return str

    result = []
    for row in rows:
        if isinstance(row, dict):
            updated = {}
            for k, v in row.iteritems():
                if k.endswith('Id'):
                    updated[k] = trimto(v, length_id)
                else:
                    updated[k] = trimto(v, length)
            result.append(updated)
        elif isinstance(row, basestring):
            result.append(trimto(row))
        else:
            result.append(row)
    return result
