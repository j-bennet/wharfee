from __future__ import unicode_literals


class CommandOption(object):
    """
    Wrapper for the optparse's option that adds some extra fields
    useful to do autocompletion in context of this option.
    """

    TYPE_FILEPATH = 1
    TYPE_DIRPATH = 1
    TYPE_BOOLEAN = 2
    TYPE_NUMERIC = 3
    TYPE_CONTAINER = 4
    TYPE_CONTAINER_RUN = 5
    TYPE_IMAGE = 6
    TYPE_IMAGE_TAG = 7
    TYPE_COMMAND = 8
    TYPE_COMMAND_ARG = 9
    TYPE_CHOICE = 10
    TYPE_KEYVALUE = 11

    def __init__(self, option_type, short_name, long_name=None, **kwargs):
        """
        Constructor for the CommandOption
        :param option_type: int: one the type constants from above
        :param short_name: string: short name to create optparse's Option
        :param long_name: string: long name to create optparse's Option
        :param kwargs: keyword args
        :return:
        """
        if option_type not in [
            CommandOption.TYPE_FILEPATH,
            CommandOption.TYPE_DIRPATH,
            CommandOption.TYPE_BOOLEAN,
            CommandOption.TYPE_NUMERIC,
            CommandOption.TYPE_CONTAINER,
            CommandOption.TYPE_CONTAINER_RUN,
            CommandOption.TYPE_IMAGE,
            CommandOption.TYPE_IMAGE_TAG,
            CommandOption.TYPE_COMMAND,
            CommandOption.TYPE_COMMAND_ARG,
            CommandOption.TYPE_CHOICE,
            CommandOption.TYPE_KEYVALUE
        ]:
            raise ValueError("Incorrect option_type.", option_type)

        if long_name and short_name:
            arguments = [short_name, long_name]
        elif long_name:
            arguments = [long_name]
        else:
            arguments = [short_name]

        if 'api_match' in kwargs and kwargs['api_match'] is not None:
            self.api_match = kwargs['api_match']
            del kwargs['api_match']
        else:
            self.api_match = True

        if 'dest' in kwargs:
            self.dest = kwargs['dest']
        elif long_name:
            self.dest = long_name.strip('-')
        else:
            self.dest = short_name.strip('-')

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
        return self.option_type == CommandOption.TYPE_CHOICE

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
        return self.option_type == CommandOption.TYPE_IMAGE_TAG

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

    @property
    def name(self):
        """
        Getter for short name
        :return: string
        """
        return self.long_name if self.long_name else self.short_name
