# -*- coding: utf-8
"""
Bottom toolbar for the CLI.
"""
from prompt_toolkit.formatted_text import FormattedText


def create_toolbar_handler(is_long_option, is_fuzzy):
    """
    Create a toolbar handler function.
    :param is_long_option: callable
    :param is_fuzzy: callable
    :return: callable
    """

    assert callable(is_long_option)
    assert callable(is_fuzzy)

    def get_toolbar_items():
        """
        Return bottom menu items.
        :return: FormattedText
        """

        if is_long_option():
            option_mode_class = 'class:bottom-toolbar.on'
            option_mode = 'Long'
        else:
            option_mode_class = 'class:bottom-toolbar.off'
            option_mode = 'Short'

        if is_fuzzy():
            fuzzy_class = 'class:bottom-toolbar.on'
            fuzzy = 'ON'
        else:
            fuzzy_class = 'class:bottom-toolbar.off'
            fuzzy = 'OFF'

        return FormattedText([
            ('class:bottom-toolbar', ' [F2] Help '),
            (option_mode_class, f' [F3] Options: {option_mode} '),
            (fuzzy_class, f' [F4] Fuzzy: {fuzzy} '),
            ('class:bottom-toolbar', ' [F10] Exit ')
        ])

    return get_toolbar_items
