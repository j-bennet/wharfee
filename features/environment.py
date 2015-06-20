# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pexpect
import codecs


def read_fixture_lines(filename):
    """
    Read lines of text from file.
    :param filename: string name
    :return: list of strings
    """
    lines = []
    for line in codecs.open(filename, 'r', encoding='utf-8'):
        lines.append(line.strip())
    return lines


def read_fixture_files():
    """
    Read all files inside fixture_data directory.
    """
    fixture_dict = {}

    current_dir = os.path.dirname(__file__)
    fixture_dir = os.path.join(current_dir, 'fixture_data/')
    for filename in os.listdir(fixture_dir):
        if filename not in ['.', '..']:
            fullname = os.path.join(fixture_dir, filename)
            fixture_dict[filename] = read_fixture_lines(fullname)

    return fixture_dict


def before_all(context):
    """
    Set env parameters.
    """
    os.environ['LINES'] = "50"
    os.environ['COLUMNS'] = "120"
    context.fixture_lines = read_fixture_files()


def after_scenario(context, _):
    """
    Cleans up after each test complete.
    """

    if hasattr(context, 'cli'):
        # Send Ctrl + D into cli
        context.cli.sendcontrol('d')
        context.cli.expect(pexpect.EOF)
