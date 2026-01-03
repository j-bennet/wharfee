# -*- coding: utf-8
"""
Style configuration for the CLI.
"""
from pygments.util import ClassNotFound
import pygments.styles
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls


def style_factory(name):
    """
    Create a style based on a Pygments style name.
    :param name: string: Pygments style name
    :return: Style
    """
    try:
        pygments_style = pygments.styles.get_style_by_name(name)
    except ClassNotFound:
        pygments_style = pygments.styles.get_style_by_name('native')

    custom_style = Style.from_dict({
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.progress-button': 'bg:#003333',
        'completion-menu.progress-bar': 'bg:#00aaaa',
        'bottom-toolbar': 'bg:#222222 #cccccc',
        'bottom-toolbar.off': 'bg:#222222 #004444',
        'bottom-toolbar.on': 'bg:#222222 #ffffff',
        'search': 'noinherit bold',
        'search.text': 'nobold',
        'system': 'noinherit bold',
        'arg': 'noinherit bold',
        'arg.text': 'nobold',
    })

    return merge_styles([
        style_from_pygments_cls(pygments_style),
        custom_style
    ])
