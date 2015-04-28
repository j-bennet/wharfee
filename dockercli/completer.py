from __future__ import unicode_literals

from prompt_toolkit.completion import Completer, Completion
from .options import COMMAND_OPTIONS
from .options import COMMAND_NAMES
from .options import find_option


class DockerCompleter(Completer):
    """
    Completer for Docker commands and parameters.
    """

    def __init__(self, containers=None, images=None):
        """
        Initialize the completer
        :return:
        """
        self.all_completions = set(COMMAND_NAMES)
        self.containers = set(containers) if containers else set()
        self.images = set(images) if images else set()

    def set_containers(self, containers):
        """
        Setter for list of available containers.
        :param containers: list
        """
        self.containers = set(containers) if containers else set()

    def set_images(self, images):
        """
        Setter for list of available images.
        :param images: list
        """
        self.images = set(images) if images else set()

    def get_completions(self, document, complete_event):
        """
        Get completions for the current scope.
        :param document:
        :param complete_event:
        :param smart_completion:
        """

        # Unused parameters.
        _ = complete_event

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
                self.images)
        else:
            completions = DockerCompleter.find_matches(
                word_before_cursor,
                self.all_completions)

        return completions

    @staticmethod
    def find_command_matches(command, word='', prev='', params=None, containers=None, images=None):
        """
        Find all matches in context of the given command.
        :param command: string: command keyword (such as "ps", "images")
        :param word: string: word currently being typed
        :param prev: string: previous word
        :param params: list of command parameters
        :param containers: list of containers
        :param images: list of images
        :return: iterable
        """

        params = set(params) if params else set([])
        current_opt = find_option(command, prev) if prev else None

        if command in COMMAND_OPTIONS:
            if current_opt and current_opt.is_type_container():
                for container_name in containers:
                    if container_name.startswith(word) or not word:
                        yield Completion(container_name, -len(word))
            else:
                for opt in COMMAND_OPTIONS[command]:
                    # Do not offer options that user already set.
                    if opt.name not in params:
                        if opt.name.startswith(word) or not word:
                            yield Completion(opt.name, -len(word))

    @staticmethod
    def find_matches(text, collection):
        """
        Find all matches for the current word
        :param text: word to complete
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
        :return: int
        """
        if text is not None:
            text = text.strip()
            words = text.split()
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
                word = text.split()[0]
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
                word = text.split()[-1]
                word = word.strip()
                return word
        return ''