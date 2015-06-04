from __future__ import unicode_literals
from __future__ import print_function

from pygments.token import Token


def get_toolbar_items(cli):
    """
    Return bottom menu items
    :param cli:
    :return: list of Token.Toolbar
    """
    _ = cli

    return [
        (Token.Toolbar.Status, ' [F2] Help '),
        (Token.Toolbar.Status, ' [F10] Exit ')
    ]