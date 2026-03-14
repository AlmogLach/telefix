# -*- coding: utf-8 -*-
"""Telefix Wizard - path and settings config."""
import os
import xbmc
import xbmcaddon
import xbmcvfs

ADDON_ID = 'plugin.program.telefix'
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_FANART = ADDON.getAddonInfo('fanart')

if ADDON_PATH and ADDON_PATH.startswith('special://'):
    ADDON_PATH = xbmcvfs.translatePath(ADDON_PATH)
ADDON_PATH = os.path.normpath(ADDON_PATH.rstrip('/').rstrip('\\'))

# Kodi special paths
HOME = xbmcvfs.translatePath('special://home/')
USERDATA = xbmcvfs.translatePath('special://userdata/')
TEMP = xbmcvfs.translatePath('special://temp/')
PROFILE = xbmcvfs.translatePath('special://profile/')
DATABASE = xbmcvfs.translatePath('special://database/')
THUMBNAILS = xbmcvfs.translatePath('special://thumbnails/')
LOGPATH = xbmcvfs.translatePath('special://logpath/')

ADDONS = os.path.join(HOME, 'addons')
PACKAGES = os.path.join(ADDONS, 'packages')
ADDON_DATA = os.path.join(USERDATA, 'addon_data')

CACHE_DIRS = [
    os.path.join(HOME, 'cache'),
    os.path.join(HOME, 'temp'),
]
LOGFILES = ['kodi.log', 'xbmc.log', 'xbmc.old.log']


def get_setting(key, default=''):
    try:
        return ADDON.getSetting(key) or default
    except Exception:
        return default


def set_setting(key, value):
    try:
        ADDON.setSetting(key, str(value))
    except Exception:
        pass


def open_settings(name=None):
    ADDON.openSettings()
