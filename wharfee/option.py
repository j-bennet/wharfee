# -*- coding: utf-8
from __future__ import unicode_literals


class CommandOption(object):
    """
    Wrapper for the optparse's option that adds some extra fields
    useful to do autocompletion in context of this option.
    """

    choices = None

    OPTION_VALUES = range(18)

    TYPE_FILEPATH, \
        TYPE_DIRPATH, \
        TYPE_BOOLEAN, \
        TYPE_NUMERIC, \
        TYPE_CONTAINER, \
        TYPE_CONTAINER_RUN, \
        TYPE_IMAGE, \
        TYPE_IMAGE_TAGGED, \
        TYPE_IMAGE_TAG, \
        TYPE_COMMAND, \
        TYPE_COMMAND_ARG, \
        TYPE_CHOICE, \
        TYPE_KEYVALUE, \
        TYPE_PORT_BINDING, \
        TYPE_PORT_RANGE, \
        TYPE_OBJECT, \
        TYPE_STRING,\
        TYPE_VOLUME = \
        OPTION_VALUES

    def __init__(self, option_type, short_name, long_name=None, **kwargs):
        """
        Constructor for the CommandOption
        :param option_type: int: one the type constants from above
        :param short_name: string: short name to create optparse's Option
        :param long_name: string: long name to create optparse's Option
        :param kwargs: keyword args
        :return:
        """
        if option_type not in self.OPTION_VALUES:
            raise ValueError("Incorrect option_type.", option_type)

        if long_name and short_name:
            arguments = [short_name, long_name]
            self.display = '{0}/{1}'.format(short_name, long_name)
        elif long_name:
            arguments = [long_name]
            self.display = long_name
        else:
            arguments = [short_name]
            self.display = short_name

        if 'api_match' in kwargs and kwargs['api_match'] is not None:
            self.api_match = kwargs['api_match']
            del kwargs['api_match']
        else:
            self.api_match = True

        if 'cli_match' in kwargs and kwargs['cli_match'] is not None:
            self.cli_match = kwargs['cli_match']
            del kwargs['cli_match']
        else:
            self.cli_match = True

        if 'dest' in kwargs:
            self.dest = kwargs['dest']
        elif long_name:
            self.dest = long_name.strip('-')
        else:
            self.dest = short_name.strip('-')

        self.default = kwargs['default'] if 'default' in kwargs else None

        if 'nargs' in kwargs:
            self.is_optional = (kwargs['nargs'] in ['?', '*'])
            self.is_multiple = (kwargs['nargs'] in ['+', '*'])

            # TODO: Optparse wants a number here... back to argparse?
            if kwargs['nargs'] in ['?', '*', '+']:
                if kwargs['nargs'] in ['*', '+']:
                    kwargs['action'] = 'append'
                del kwargs['nargs']

        else:
            self.is_optional = False
            self.is_multiple = False

        if 'choices' in kwargs:
            self.choices = kwargs['choices']
            if option_type != CommandOption.TYPE_CHOICE:
                kwargs.pop('choices')

        self.option_type = option_type
        self.short_name = short_name
        self.long_name = long_name
        self.args = arguments
        self.kwargs = kwargs

    def is_type_choice(self):
        """
        If this option is a list of choices.
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_CHOICE or self.choices

    def is_type_container(self):
        """
        Should this option suggest container name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_CONTAINER

    def is_type_running(self):
        """
        Should this option suggest running container name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_CONTAINER_RUN

    def is_type_image(self):
        """
        Should this option suggest image name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_IMAGE

    def is_type_tagged(self):
        """
        Should this option suggest tagged image name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_IMAGE_TAGGED

    def is_type_volume(self):
        """
        Should this option suggest volume name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_VOLUME

    def is_type_filepath(self):
        """
        Should this option suggest filename?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_FILEPATH

    def is_type_dirname(self):
        """
        Should this option suggest directory name?
        :return: boolean
        """
        return self.option_type == CommandOption.TYPE_DIRPATH

    def get_name(self, is_long):
        """
        Return short name if we have one, and is requested. Otherwise default
        to long name.
        :param is_long: boolean
        :return: string
        """
        if is_long:
            return self.long_name if self.long_name else self.short_name
        return self.short_name if self.short_name else self.long_name

    def is_match(self, word):
        """
        Can this option be suggested having this word being typed?
        :param word:
        :return:
        """
        if word:
            return (self.long_name and self.long_name.startswith(word)) or \
                   (self.short_name and self.short_name.startswith(word))
        return True

    @property
    def name(self):
        """
        Getter for short name
        :return: string
        """
        return self.long_name if self.long_name else self.short_name

    @property
    def names(self):
        """
        Getter for all possible names.
        :return: list
        """
        if self.short_name and self.long_name:
            return [self.short_name, self.long_name]
        elif self.long_name:
            return [self.long_name]
        else:
            return [self.short_name]

    def __repr__(self):
        """
        Return the printable representation.
        """
        return 'CommandOption({0}, {1}'.format(
            self.short_name,
            self.long_name)
