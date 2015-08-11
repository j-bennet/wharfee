# -*- coding: utf-8
from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import Operator, Keyword, Text

from .options import COMMAND_NAMES, all_option_names


class CommandLexer(RegexLexer):
    name = 'Command Line'
    aliases = ['cli']
    filenames = []

    tokens = {
        'root': [
            (words(tuple(COMMAND_NAMES), prefix=r'^', suffix=r'\b'),
             Operator.Word),
            (words(tuple(all_option_names()), prefix=r'', suffix=r'\b'),
             Keyword),
            (r'.*\n', Text),
        ]
    }
