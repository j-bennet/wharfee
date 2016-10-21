# -*- coding: utf-8
from __future__ import unicode_literals

from optparse import OptionParser, OptionError, OptionGroup
from .option import CommandOption

COMMAND_NAMES = [
    'attach',
    'build',
    'clear',
    'create',
    'exec',
    'help',
    'images',
    'info',
    'inspect',
    'kill',
    'login',
    'logs',
    'ps',
    'pull',
    'pause',
    'port',
    'push',
    'refresh',
    'restart',
    'run',
    'rm',
    'rmi',
    'search',
    'shell',
    'start',
    'stop',
    'tag',
    'top',
    'unpause',
    'version',
    'volume create',
    'volume inspect',
    'volume ls',
    'volume rm',
]


COMMAND_LENGTH = dict((k, len(k.split(' '))) for k in COMMAND_NAMES if ' ' in k)


OPTION_HELP = CommandOption(
    CommandOption.TYPE_BOOLEAN, '-h', '--help',
    action='store_true',
    dest='help',
    help='Display help for this command.')

OPTION_ATTACH_CHOICE = CommandOption(
    CommandOption.TYPE_CHOICE, '-a', '--attach',
    action='append',
    dest='attach',
    help='Attach to STDIN, STDOUT, or STDERR (can use multiple times).',
    nargs='*',
    choices=['stdin', 'stdout', 'stderr'],
    api_match=False)

OPTION_ATTACH_BOOLEAN = CommandOption(
    CommandOption.TYPE_BOOLEAN, '-a', '--attach',
    action='store_true',
    dest='attach',
    help='Attach container\'s STDOUT and STDERR and ' +
         'forward all signals to the process.',
    api_match=False)

OPTION_ENV = CommandOption(
    CommandOption.TYPE_KEYVALUE, '-e', '--env',
    action='append',
    dest='environment',
    help='Set environment variables.',
    nargs='*')

OPTION_EXPOSE = CommandOption(
    CommandOption.TYPE_PORT_RANGE, None, '--expose',
    action='append',
    dest='expose',
    help=('Expose a port or a range of ports (e.g. '
          '--expose=3300-3310) from the container without '
          'publishing it to your host.'),
    nargs='*',
    api_match=False)

OPTION_CONTAINER_HOSTNAME = CommandOption(
    CommandOption.TYPE_STRING, '-h', '--hostname',
    action='store',
    dest='hostname',
    help='Container host name.')

OPTION_CONTAINER_NAME = CommandOption(
    CommandOption.TYPE_CONTAINER, None, '--name',
    action='store',
    dest='name',
    help='Specify volume name.')

OPTION_VOLUME_NAME = CommandOption(
    CommandOption.TYPE_VOLUME, None, '--name',
    action='store',
    dest='name',
    help='Assign a name to the container.')

OPTION_VOLUME_NAME_POS = CommandOption(
    CommandOption.TYPE_VOLUME, 'name',
    help='Volume name.',
    nargs='+')

OPTION_LINK = CommandOption(
    CommandOption.TYPE_CONTAINER, None, '--link',
    action='append',
    dest='links',
    help=('Add link to another container in the form of '
          '<name|id>:alias. To add multiple links: --link '
          'name1:alias1 --link name2:alias2...'),
    nargs='*',
    api_match=False)

OPTION_PUBLISH_ALL = CommandOption(
    CommandOption.TYPE_BOOLEAN, '-P', '--publish-all',
    action='store_true',
    dest='publish_all_ports',
    help=('Publish all exposed ports to the host '
          'interfaces.'),
    api_match=False)

OPTION_PUBLISH = CommandOption(
    CommandOption.TYPE_PORT_BINDING, '-p', '--publish',
    action='append',
    dest='port_bindings',
    help=('Publish a container\'s port to the host. '
          'Format: ip:hostPort:containerPort or '
          'ip::containerPort or hostPort:containerPort or '
          'containerPort. To add multiple ports: --publish '
          '1111:2222 --publish 3333:4444...'),
    nargs='*',
    api_match=False)

OPTION_INTERACTIVE = CommandOption(
    CommandOption.TYPE_BOOLEAN, '-i', '--interactive',
    action='store_true',
    dest='interactive',
    default=False,
    help='Keep STDIN open even if not attached.',
    api_match=False)

OPTION_TTY = CommandOption(
    CommandOption.TYPE_BOOLEAN, '-t', '--tty',
    action='store_true',
    dest='tty',
    default=False,
    help='Allocate a pseudo-TTY.')

OPTION_RM = CommandOption(
    CommandOption.TYPE_BOOLEAN, None, '--rm',
    action='store_true',
    dest='remove',
    help=('Remove the container when it exits. '
          'Can\'t be used with --detach'),
    api_match=False)

OPTION_VOLUME = CommandOption(
    CommandOption.TYPE_FILEPATH, '-v', '--volume',
    action='append',
    dest='volumes',
    help=('Bind mount a volume (e.g., from the host: -v '
          '/host-path:/container-path, from Docker: '
          '-v /container-path).'),
    nargs='*')

OPTION_VOLUMES_FROM = CommandOption(
    CommandOption.TYPE_CONTAINER, None, '--volumes-from',
    action='append',
    dest='volumes_from',
    help=('Mount volumes from the specified containers. Can '
          'be specified multiple times. Alternatively, can '
          'accept a comma-separated string of container '
          'names.'),
    nargs='*',
    api_match=False)

OPTION_NET = CommandOption(
    CommandOption.TYPE_STRING, None, '--net',
    action='store',
    dest='net',
    help='Network mode for the container. Possible values are "bridge", '
         '"none", "container:<name|id>", "host".',
    choices=['bridge', 'none', 'container:', 'host'],
    api_match=False)

OPTION_FILTERS = CommandOption(
    CommandOption.TYPE_STRING, None, '--filter',
    action='append',
    dest='filters',
    nargs='+',
    help='Provide filter values (i.e. "dangling=true").')

OPTION_OPT = CommandOption(
    CommandOption.TYPE_STRING, '-o', '--opt',
    action='append',
    dest='driver_opts',
    nargs='+',
    help='Set driver specific options (e.g. "tardis=blue").')

OPTION_DRIVER = CommandOption(
    CommandOption.TYPE_STRING, '-d', '--driver',
    action='store',
    help='Specify volume driver name (--driver local).')

OPTION_IMAGE = CommandOption(
    CommandOption.TYPE_IMAGE, None, 'image',
    action='store',
    help='Image ID or name to use.')

OPTION_CMD = CommandOption(
    CommandOption.TYPE_COMMAND, None, 'cmd',
    action='store',
    help='Command to run in a container.',
    nargs='?')

OPTION_COMMAND = CommandOption(
    CommandOption.TYPE_COMMAND, None, 'command',
    action='store',
    help='Command to run in a container.',
    nargs='?')

OPTION_STDIN_OPEN = CommandOption(
    CommandOption.TYPE_BOOLEAN, None, 'stdin_open',
    action='store',
    dest='stdin_open',
    default=False)

OPTION_CONTAINER = CommandOption(
    CommandOption.TYPE_CONTAINER, None, 'container',
    action='store',
    help='Container ID or name to use.')

OPTION_CONTAINER_RUNNING = CommandOption(
    CommandOption.TYPE_CONTAINER_RUN, None, 'container',
    action='store',
    help='Container ID or name to use.')

OPTION_HOST_CONFIG = CommandOption(
    CommandOption.TYPE_OBJECT, None, 'host_config',
    action='store',
    dest='host_config')

OPTION_PORTS = CommandOption(
    CommandOption.TYPE_NUMERIC, None, 'ports',
    action='append',
    dest='ports',
    nargs='*')


COMMAND_OPTIONS = {
    'attach': [
        CommandOption(CommandOption.TYPE_BOOLEAN, None, '--no-stdin',
                      action='store_true',
                      dest='no_stdin',
                      help='Do not attach STDIN.',
                      default=False,
                      api_match=False),
        CommandOption(CommandOption.TYPE_CHOICE, None, '--sig-proxy',
                      action='store',
                      dest='sig_proxy',
                      help='Proxy all received signals to the process.',
                      default=True,
                      api_match=False,
                      choices=['true', 'false']),
        OPTION_CONTAINER_RUNNING,
        CommandOption(CommandOption.TYPE_STRING, None, '--detach-keys',
                      action='store',
                      dest='detach_keys',
                      help='Override the key sequence for detaching a container.',
                      api_match=False),
    ],
    'build': [
        CommandOption(CommandOption.TYPE_IMAGE, '-t', '--tag',
                      dest='tag',
                      help=('Repository name (and optionally a tag) to be '
                            'applied to the resulting image in case of '
                            'success.')),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-q', '--quiet',
                      action='store_true',
                      dest='quiet',
                      help=('Suppress the verbose output generated by the '
                            'containers.')),
        CommandOption(CommandOption.TYPE_CHOICE, '--rm',
                      action='store',
                      dest='rm',
                      help=('Remove intermediate containers after a '
                            'successful build.'),
                      default='true',
                      choices=['true', 'false']),
        CommandOption(CommandOption.TYPE_BOOLEAN, '--no-cache',
                      action='store_true',
                      dest='nocache',
                      help='Do not use cache when building the image.'),
        CommandOption(CommandOption.TYPE_DIRPATH, 'path',
                      help='Path or URL where the Dockerfile is located.'),
    ],
    'clear': [],
    'create': [
        OPTION_ATTACH_CHOICE,
        OPTION_ENV,
        OPTION_EXPOSE,
        OPTION_INTERACTIVE,
        OPTION_LINK,
        OPTION_CONTAINER_HOSTNAME,
        OPTION_CONTAINER_NAME,
        OPTION_PUBLISH_ALL,
        OPTION_PUBLISH,
        OPTION_TTY,
        OPTION_VOLUME,
        OPTION_VOLUMES_FROM,
        OPTION_IMAGE,
        OPTION_COMMAND,
        OPTION_NET,
    ],
    'exec': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-d', '--detach',
                      action='store_true',
                      dest='detach',
                      help='Detached mode: run command in the background.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-i', '--interactive',
                      action='store_true',
                      dest='interactive',
                      default=False,
                      help='Keep STDIN open even if not attached.',
                      api_match=False),
        OPTION_TTY,
        OPTION_CONTAINER_RUNNING,
        OPTION_CMD,
    ],
    'info': [
    ],
    'inspect': [
        CommandOption(CommandOption.TYPE_IMAGE, 'image',
                      action='store',
                      dest="image_id",
                      help='Image to inspect.',
                      nargs='*'),
        CommandOption(CommandOption.TYPE_CONTAINER, 'container',
                      action='store',
                      help='Container to inspect.',
                      nargs='*'),
    ],
    'kill': [
        CommandOption(CommandOption.TYPE_CHOICE, '-s', '--signal',
                      action='store',
                      dest='signal',
                      help=('Signal to send to the container'),
                      default='KILL',
                      choices=['ABRT', 'ALRM', 'BUS', 'CLD', 'CONT', 'FPE',
                               'HUP', 'ILL', 'INT', 'KILL', 'PIPE', 'POLL',
                               'PROF', 'PWR', 'QUIT', 'RTMAX', 'RTMIN', 'SEGV',
                               'STOP', 'SYS', 'TERM', 'TRAP', 'TSTP', 'TTIN',
                               'TTOU', 'URG', 'USR1', 'USR2', 'VTALRM',
                               'WINCH', 'XCPU', 'XFSZ']),
        OPTION_CONTAINER_RUNNING,
    ],
    'login': [
        CommandOption(CommandOption.TYPE_STRING, '-e', '--email',
                      help='Email.'),
        CommandOption(CommandOption.TYPE_STRING, '-p', '--password',
                      help='Password.'),
        CommandOption(CommandOption.TYPE_STRING, '-u', '--username',
                      help='Username.'),
        CommandOption(CommandOption.TYPE_STRING, None, 'server',
                      dest='registry',
                      help='Registry server.'),
    ],
    'logs': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-f', '--follow',
                      action='store_true',
                      dest='stream',
                      help='Follow log output.'),
        OPTION_CONTAINER,
    ],
    'pause': [
        OPTION_CONTAINER_RUNNING,
    ],
    'port': [
        OPTION_CONTAINER,
        CommandOption(CommandOption.TYPE_STRING, None, 'port',
                      action='store',
                      dest='port',
                      help='Port number (optionally with protocol).'),
    ],
    'ps': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-a', '--all',
                      action='store_true',
                      dest='all',
                      help='Show all containers. '
                           'Only running containers are shown by default.'),
        CommandOption(CommandOption.TYPE_CONTAINER, None, '--before',
                      action='store',
                      dest='before',
                      help='Show only container created before Id or Name, ' +
                           'include non-running ones.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-l', '--latest',
                      action='store_true',
                      dest='latest',
                      help='Show only the latest created container, ' +
                           'include non-running ones.'),
        CommandOption(CommandOption.TYPE_NUMERIC, '-n', None,
                      action='store',
                      dest='limit',
                      help='Show n last created containers, include ' +
                           'non-running ones.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, None, '--no-trunc',
                      action='store_false',
                      dest='trunc',
                      help='Don\'t truncate output.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-q', '--quiet',
                      action='store_true',
                      dest='quiet',
                      help='Only display numeric IDs.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-s', '--size',
                      action='store_true',
                      dest='latest',
                      help='Display total file sizes.'),
        CommandOption(CommandOption.TYPE_CONTAINER, None, '--since',
                      action='store',
                      dest='since',
                      help='Show only containers created since Id or Name, ' +
                           'include non-running ones.')
    ],
    'pull': [
        CommandOption(CommandOption.TYPE_IMAGE, 'image',
                      action='store',
                      help='Image name to pull.'),
    ],
    'push': [
        CommandOption(CommandOption.TYPE_IMAGE_TAGGED, 'name',
                      action='store',
                      help='Image name to push (format: "name[:tag]").'),
    ],
    'images': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-a', '--all',
                      action='store_true',
                      dest='all',
                      help='Show all images (by default filter out the ' +
                           'intermediate image layers).'),
        CommandOption(CommandOption.TYPE_IMAGE, '-f', '--filter',
                      action='store',
                      dest='name',
                      help='Provide name to filter on.'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-q', '--quiet',
                      action='store_true',
                      dest='quiet',
                      help='Only show numeric IDs.')
    ],
    'refresh': [],
    'run': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-d', '--detach',
                      action='store_true',
                      dest='detach',
                      help=('Detached mode: run the container in the '
                            'background and print the new container ID')),
        OPTION_ATTACH_CHOICE,
        OPTION_ENV,
        OPTION_EXPOSE,
        OPTION_CONTAINER_HOSTNAME,
        OPTION_CONTAINER_NAME,
        OPTION_LINK,
        OPTION_PUBLISH_ALL,
        OPTION_PUBLISH,
        OPTION_INTERACTIVE,
        OPTION_TTY,
        OPTION_RM,
        OPTION_VOLUME,
        OPTION_VOLUMES_FROM,
        CommandOption(CommandOption.TYPE_IMAGE_TAGGED, None, 'image',
                      action='store',
                      help='Image name.'),
        OPTION_COMMAND,
        OPTION_NET,
    ],
    'shell': [
        OPTION_CONTAINER_RUNNING,
        CommandOption(CommandOption.TYPE_CHOICE, 'command',
                      action='store',
                      help='Shell command to execute.',
                      choices=[
                          'bash',
                          'sh',
                          'zsh',
                          '/bin/sh',
                          '/usr/bin/bash',
                          '/usr/bin/sh',
                          '/usr/bin/zsh',
                          '/usr/local/bin/bash',
                          '/usr/local/bin/sh',
                          '/usr/local/bin/zsh',
                      ],
                      default='bash',
                      nargs='?'),
    ],
    'start': [
        OPTION_ATTACH_BOOLEAN,
        CommandOption(CommandOption.TYPE_BOOLEAN, '-i', '--interactive',
                      action='store_true',
                      dest='interactive',
                      default=False,
                      help='Attach container\'s STDIN.',
                      api_match=False),
        OPTION_CONTAINER,
    ],
    'restart': [
        CommandOption(CommandOption.TYPE_NUMERIC, '-t', '--timeout',
                      dest='timeout',
                      help=('Number of seconds to try to stop for before '
                            'killing the container. Once killed it will then '
                            'be restarted. Default is 10 seconds.')),
        CommandOption(CommandOption.TYPE_CONTAINER, 'container',
                      action='store',
                      help='Container ID or name to use.',
                      nargs='+'),
    ],
    'rm': [
        CommandOption(CommandOption.TYPE_CONTAINER, 'container',
                      action='store',
                      help='Container ID or name to use.',
                      nargs='+'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '--all-stopped',
                      action='store_true',
                      dest='all_stopped',
                      help='Shortcut to remove all stopped containers.',
                      api_match=False,
                      cli_match=False),
        CommandOption(CommandOption.TYPE_BOOLEAN, '--all',
                      action='store_true',
                      dest='all',
                      help='Shortcut to remove all containers.',
                      api_match=False,
                      cli_match=False),
        CommandOption(CommandOption.TYPE_BOOLEAN, '-f', '--force',
                      action='store_true',
                      dest='force',
                      help='Force the removal of a running container (uses SIGKILL).'),
    ],
    'rmi': [
        CommandOption(CommandOption.TYPE_IMAGE_TAGGED, 'image',
                      action='store',
                      help='Image name name to remove.',
                      nargs='+'),
        CommandOption(CommandOption.TYPE_BOOLEAN, '--all-dangling',
                      action='store_true',
                      dest='all_dangling',
                      help='Shortcut to remove all dangling images.',
                      api_match=False,
                      cli_match=False),
        CommandOption(CommandOption.TYPE_BOOLEAN, '--all',
                      action='store_true',
                      dest='all',
                      help='Shortcut to remove all images.',
                      api_match=False,
                      cli_match=False),
    ],
    'search': [
        CommandOption(CommandOption.TYPE_IMAGE, 'term',
                      action='store',
                      help='A term to search for.'),
    ],
    'stop': [
        OPTION_CONTAINER_RUNNING,
    ],
    'tag': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-f', '--force',
                      action='store_true',
                      dest='force',
                      help='Force.'),
        CommandOption(CommandOption.TYPE_IMAGE, 'image',
                      action='store',
                      help='The image to tag (format: "image[:tag]").'),
        CommandOption(CommandOption.TYPE_IMAGE_TAG, 'name',
                      action='store',
                      help=('The tag name (format: "[registryhost/]'
                            '[username/]name[:tag]").')),
    ],
    'top': [
        OPTION_CONTAINER_RUNNING,
    ],
    'unpause': [
        OPTION_CONTAINER_RUNNING,
    ],
    'volume create': [
        OPTION_VOLUME_NAME,
        OPTION_DRIVER,
        OPTION_OPT
    ],
    'volume inspect': [
        OPTION_VOLUME_NAME_POS
    ],
    'volume ls': [
        CommandOption(CommandOption.TYPE_BOOLEAN, '-q', '--quiet',
                      action='store_true',
                      dest='quiet',
                      help='Only display volume names.'),
        OPTION_FILTERS
    ],
    'volume rm': [
        OPTION_VOLUME_NAME_POS
    ],
}


# Hidden options are options that docker-py supports, but the standard docker cli doesn't have
# them. Since we're emulating the standard cli as close as possible, we're not suggesting these
# to the user.
HIDDEN_OPTIONS = {
    'start': [
        OPTION_PUBLISH_ALL,
    ],
    'run': [
        OPTION_PORTS,
        OPTION_HOST_CONFIG,
        OPTION_STDIN_OPEN
    ],
    'create': [
        OPTION_PORTS,
        OPTION_HOST_CONFIG,
        OPTION_STDIN_OPEN
    ]
}


def all_option_names():
    """
    Helper method to go through all commands and return all option names,
    long or short.
    :return: iterable
    """
    opts = set([OPTION_HELP.short_name, OPTION_HELP.long_name])
    for command in COMMAND_OPTIONS:
        for opt in COMMAND_OPTIONS[command]:
            if opt.short_name and opt.short_name.startswith('-'):
                opts.add(opt.short_name)
            if opt.long_name and opt.long_name.startswith('--'):
                opts.add(opt.long_name)
    return sorted(list(opts))


def find_option(command, name):
    """
    Helper method to find command option by its name.
    :param command: string
    :param name: string
    :return: CommandOption
    """
    # TODO: use all_options
    if command in COMMAND_OPTIONS:
        if name == 'help':
            return OPTION_HELP
        for opt in COMMAND_OPTIONS[command]:
            if name in [opt.short_name, opt.long_name]:
                return opt
    return None


def allowed_args(command_name, **kwargs):
    """
    Return only arguments that the command accepts.
    :param command_name: string
    :param kwargs: dict
    :return: dict
    """
    matches = {}
    available = all_supported(command_name)
    if available:
        for k in kwargs:
            if k in available:
                matches[k] = kwargs[k]
    return matches


def all_options(command, include_hidden=False):
    """
    Helper method to find all command options.
    :param command: string
    :param include_hidden: boolean
    :return: set of CommandOption
    """
    result = [OPTION_HELP]
    if command in COMMAND_OPTIONS:
        result.extend(COMMAND_OPTIONS[command])
    if include_hidden and command in HIDDEN_OPTIONS:
        result.extend(HIDDEN_OPTIONS[command])
    return result


def all_supported(command):
    """
    Helper method to find all command options that docker-py supports.
    :param command: string
    :return: set of CommandOption
    """
    result = set([OPTION_HELP])

    if command in COMMAND_OPTIONS:
        result.update(
            [x.dest for x in COMMAND_OPTIONS[command] if x.api_match])

    if command in HIDDEN_OPTIONS:
        result.update([x.dest for x in HIDDEN_OPTIONS[command]])

    return result


def parse_command_options(cmd, params):
    """
    Parse options for a given command.
    :param cmd: string: command name
    :param params: list: all tokens after command name
    :return: parser, args, opts
    """
    parser = OptParser(
        prog=cmd, add_help_option=False, conflict_handler='resolve')
    parser.disable_interspersed_args()
    for opt in all_options(cmd, include_hidden=True):
        if opt.name.startswith('-'):
            parser.add_option(*opt.args, **opt.kwargs)
    popts, pargs = parser.parse_args(params)
    parser.assert_option_format()
    popts = vars(popts)

    # Add hidden defaults
    if cmd in HIDDEN_OPTIONS:
        for opt in HIDDEN_OPTIONS[cmd]:
            if opt.default is not None:
                popts[opt.dest] = opt.default

    return parser, popts, pargs


def format_command_line(cmd, is_long, args, kwargs):
    """
    Reconstruct the command  line for sending back to official Docker CLI.
    :param cmd: command
    :param is_long: bool use long option names
    :param args: positional parameters
    :param kwargs: named parameters
    :return: string
    """
    opts = dict([(x.dest, x) for x in all_options(cmd)
                 if x.name.startswith('-')])
    comps = ['docker', cmd]

    def kve(o, v):
        v1, v2 = v.split('=', 1)
        if ' ' in v2:
            return '{0} {1}="{2}"'.format(o.get_name(is_long), v1, v2)
        return '{0} {1}={2}'.format(o.get_name(is_long), v1, v2)

    def kv(o, v):
        if o.dest == 'environment':
            return kve(o, v)
        return '{0}={1}'.format(o.get_name(is_long), v)

    for opt_dest, opt_value in kwargs.items():
        if opt_dest in opts and opt_value is not None:
            opt = opts[opt_dest]
            if opt.cli_match:
                if isinstance(opt_value, bool):
                    # skip appending if default
                    if opt.default is not None and opt_value == opt.default:
                        continue
                    comps.append(opt.get_name(is_long))
                elif isinstance(opt_value, list):
                    comps.append(' '.join([kv(opt, val) for val in opt_value]))
                else:
                    comps.append(kv(opt, opt_value))
    comps.extend(args)
    external_command = ' '.join(comps)
    return external_command


def split_command_and_args(tokens):
    """
    Take all tokens from command line, return command part and args part.
    Command can be more than 1 words.
    :param tokens: list
    :return: tuple of (string, list)
    """
    command, args = None, None
    if tokens:
        length = 1
        for cmd_name in COMMAND_LENGTH:
            if ' '.join(tokens).startswith(cmd_name):
                length = COMMAND_LENGTH[cmd_name]
                break
        command = ' '.join(tokens[:length])
        args = tokens[length:] if len(tokens) >= length else None
    return command, args


def format_command_help(cmd):
    """
    Format help string for the command.
    :param cmd: string: command name
    :return: string
    """
    usage = [cmd, '[options]']
    alls = all_options(cmd)

    standards = [_ for _ in alls if _.cli_match]
    extras = [_ for _ in alls if not _.cli_match]

    for opt in alls:
        if not opt.name.startswith('-'):
            optname = "[{0}]".format(opt.name) if opt.is_optional else opt.name
            usage.append(optname)

    usage = ' '.join(usage)

    parser = OptParser(prog=cmd, add_help_option=False, usage=usage,
                       conflict_handler='resolve')

    for opt in standards:
        if opt.name.startswith('-'):
            parser.add_option(*opt.args, **opt.kwargs)

    if extras:
        g = OptionGroup(parser, "Non-standard options")
        for opt in extras:
            g.add_option(*opt.args, **opt.kwargs)
        parser.add_option_group(g)

    return parser.format_help()


class OptParser(OptionParser):

    # TODO: Bad bad bad. There should be a better way to do this.
    def assert_option_format(self):
        """
        I don't want environment vars to be provided as
        "-e KEY VALUE", I want "-e KEY=VALUE" instead.
        Would argparse help here?
        """
        dict_values = vars(self.values)
        if 'environment' in dict_values and dict_values['environment']:
            for envar in dict_values['environment']:
                if '=' not in envar:
                    raise OptionError(
                        'Usage: -e KEY1=VALUE1 -e KEY2=VALUE2...',
                        '-e')

    """
    Wrapper around OptionParser.
    Overrides error method to throw an exception.
    """
    def error(self, msg):
        """error(msg : string)

        Print a usage message incorporating 'msg' to stderr and exit.
        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        raise Exception("Error parsing options: {0}".format(msg))
