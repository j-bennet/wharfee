# -*- coding: utf-8
from __future__ import unicode_literals

import fuzzyfinder

from itertools import chain
from prompt_toolkit.completion import Completer, Completion
from .options import COMMAND_OPTIONS, COMMAND_NAMES, all_options, find_option, \
    split_command_and_args
from .helpers import list_dir, parse_path, complete_path
from .utils import shlex_split, shlex_first_token


class DockerCompleter(Completer):
    """
    Completer for Docker commands and parameters.
    """

    def __init__(self, containers=None, running=None, images=None, tagged=None,
                 volumes=None, long_option_names=True, fuzzy=False):
        """
        Initialize the completer
        :return:
        """
        self.all_completions = set(COMMAND_NAMES)
        self.containers = set(containers) if containers else set()
        self.running = set(running) if running else set()
        self.images = set(images) if images else set()
        self.tagged = set(tagged) if tagged else set()
        self.volumes = set(volumes) if volumes else set()
        self.long_option_mode = long_option_names
        self.fuzzy = fuzzy

    def set_volumes(self, volumes):
        """
        Setter for list of available volumes.
        :param volumes: list
        """
        self.volumes = set(volumes) if volumes else set()

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

    def set_long_options(self, is_long):
        """
        Setter for long option names.
        :param is_long: boolean
        """
        self.long_option_mode = is_long

    def get_long_options(self):
        """
        Getter for long option names.
        """
        return self.long_option_mode

    def set_fuzzy_match(self, is_fuzzy):
        """
        Setter for fuzzy match option.
        :param is_fuzzy: boolean
        """
        self.fuzzy = is_fuzzy

    def get_fuzzy_match(self):
        """
        Getter for fuzzy match option.
        :return: boolean
        """
        return self.fuzzy

    def get_completions(self, document, _):
        """
        Get completions for the current scope.
        :param document:
        :param _: complete_event
        """

        # Unused parameters.

        if DockerCompleter.in_quoted_string(document.text):
            return []

        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = DockerCompleter.get_tokens(document.text)
        command_name = split_command_and_args(words)[0]

        in_command = (len(words) > 1) or \
                     ((not word_before_cursor) and command_name)

        if in_command:
            previous_word = ''
            previous_start = document.find_start_of_previous_word(WORD=True)

            if previous_start == -len(word_before_cursor):
                previous_start = document.find_start_of_previous_word(
                    WORD=True, count=2)

            if previous_start:
                previous_word = document.text_before_cursor[previous_start:]
                previous_word = previous_word.strip().split()[0]

            params = words[1:] if (len(words) > 1) else []
            completions = DockerCompleter.find_command_matches(
                command_name,
                word_before_cursor,
                previous_word,
                params,
                self.containers,
                self.running,
                self.images,
                self.tagged,
                self.volumes,
                self.long_option_mode,
                self.fuzzy)
        else:
            completions = DockerCompleter.find_matches(
                word_before_cursor,
                self.all_completions,
                self.fuzzy)

        return completions

    @staticmethod
    def find_command_matches(command, word='', prev='', params=None,
                             containers=None, running=None, images=None,
                             tagged=None, volumes=None, long_options=True,
                             fuzzy=False):
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
        :param volumes: list of volumes
        :param long_options: boolean
        :param fuzzy: boolean
        :return: iterable
        """

        params = set(params) if params else set([])
        current_opt = find_option(command, prev) if prev else None

        add_directory = False
        add_filepath = False

        if command in COMMAND_OPTIONS:
            opt_suggestions = []
            if current_opt:
                if current_opt.is_type_container():
                    opt_suggestions = containers
                elif current_opt.is_type_running():
                    opt_suggestions = running
                elif current_opt.is_type_image():
                    opt_suggestions = images
                elif current_opt.is_type_tagged():
                    opt_suggestions = tagged
                elif current_opt.is_type_volume():
                    opt_suggestions = volumes
                elif current_opt.is_type_choice():
                    opt_suggestions = current_opt.choices
                elif current_opt.is_type_dirname():
                    add_directory = True
                elif current_opt.is_type_filepath():
                    add_filepath = True

                for m in DockerCompleter.find_collection_matches(
                        word, opt_suggestions, fuzzy):
                    yield m

            if not opt_suggestions:

                def is_unused(o):
                    """
                    Do not offer options that user already set.
                    Unless user may want to set them multiple times.
                    Example: -e VAR1=value1 -e VAR2=value2.
                    """
                    return o.long_name not in params and o.short_name not in params

                def is_current(o):
                    return word in o.names

                def get_opt_name(t):
                    return t.get_name(long_options)

                positionals = []
                possible_options = [x for x in all_options(command) if is_unused(x)
                                    or is_current(x)
                                    or x.is_multiple]
                named_options = sorted([x for x in possible_options if x.name.startswith('-')],
                                       key=get_opt_name)
                positional_options = [x for x in possible_options if not x.name.startswith('-')]

                named_option_map = {}

                for x in named_options:
                    suggestion = x.get_name(long_options)
                    if suggestion:
                        named_option_map[suggestion] = x.display

                for m in DockerCompleter.find_dictionary_matches(
                        word, named_option_map, fuzzy):
                    yield m

                for opt in positional_options:
                    if opt.is_type_container():
                        positionals = chain(positionals, containers)
                    elif opt.is_type_image():
                        positionals = chain(positionals, images)
                    elif opt.is_type_running():
                        positionals = chain(positionals, running)
                    elif opt.is_type_tagged():
                        positionals = chain(positionals, tagged)
                    elif opt.is_type_volume():
                        positionals = chain(positionals, volumes)
                    elif opt.is_type_choice():
                        positionals = chain(positionals, opt.choices)
                    elif opt.is_type_dirname():
                        add_directory = True
                    elif opt.is_type_filepath():
                        add_filepath = True

                # Also return completions for positional options (images,
                # containers, etc.)
                for m in DockerCompleter.find_collection_matches(
                        word, positionals, fuzzy):
                    yield m

        # Special handling for path completion
        if add_directory:
            for m in DockerCompleter.find_directory_matches(word):
                yield m
        if add_filepath:
            for m in DockerCompleter.find_filepath_matches(word):
                yield m

    @staticmethod
    def find_filepath_matches(word):
        """
        Yield matching directory or file names.
        :param word:
        :return: iterable
        """
        base_path, last_path, position = parse_path(word)
        paths = list_dir(word, dirs_only=False)
        for name in sorted(paths):
            suggestion = complete_path(name, last_path)
            if suggestion:
                yield Completion(suggestion, position)

    @staticmethod
    def find_directory_matches(word):
        """
        Yield matching directory names.
        :param word:
        :return: iterable
        """
        base_dir, last_dir, position = parse_path(word)
        dirs = list_dir(word, dirs_only=True)
        for name in sorted(dirs):
            suggestion = complete_path(name, last_dir)
            if suggestion:
                yield Completion(suggestion, position)

    @staticmethod
    def find_dictionary_matches(word, dic, fuzzy):
        """
        Yield all matching names in dict
        :param dic: dict mapping name to display name
        :param word: string user typed
        :param fuzzy: boolean
        :return: iterable
        """

        if fuzzy:
            for suggestion in fuzzyfinder.fuzzyfinder(word, dic.keys()):
                yield Completion(suggestion, -len(word), dic[suggestion])
        else:
            for name in sorted(dic.keys()):
                if name.startswith(word) or not word:
                    yield Completion(name, -len(word), dic[name])

    @staticmethod
    def find_collection_matches(word, lst, fuzzy):
        """
        Yield all matching names in list
        :param lst: collection
        :param word: string user typed
        :param fuzzy: boolean
        :return: iterable
        """

        if fuzzy:
            for suggestion in fuzzyfinder.fuzzyfinder(word, lst):
                yield Completion(suggestion, -len(word))
        else:
            for name in sorted(lst):
                if name.startswith(word) or not word:
                    yield Completion(name, -len(word))

    @staticmethod
    def find_matches(text, collection, fuzzy):
        """
        Find all matches for the current text
        :param text: text before cursor
        :param collection: collection to suggest from
        :param fuzzy: boolean
        :return: iterable
        """
        text = DockerCompleter.last_token(text).lower()

        for suggestion in DockerCompleter.find_collection_matches(
                text, collection, fuzzy):
            yield suggestion

    @staticmethod
    def get_tokens(text):
        """
        Parse out all tokens.
        :param text:
        :return: list
        """
        if text is not None:
            text = text.strip()
            words = DockerCompleter.safe_split(text)
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
                try:
                    word = shlex_first_token(text)
                    word = word.strip()
                    return word
                except:
                    # no error, just do not complete
                    pass
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
                word = DockerCompleter.safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    @staticmethod
    def safe_split(text):
        """
        Shlex can't always split. For example, "\" crashes the completer.
        """
        try:
            words = shlex_split(text)
            return words
        except:
            return text

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
