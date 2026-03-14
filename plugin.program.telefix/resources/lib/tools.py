# -*- coding: utf-8 -*-
"""Telefix Wizard - file size and path helpers."""
import os


def get_size(path, total=0):
    if not path or not os.path.exists(path):
        return total
    try:
        if os.path.isfile(path):
            return total + os.path.getsize(path)
        for _root, _dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(_root, f)
                try:
                    total += os.path.getsize(fp)
                except (OSError, IOError):
                    pass
    except (OSError, IOError):
        pass
    return total


def convert_size(num, suffix='B'):
    num = float(num)
    for unit in ['', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit) if unit else "%d %s" % (int(num), suffix)
        num /= 1024.0
    return "%.1f TB" % num
