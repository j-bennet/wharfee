import shutil
from os.path import expanduser, exists

try:
    # Python 2.x
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    # Python 3.x
    from configparser import ConfigParser


def read_config(filename, default_filename=None):
    """
    Read config file (if not exists, read default config).
    :param filename: string: config file name
    :param default_filename: string: default name
    :return: ConfigParser
    """
    filename = expanduser(filename)
    parser = ConfigParser()

    # no need for try/except, as parser.read will not fail in case of IOError
    if default_filename:
        parser.read(default_filename)

    parser.read(filename)
    return parser


def write_default_config(source, destination, overwrite=False):
    """
    Write default config (from template).
    :param source: string: path to template
    :param destination: string: path to write
    :param overwrite: boolean
    """
    destination = expanduser(destination)
    if not overwrite and exists(destination):
        return

    shutil.copyfile(source, destination)
