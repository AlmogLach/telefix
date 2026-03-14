# -*- coding: utf-8 -*-
"""Telefix Wizard - clear cache, packages, thumbnails (Chameleon-style)."""
import os
import shutil
import xbmc
import xbmcgui

from . import config
from . import tools


def _notify(msg, error=False):
    xbmc.executebuiltin('Notification(%s,%s,%s)' % (
        config.ADDON_NAME, msg, 3000 if error else 2000))


def _clean_folder(folder, exclude_dirs=None, exclude_files=None):
    """Delete contents of folder; exclude_dirs/exclude_files = names to skip."""
    if not folder or not os.path.exists(folder) or not os.path.isdir(folder):
        return 0
    exclude_dirs = exclude_dirs or []
    exclude_files = exclude_files or []
    count = 0
    try:
        for root, dirs, files in os.walk(folder, topdown=False):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                if f in exclude_files:
                    continue
                try:
                    path = os.path.join(root, f)
                    os.unlink(path)
                    count += 1
                except (OSError, IOError):
                    pass
            for d in dirs:
                try:
                    path = os.path.join(root, d)
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                        count += 1
                except (OSError, IOError):
                    pass
    except (OSError, IOError):
        pass
    return count


def clear_cache(confirm=True):
    """Clear Kodi cache and temp folders."""
    if confirm:
        if not xbmcgui.Dialog().yesno(config.ADDON_NAME,
                'Clear cache and temp?', 'This frees space and can fix some issues.'):
            return
    total = 0
    for folder in config.CACHE_DIRS:
        if os.path.exists(folder):
            total += _clean_folder(folder, exclude_dirs=['archive_cache'])
    _notify('Cache cleared: %s items' % total)


def clear_packages(confirm=True):
    """Clear Kodi addons packages folder (leftover install zips)."""
    if not os.path.exists(config.PACKAGES):
        _notify('No packages to clear')
        return
    size = tools.get_size(config.PACKAGES)
    if confirm:
        if not xbmcgui.Dialog().yesno(config.ADDON_NAME,
                'Clear install packages?', 'Size: %s. Free this space?' % tools.convert_size(size)):
            return
    count = _clean_folder(config.PACKAGES)
    _notify('Packages cleared: %s' % tools.convert_size(size))


def clear_thumbs(confirm=True):
    """Clear Kodi thumbnails (artwork cache)."""
    if confirm:
        if not xbmcgui.Dialog().yesno(config.ADDON_NAME,
                'Clear thumbnails?', 'Artwork will reload when you browse again.'):
            return
    if not os.path.exists(config.THUMBNAILS):
        _notify('No thumbnails to clear')
        return
    size = tools.get_size(config.THUMBNAILS)
    count = _clean_folder(config.THUMBNAILS)
    _notify('Thumbnails cleared: %s' % tools.convert_size(size))


def clear_crash_logs(confirm=True):
    """Clear crash/log files from logpath."""
    if not os.path.exists(config.LOGPATH):
        _notify('No log path')
        return
    files = []
    for f in os.listdir(config.LOGPATH):
        if 'crash' in f.lower() or f.endswith('.log'):
            files.append(os.path.join(config.LOGPATH, f))
    if not files:
        _notify('No crash logs to clear')
        return
    if confirm:
        if not xbmcgui.Dialog().yesno(config.ADDON_NAME,
                'Delete %s log/crash file(s)?' % len(files)):
            return
    for path in files:
        try:
            if os.path.isfile(path):
                os.unlink(path)
        except (OSError, IOError):
            pass
    _notify('Crash logs cleared')


def total_clean(confirm=True):
    """Clear cache + packages + thumbnails (full cleanup)."""
    if confirm:
        if not xbmcgui.Dialog().yesno(config.ADDON_NAME,
                'Full cleanup', 'Clear cache, packages, and thumbnails? This frees maximum space.'):
            return
    clear_cache(confirm=False)
    clear_packages(confirm=False)
    clear_thumbs(confirm=False)
    _notify('Full cleanup done')


def get_cache_size():
    """Return total size in bytes of cache + temp."""
    total = 0
    for folder in config.CACHE_DIRS:
        if os.path.exists(folder):
            total += tools.get_size(folder)
    return total
