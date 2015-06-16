# -*- coding: utf-8
import os
import math


def parse_port_bindings(bindings):
    """
    Parse array of string port bindings into a dict.

    port_bindings={
        1111: 4567,
        2222: None
    }

    or
    port_bindings={
        1111: ('127.0.0.1', 4567)
    }

    :param bindings: array of string
    :return: dict
    """

    def parse_port_mapping(s):
        """
        Parse single port mapping.
        """
        if ':' in s:
            parts = s.split(':')
            if len(parts) > 2:
                ip, hp, cp = parts[0], parts[1], parts[2]
                return cp, (ip, None if hp == '' else hp)
            else:
                hp, cp = parts[0], parts[1]
                return cp, None if hp == '' else hp
        else:
            return s, None
    result = {}
    if bindings:
        for binding in bindings:
            container_port, mapping = parse_port_mapping(binding)
            result[container_port] = mapping
    return result


def filesize(size):
    """
    Pretty-print file size from bytes.
    """
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    if int(size) > 0:
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024, i)
        s = round(size / p, 3)
        if s > 0:
            return '%s %s' % (s, size_name[i])
    return '0 B'


def complete_path(curr_dir, last_dir):
    """
    Return the path to complete that matches the last entered component.
    If the last entered component is ~, expanded path would not
    match, so return all of the available paths.
    :param curr_dir: string
    :param last_dir: string
    :return: string
    """
    if not last_dir or curr_dir.startswith(last_dir):
        return curr_dir
    elif last_dir == '~':
        return os.path.join(last_dir, curr_dir)


def parse_path(root_dir):
    """
    Split path into head and last component for the completer.
    Also return position where last component starts.
    :param root_dir: path
    :return: tuple of (string, string, int)
    """
    base_dir, last_dir, position = '', '', 0
    if root_dir:
        base_dir, last_dir = os.path.split(root_dir)
        position = -len(last_dir) if last_dir else 0
    return base_dir, last_dir, position


def list_dir(root_dir, dirs_only=False, include_special=False):
    """
    List directory.
    :param root_dir: string: directory to list
    :param dirs_only: boolean
    :param include_special: boolean
    :return: list
    """
    root_dir = '.' if not root_dir else root_dir
    res = []

    if '~' in root_dir:
        root_dir = os.path.expanduser(root_dir)

    if not os.path.exists(root_dir):
        root_dir, _ = os.path.split(root_dir)

    if os.path.exists(root_dir):
        for name in os.listdir(root_dir):
            path = os.path.join(root_dir, name)
            if not include_special and name.startswith('.'):
                continue
            if dirs_only and not os.path.isdir(path):
                continue
            res.append(name)
    return res