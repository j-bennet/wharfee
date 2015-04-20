
import re
from prompt_toolkit.completion import Completer, Completion


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
        completions = DockerCompleter.find_matches(word_before_cursor, self.all_completions)
        return completions

    @staticmethod
    def find_matches(text, collection):
        """
        Find all matches for the current word
        :param text: word to complete
        :param collection: collection to suggest from
        :return: iterable
        """
        text = DockerCompleter.last_word(text).lower()

        if text:
            for item in sorted(collection):
                if item.startswith(text):
                    yield Completion(item, -len(text))

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