# -*- coding: utf-8
import os


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
