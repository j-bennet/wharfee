from __future__ import unicode_literals

import os
import shlex

from itertools import chain
from prompt_toolkit.completion import Completer, Completion
from .options import COMMAND_OPTIONS
from .options import COMMAND_NAMES
from .options import all_options
from .options import find_option


class DockerCompleter(Completer):
    """
    Completer for Docker commands and parameters.
    """

    def __init__(self, containers=None, running=None, images=None, tagged=None):
        """
        Initialize the completer
        :return:
        """
        self.all_completions = set(COMMAND_NAMES)
        self.containers = set(containers) if containers else set()
        self.running = set(running) if running else set()
        self.images = set(images) if images else set()
        self.tagged = set(tagged) if tagged else set()

    def set_containers(self, containers):
        """
        Setter for list of available containers.
        :param containers: list
        """
        self.containers = set(containers) if containers else set()

    def set_running(self, containers):
        """
        Setter for list of running containers.
        :param containers: list
        """
        self.running = set(containers) if containers else set()

    def set_images(self, images):
        """
        Setter for list of available images.
        :param images: list
        """
        self.images = set(images) if images else set()

    def set_tagged(self, images):
        """
        Setter for list of tagged images.
        :param images: list
        """
        self.tagged = set(images) if images else set()

    def get_completions(self, document, complete_event):
        """
        Get completions for the current scope.
        :param document:
        :param complete_event:
        :param smart_completion:
        """

        # Unused parameters.
        _ = complete_event

        if DockerCompleter.in_quoted_string(document.text):
            return []

        word_before_cursor = document.get_word_before_cursor(WORD=True)
        first_word = DockerCompleter.first_token(document.text).lower()
        words = DockerCompleter.get_tokens(document.text)

        in_command = (len(words) > 1) or \
                     ((not word_before_cursor) and first_word)

        if in_command:
            previous_word = ''
            previous_start = document.find_start_of_previous_word(WORD=True)

            if previous_start == -len(word_before_cursor):
                previous_start = document.find_start_of_previous_word(WORD=True, count=2)

            if previous_start:
                previous_word = document.text_before_cursor[previous_start:]
                previous_word = previous_word.strip().split()[0]

            params = words[1:] if (len(words) > 1) else []
            completions = DockerCompleter.find_command_matches(
                first_word,
                word_before_cursor,
                previous_word,
                params,
                self.containers,
                self.running,
                self.images,
                self.tagged)
        else:
            completions = DockerCompleter.find_matches(
                word_before_cursor,
                self.all_completions)

        return completions

    @staticmethod
    def find_command_matches(command, word='', prev='', params=None,
                             containers=None, running=None, images=None,
                             tagged=None):
        """
        Find all matches in context of the given command.
        :param command: string: command keyword (such as "ps", "images")
        :param word: string: word currently being typed
        :param prev: string: previous word
        :param params: list of command parameters
        :param containers: list of containers
        :param running: list of running containers
        :param images: list of images
        :param tagged: list of tagged images
        :return: iterable
        """

        params = set(params) if params else set([])
        current_opt = find_option(command, prev) if prev else None

        add_directory = False

        if command in COMMAND_OPTIONS:
            if current_opt:
                opt_suggestions = []
                if current_opt.is_type_container():
                    opt_suggestions = containers
                elif current_opt.is_type_running():
                    opt_suggestions = running
                elif current_opt.is_type_image():
                    opt_suggestions = images
                elif current_opt.is_type_tagged():
                    opt_suggestions = tagged
                elif current_opt.is_type_choice():
                    opt_suggestions = current_opt.choices
                for m in DockerCompleter.find_collection_matches(
                        word, opt_suggestions):
                    yield m
            else:
                positionals = []
                for opt in all_options(command):

                    # Do not offer options that user already set.
                    # Unless user may want to set them multiple times.
                    # Example: -e VAR1=value1 -e VAR2=value2.
                    if opt.name not in params or opt.is_multiple:
                        if opt.name.startswith('-'):
                            if opt.name.startswith(word) or not word:
                                yield Completion(opt.name, -len(word))
                        else:
                            # positional option
                            if opt.is_type_container():
                                positionals = chain(positionals, containers)
                            elif opt.is_type_image():
                                positionals = chain(positionals, images)
                            elif opt.is_type_running():
                                positionals = chain(positionals, running)
                            elif opt.is_type_tagged():
                                positionals = chain(positionals, tagged)
                            elif opt.is_type_choice():
                                positionals = chain(positionals, opt.choices)
                            elif opt.is_type_dirname():
                                add_directory = True

                # Also return completions for positional options (images,
                # containers, etc.)
                for m in DockerCompleter.find_collection_matches(
                        word, positionals):
                    yield m
                # Special handling for path completion
                if add_directory:
                    for m in DockerCompleter.find_directory_matches(word):
                        yield m

    @staticmethod
    def find_directory_matches(word):
        """
        Yield matching directory names
        :param word:
        :return: iterable
        """
        basedir, lastdir, position = '', '', 0
        if word:
            basedir, lastdir = os.path.split(word)
            position = -len(lastdir) if lastdir else 0

        dirs = DockerCompleter.list_dir(word, True)
        for name in sorted(dirs):
            if not lastdir or name.startswith(lastdir):
                yield Completion(name, position)
            elif lastdir == '~':
                yield Completion(os.path.join(lastdir, name), position)

    @staticmethod
    def list_dir(root, dirs_only=False, include_special=False):
        """
        List directory.
        :param root: string: directory to list
        :param dirs_only: boolean
        :param include_special: boolean
        :return: list
        """
        root = '.' if not root else root
        res = []

        if '~' in root:
            root = os.path.expanduser(root)

        if not os.path.exists(root):
            root, _ = os.path.split(root)

        if os.path.exists(root):
            for name in os.listdir(root):
                path = os.path.join(root, name)
                if not include_special and name.startswith('.'):
                    continue
                if dirs_only and not os.path.isdir(path):
                    continue
                res.append(name)
        return res

    @staticmethod
    def find_collection_matches(word, lst):
        """
        Yield all matching names in list
        :param lst:
        :param word:
        :return:
        """
        for name in sorted(lst):
            if name.startswith(word) or not word:
                yield Completion(name, -len(word))

    @staticmethod
    def find_matches(text, collection):
        """
        Find all matches for the current text
        :param text: text before cursor
        :param collection: collection to suggest from
        :return: iterable
        """
        text = DockerCompleter.last_token(text).lower()

        for item in sorted(collection):
            if item.startswith(text) or (not text):
                yield Completion(item, -len(text))

    @staticmethod
    def get_tokens(text):
        """
        Parse out all tokens.
        :param text:
        :return: list
        """
        if text is not None:
            text = text.strip()
            words = shlex.split(text)
            return words
        return []

    @staticmethod
    def first_token(text):
        """
        Find first word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                lexer = shlex.shlex(text)
                word = lexer.get_token()
                word = word.strip()
                return word
        return ''

    @staticmethod
    def last_token(text):
        """
        Find last word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = shlex.split(text)[-1]
                word = word.strip()
                return word
        return ''

    @staticmethod
    def in_quoted_string(text):
        """
        Find last word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0 and ('"' in text or "'" in text):
                stack = []
                for char in text:
                    if char in ['"', "'"]:
                        if len(stack) > 0 and stack[-1] == char:
                            stack = stack[:-1]
                        else:
                            stack.append(char)
                return len(stack) > 0
        return False
