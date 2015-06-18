import shutil
from os.path import expanduser, exists

from configobj import ConfigObj

def read_config(usr_config, def_config=None):
    """
    Read config file (if not exists, read default config).
    :param usr_config: string: config file name
    :param def_config: string: default name
    :return: ConfigParser
    """
    cfg = ConfigObj()

    if def_config:
        cfg.merge(ConfigObj(def_config, interpolation=False))

    cfg.merge(ConfigObj(expanduser(usr_config), interpolation=False))
    return cfg


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


def write_config(cfg, cfg_path):
    """
    Write current user's config.
    :param cfg: ConfigObj
    :param cfg_path: string: path to write
    """
    cfg.filename = expanduser(cfg_path)
    cfg.write()
