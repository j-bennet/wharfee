from pygments.lexer import RegexLexer
from pygments.token import *


class CommandLexer(RegexLexer):
    name = 'Command Line'
    aliases = ['cli']
    filenames = []

    tokens = {
        'root': [
            (r'^[a-z]+\b', Generic.Strong),
            (r'--[a-z]+\b', Keyword),
            (r'.*\n', Text),
        ]
    }