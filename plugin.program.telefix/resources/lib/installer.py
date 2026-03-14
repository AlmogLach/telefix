# -*- coding: utf-8 -*-
# Telefix installer: extract bundled addon zips to Kodi addons folder

import os
import zipfile
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
if ADDON_PATH.startswith('special://'):
    ADDON_PATH = xbmcvfs.translatePath(ADDON_PATH)
PACKAGES_DIR = os.path.join(ADDON_PATH, 'resources', 'packages')
KODI_ADDONS = xbmcvfs.translatePath('special://home/addons/')


def _progress_dialog(heading, line1=''):
    return xbmcgui.DialogProgressBG() if hasattr(xbmcgui, 'DialogProgressBG') else xbmcgui.DialogProgress()


def install_telefix_setup():
    """Install addons from resources/packages/*.zip into special://home/addons/"""
    if not xbmcvfs.exists(PACKAGES_DIR):
        xbmcgui.Dialog().ok('Telefix', 'Packages folder not found. Put addon zips in resources/packages/')
        return
    zips = [f for f in xbmcvfs.listdir(PACKAGES_DIR)[1] if f and f.lower().endswith('.zip')]
    if not zips:
        xbmcgui.Dialog().ok('Telefix', 'No zip files in resources/packages/.\n\nPut addon .zip files there (each zip root = addon folder, e.g. skin.bingie/addon.xml).')
        return
    use_bg = hasattr(xbmcgui, 'DialogProgressBG')
    if use_bg:
        pd = xbmcgui.DialogProgressBG()
        pd.create('Telefix', 'Installing...')
    else:
        pd = xbmcgui.DialogProgress()
        pd.create('Telefix', 'Installing...')
    total = len(zips)
    for i, name in enumerate(zips):
        if use_bg:
            pd.update(int(100 * (i + 1) / total), message=name)
        else:
            pd.update(int(100 * (i + 1) / total), name)
        zip_path = os.path.join(PACKAGES_DIR, name)
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Expect zip root = single addon folder (e.g. skin.bingie/)
                names = z.namelist()
                if not names:
                    continue
                root = names[0].split('/')[0].split('\\')[0]
                if not root or root == name.replace('.zip', ''):
                    # Some zips have addon id as root folder
                    pass
                for info in z.infolist():
                    path = info.filename.replace('\\', '/').rstrip('/')
                    if not path:
                        continue
                    target_path = os.path.join(KODI_ADDONS, path)
                    target_dir = os.path.dirname(target_path)
                    if target_dir and not xbmcvfs.exists(target_dir):
                        _mkdirs(target_dir)
                    data = z.read(info.filename)
                    if isinstance(data, str):
                        data = data.encode('utf-8')
                    f = xbmcvfs.File(target_path, 'wb')
                    f.write(data)
                    f.close()
        except Exception as e:
            xbmc.log('Telefix installer error %s: %s' % (name, str(e)), xbmc.LOGERROR)
            if use_bg:
                pd.close()
            else:
                pd.close()
            xbmcgui.Dialog().ok('Telefix', 'Error installing %s:\n%s' % (name, str(e)))
            return
    if use_bg:
        pd.close()
    else:
        pd.close()
    xbmcgui.Dialog().ok('Telefix', 'Installation finished.\n\nRestart Kodi to use the new addons.')
    xbmc.executebuiltin('ReloadSkin()')


def _mkdirs(path):
    """Create directory and parents using xbmcvfs."""
    path = path.rstrip('/').rstrip('\\')
    if not path or xbmcvfs.exists(path):
        return
    parent = os.path.dirname(path)
    if parent and parent != path:
        _mkdirs(parent)
    xbmcvfs.mkdir(path)
