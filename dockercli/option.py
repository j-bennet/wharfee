from __future__ import unicode_literals

from optparse import make_option


class CommandOption(object):
    """
    Wrapper for the optparse's option that adds some extra fields
    useful to do autocompletion in context of this option.
    """

    TYPE_FILEPATH = 1
    TYPE_BOOLEAN = 2
    TYPE_NUMERIC = 3
    TYPE_CONTAINER = 4
    TYPE_IMAGE = 5

    def __init__(self, option_type, short_name, long_name=None, **kwargs):
        """
        Constructor for the CommandOption
        :param option_type: int: one the type constants from above
        :param short_name: string: short name to create optparse's Option
        :param long_name: string: long name to create optparse's Option
        :param kwargs: keyword args to create optparse's Option
        :return:
        """
        if option_type not in [
            CommandOption.TYPE_FILEPATH,
            CommandOption.TYPE_BOOLEAN,
            CommandOption.TYPE_NUMERIC,
            CommandOption.TYPE_CONTAINER,
            CommandOption.TYPE_IMAGE
        ]:
            raise ValueError("Incorrect option_type.", option_type)

        if long_name and short_name:
            arguments = [short_name, long_name]
        elif long_name:
            arguments = [long_name]
        else:
            arguments = [short_name]

        self.option_type = option_type
        self.short_name = short_name
        self.long_name = long_name
        self.option = make_option(*arguments, **kwargs)

    def get_option(self):
        """
        Getter for optparse's Option
        :return: Option
        """
        return self.option

    def is_type_container(self):
        """
        Should this option suggest container name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_CONTAINER

    def is_type_image(self):
        """
        Should this option suggest image name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_IMAGE

    @property
    def name(self):
        """
        Getter for short name
        :return: string
        """
        return self.long_name if self.long_name else self.short_name
