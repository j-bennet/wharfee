
import re
from prompt_toolkit.completion import Completer, Completion
from .options import COMMAND_OPTIONS


class DockerCompleter(Completer):
    """
    Completer for Docker commands and parameters.
    """

    commands = [
        'help',
        'version',
        'ps',
        'images',
        'run',
        'stop'
    ]

    RE_WHITESPACE = re.compile('\s+')

    def __init__(self):
        """
        Initialize the completer
        :return:
        """
        self.all_completions = set(self.commands)

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
        first_word = DockerCompleter.first_word(document.text).lower()
        word_count = DockerCompleter.get_word_count(document.text)

        in_command = (word_count > 1) or \
                     ((not word_before_cursor) and first_word)

        if in_command:
            completions = DockerCompleter.find_command_matches(
                first_word,
                word_before_cursor)
        else:
            completions = DockerCompleter.find_matches(
                word_before_cursor,
                self.all_completions)

        return completions

    @staticmethod
    def find_command_matches(command, word=''):
        """
        Find all matches in context of the given command.
        :param command: string: command keyword (such as "ps", "images")
        :param word: string: word currently being typed
        :return: iterable
        """
        if command in COMMAND_OPTIONS:
            for opt in COMMAND_OPTIONS[command]:
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
        text = DockerCompleter.last_word(text).lower()

        for item in sorted(collection):
            if item.startswith(text) or (not text):
                yield Completion(item, -len(text))

    @staticmethod
    def get_word_count(text):
        """
        Find count of words.
        :param text:
        :return: int
        """
        if text is not None:
            text = text.strip()
            words = re.split('\s+', text)
            return len(words)
        return 0

    @staticmethod
    def first_word(text):
        """
        Find first word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            word = re.split('\s+', text)[0]
            word = word.strip()
            return word
        return ''

    @staticmethod
    def last_word(text):
        """
        Find last word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            word = re.split('\s+', text)[-1]
            word = word.strip()
            return word
        return ''