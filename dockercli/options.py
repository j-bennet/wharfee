from optparse import make_option


COMMAND_OPTIONS = {
    'ps': [
        make_option("-a", "--all", action="store_true", dest="all",
                    help='Show all containers. '
                         'Only running containers are shown by default.'),
        make_option("-q", "--quiet", action="store_true", dest="quiet",
                    help='Only display numeric IDs.'),
        make_option("-l", "--latest", action="store_true", dest="latest",
                    help='Show only the latest created container, '
                         'include non-running ones.'),
        make_option("-s", "--size", action="store_true", dest="latest",
                    help='Display total file sizes.'),
    ]
}

