# -*- coding: utf-8
from pygments.token import Token
from pygments.util import ClassNotFound
from prompt_toolkit.styles import merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls, style_from_pygments_dict
import pygments.styles


def style_factory(name):
    try:
        pygments_style = pygments.styles.get_style_by_name(name)
    except ClassNotFound:
        pygments_style = pygments.styles.get_style_by_name('native')

    return merge_styles([
        style_from_pygments_cls(pygments_style),
        style_from_pygments_dict({
            Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
            Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
            Token.Menu.Completions.ProgressButton: 'bg:#003333',
            Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
            Token.Toolbar: 'bg:#222222 #cccccc',
            Token.Toolbar.Off: 'bg:#222222 #004444',
            Token.Toolbar.On: 'bg:#222222 #ffffff',
            Token.Toolbar.Search: 'noinherit bold',
            Token.Toolbar.Search.Text: 'nobold',
            Token.Toolbar.System: 'noinherit bold',
            Token.Toolbar.Arg: 'noinherit bold',
            Token.Toolbar.Arg.Text: 'nobold'
        })
    ])
