# -*- coding: utf-8 -*-
import shlex


def shlex_split(text):
    """
    Wrapper for shlex.split.
    :param text: string
    :return: list
    """
    return shlex.split(text)


def shlex_first_token(text):
    """
    Get the first token from text using shlex.
    :param text: string
    :return: string
    """
    lexer = shlex.shlex(text)
    return lexer.get_token()
