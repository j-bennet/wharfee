# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from pygments.token import Token


def create_toolbar_handler(is_long_option, is_fuzzy):

    assert callable(is_long_option)
    assert callable(is_fuzzy)

    def get_toolbar_items(_):
        """
        Return bottom menu items
        :param _: cli instance
        :return: list of Token.Toolbar
        """

        if is_long_option():
            option_mode_token = Token.Toolbar.On
            option_mode = 'Long'
        else:
            option_mode_token = Token.Toolbar.Off
            option_mode = 'Short'

        if is_fuzzy():
            fuzzy_token = Token.Toolbar.On
            fuzzy = 'ON'
        else:
            fuzzy_token = Token.Toolbar.Off
            fuzzy = 'OFF'

        return [
            (Token.Toolbar, ' [F2] Help '),
            (option_mode_token, ' [F3] Options: {0} '.format(option_mode)),
            (fuzzy_token, ' [F4] Fuzzy: {0} '.format(fuzzy)),
            (Token.Toolbar, ' [F10] Exit ')
        ]

    return get_toolbar_items
