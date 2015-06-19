# -*- coding: utf-8 -*-
import pexpect


def after_scenario(context, scenario):
    """
    Cleans up after each test complete.
    """

    if hasattr(context, 'cli'):
        # Send Ctrl + D into cli
        context.cli.sendcontrol('d')
        context.cli.expect(pexpect.EOF)
