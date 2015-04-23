from .option import CommandOption


COMMAND_OPTIONS = {
    'ps': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-h', '--help',
                      action='store_true',
                      dest='help',
                      help='Display help for this command.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-a', '--all',
                      action='store_true',
                      dest='all',
                      help='Show all containers. '
                           'Only running containers are shown by default.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-q', '--quiet',
                      action='store_true',
                      dest='quiet',
                      help='Only display numeric IDs.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-l', '--latest',
                      action='store_true',
                      dest='latest',
                      help='Show only the latest created container, '
                           'include non-running ones.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-s', '--size',
                      action='store_true',
                      dest='latest',
                      help='Display total file sizes.')
    ]
}

