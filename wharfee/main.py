#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import os
import click
import traceback

from types import GeneratorType
from prompt_toolkit import (AbortAction,
                            Application,
                            CommandLineInterface)
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Always, HasFocus, IsDone
from prompt_toolkit.layout.processors import (
    HighlightMatchingBracketProcessor,
    ConditionalProcessor
)
from prompt_toolkit.buffer import (Buffer, AcceptAction)
from prompt_toolkit.shortcuts import (create_prompt_layout, create_eventloop)
from prompt_toolkit.history import FileHistory

from .client import DockerClient
from .client import DockerPermissionException
from .client import DockerTimeoutException
from .client import DockerSslException
from .completer import DockerCompleter
from .lexer import CommandLexer
from .formatter import format_data
from .formatter import output_stream
from .config import write_default_config, read_config
from .style import style_factory
from .keys import get_key_manager
from .toolbar import create_toolbar_handler
from .options import OptionError
from .logger import create_logger
from .__init__ import __version__

# Added this to avoid the annoying warning: http://click.pocoo.org/5/python3/
click.disable_unicode_literals_warning = True


class WharfeeCli(object):
    """
    The CLI implementation.
    """

    dcli = None
    keyword_completer = None
    handler = None
    saved_less_opts = None
    config = None
    config_template = 'wharfeerc'
    config_name = '~/.wharfeerc'

    def __init__(self):
        """
        Initialize class members.
        Should read the config here at some point.
        """

        self.config = self.read_configuration()
        self.theme = self.config['main']['theme']

        log_file = self.config['main']['log_file']
        log_level = self.config['main']['log_level']
        self.logger = create_logger(__name__, log_file, log_level)

        # set_completer_options refreshes all by default
        self.handler = DockerClient(
            self.config['main'].as_int('client_timeout'),
            self.clear,
            self.set_completer_options)

        self.completer = DockerCompleter(
            long_option_names=self.get_long_options(),
            fuzzy=self.get_fuzzy_match())
        self.set_completer_options()
        self.saved_less_opts = self.set_less_opts()

    def read_configuration(self):
        """

        :return:
        """
        default_config = os.path.join(
            self.get_package_path(), self.config_template)
        write_default_config(default_config, self.config_name)
        return read_config(self.config_name, default_config)

    def get_package_path(self):
        """
        Find out pakage root path.
        :return: string: path
        """
        from wharfee import __file__ as package_root
        return os.path.dirname(package_root)

    def set_less_opts(self):
        """
        Set the "less" options and save the old settings.

        What we're setting:
          -F:
            --quit-if-one-screen: Quit if entire file fits on first screen.
          -R:
            --raw-control-chars: Output "raw" control characters.
          -X:
            --no-init: Don't use termcap keypad init/deinit strings.
            --no-keypad: Don't use termcap init/deinit strings.
            This also disables launching "less" in an alternate screen.

        :return: string with old options
        """
        opts = os.environ.get('LESS', '')
        os.environ['LESS'] = '-RXF'
        return opts

    def revert_less_opts(self):
        """
        Restore the previous "less" options.
        """
        os.environ['LESS'] = self.saved_less_opts

    def write_config_file(self):
        """
        Write config file on exit.
        """
        self.config.write()

    def clear(self):
        """
        Clear the screen.
        """
        click.clear()

    def set_completer_options(self, cons=True, runs=True, imgs=True, vols=True):
        """
        Set image and container names in Completer.
        Re-read if needed after a command.
        :param cons: boolean: need to refresh containers
        :param runs: boolean: need to refresh running containers
        :param imgs: boolean: need to refresh images
        :param vols: boolean: need to refresh volumes
        """

        if cons:
            cs = self.handler.containers(all=True)
            if cs and len(cs) > 0 and isinstance(cs[0], dict):
                containers = [name for c in cs for name in c['Names']]
                self.completer.set_containers(containers)

        if runs:
            cs = self.handler.containers()
            if cs and len(cs) > 0 and isinstance(cs[0], dict):
                running = [name for c in cs for name in c['Names']]
                self.completer.set_running(running)

        if imgs:
            def format_tagged(tagname, img_id):
                if tagname == '<none>:<none>':
                    return img_id[:11]
                return tagname

            def parse_image_name(tag, img_id):
                if ':' in tag:
                    result = tag.split(':', 2)[0]
                else:
                    result = tag
                if result == '<none>':
                    result = img_id[:11]
                return result

            ims = self.handler.images()
            if ims and len(ims) > 0 and isinstance(ims[0], dict):
                images = set([])
                tagged = set([])
                for im in ims:
                    repo_tag = '{0}:{1}'.format(im['Repository'], im['Tag'])
                    images.add(parse_image_name(repo_tag, im['Id']))
                    tagged.add(format_tagged(repo_tag, im['Id']))
                self.completer.set_images(images)
                self.completer.set_tagged(tagged)

        if vols:
            vs = self.handler.volume_ls(quiet=True)
            self.completer.set_volumes(vs)

    def set_fuzzy_match(self, is_fuzzy):
        """
        Setter for fuzzy matching mode
        :param is_fuzzy: boolean
        """
        self.config['main']['fuzzy_match'] = is_fuzzy
        self.completer.set_fuzzy_match(is_fuzzy)

    def get_fuzzy_match(self):
        """
        Getter for fuzzy matching mode
        :return: boolean
        """
        return self.config['main'].as_bool('fuzzy_match')

    def set_long_options(self, is_long):
        """
        Setter for long option names.
        :param is_long: boolean
        """
        self.config['main']['suggest_long_option_names'] = is_long
        self.completer.set_long_options(is_long)

    def get_long_options(self):
        """
        Getter for long option names.
        :return: boolean
        """
        return self.config['main'].as_bool('suggest_long_option_names')

    def refresh_completions(self):
        """
        After processing the command, refresh the lists of
        containers and images as needed
        """
        self.set_completer_options(self.handler.is_refresh_containers,
                                   self.handler.is_refresh_running,
                                   self.handler.is_refresh_images,
                                   self.handler.is_refresh_volumes)

    def run_cli(self):
        """
        Run the main loop
        """
        print('Version:', __version__)
        print('Home: http://wharfee.com')

        history = FileHistory(os.path.expanduser('~/.wharfee-history'))
        toolbar_handler = create_toolbar_handler(self.get_long_options, self.get_fuzzy_match)

        layout = create_prompt_layout(
            message='wharfee> ',
            lexer=CommandLexer,
            get_bottom_toolbar_tokens=toolbar_handler,
            extra_input_processors=[
                ConditionalProcessor(
                    processor=HighlightMatchingBracketProcessor(
                        chars='[](){}'),
                    filter=HasFocus(DEFAULT_BUFFER) & ~IsDone())
            ]
        )

        cli_buffer = Buffer(
            history=history,
            completer=self.completer,
            complete_while_typing=Always(),
            accept_action=AcceptAction.RETURN_DOCUMENT)

        manager = get_key_manager(
            self.set_long_options,
            self.get_long_options,
            self.set_fuzzy_match,
            self.get_fuzzy_match)

        application = Application(
            style=style_factory(self.theme),
            layout=layout,
            buffer=cli_buffer,
            key_bindings_registry=manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            on_abort=AbortAction.RETRY,
            ignore_case=True)

        eventloop = create_eventloop()

        self.dcli = CommandLineInterface(
            application=application,
            eventloop=eventloop)

        while True:
            try:
                document = self.dcli.run(True)
                self.handler.handle_input(document.text)

                if isinstance(self.handler.output, GeneratorType):
                    output_stream(self.handler.command,
                                  self.handler.output,
                                  self.handler.logs)

                elif self.handler.output is not None:
                    lines = format_data(
                        self.handler.command,
                        self.handler.output)
                    click.echo_via_pager('\n'.join(lines))

                if self.handler.after:
                    for line in self.handler.after():
                        click.echo(line)

                if self.handler.exception:
                    # This was handled, just log it.
                    self.logger.warning('An error was handled: %r',
                                        self.handler.exception)

                self.refresh_completions()

            except OptionError as ex:
                self.logger.debug('Error: %r.', ex)
                self.logger.error("traceback: %r", traceback.format_exc())
                click.secho(ex.msg, fg='red')

            except KeyboardInterrupt:
                # user pressed Ctrl + C
                if self.handler.after:
                    click.echo('')
                    for line in self.handler.after():
                        click.echo(line)

                self.refresh_completions()

            except DockerPermissionException as ex:
                self.logger.debug('Permission exception: %r.', ex)
                self.logger.error("traceback: %r", traceback.format_exc())
                click.secho(ex.message, fg='red')

            except EOFError:
                # exit out of the CLI
                break

            # TODO: uncomment for release
            except Exception as ex:
                self.logger.debug('Exception: %r.', ex)
                self.logger.error("traceback: %r", traceback.format_exc())
                click.secho("{0}".format(ex), fg='red')
                break

        self.revert_less_opts()
        self.write_config_file()
        print('Goodbye!')


@click.command()
def cli():
    """
    Create and call the CLI
    """
    try:
        dcli = WharfeeCli()
        dcli.run_cli()
    except DockerTimeoutException as ex:
        click.secho(ex.message, fg='red')
    except DockerSslException as ex:
        click.secho(ex.message, fg='red')

if __name__ == "__main__":
    cli()
