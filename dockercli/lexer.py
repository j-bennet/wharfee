from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import *

from .options import COMMAND_NAMES


class CommandLexer(RegexLexer):
    name = 'Command Line'
    aliases = ['cli']
    filenames = []

    tokens = {
        'root': [
            (words(tuple(COMMAND_NAMES), prefix=r'^', suffix=r'\b'), Generic.Strong),
            (r'--[a-z]+\b', Keyword),
            (r'.*\n', Text),
        ]
    }