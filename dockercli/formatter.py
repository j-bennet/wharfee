"""
Helper functions to format output for CLI.
"""
from tabulate import tabulate


def format_data(data):
    """
    Uses tabulate to format the iterable.
    :return: string (multiline)
    """
    if isinstance(data, list):
        if isinstance(data[0], tuple):
            text = tabulate(data)
            return text.split('\n')
        elif isinstance(data[0], dict):
            data = flatten_rows(data)
            data = truncate_rows(data)
            text = tabulate(data, headers='keys')
            return text.split('\n')
    return data


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


def truncate_rows(rows, length=25):
    """
    Truncate every string value in a dictionary up to a certain length.
    :param rows: iterable of dictionaries
    :param length: int
    :return:
    """

    def trimto(str):
        if isinstance(str, basestring):
            return str[:length+1]
        return str

    result = []
    for row in rows:
        if isinstance(row, dict):
            result.append({k: trimto(v) for k, v in row.iteritems()})
        else:
            result.append(row)
    return result
