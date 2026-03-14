# -*- coding: utf-8 -*-
# Telefix installer: extract bundled addon zips to Kodi addons folder

import os
import zipfile
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon

# Default: full setup zip from GitHub Releases (upload via Releases page)
TELEFIX_FULL_ZIP_URL = 'https://github.com/AlmogLach/telefix/releases/download/v1.0.0/telefix-full-setup.zip'

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
if ADDON_PATH and ADDON_PATH.startswith('special://'):
    ADDON_PATH = xbmcvfs.translatePath(ADDON_PATH)
PACKAGES_DIR = os.path.join(ADDON_PATH, 'resources', 'packages')
KODI_ADDONS = xbmcvfs.translatePath('special://home/addons/')


def _progress_dialog(heading, line1=''):
    return xbmcgui.DialogProgressBG() if hasattr(xbmcgui, 'DialogProgressBG') else xbmcgui.DialogProgress()


def _download_full_zip_from_github():
    """Download full setup zip from GitHub and extract to addons. Returns True on success."""
    try:
        import urllib.request
        temp_dir = xbmcvfs.translatePath('special://temp/')
        zip_path = os.path.join(temp_dir, 'telefix_full_setup.zip')
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except Exception:
                pass
        use_bg = hasattr(xbmcgui, 'DialogProgressBG')
        if use_bg:
            pd = xbmcgui.DialogProgressBG()
            pd.create('Telefix', 'מוריד מערך מלא מ-GitHub...')
        else:
            pd = xbmcgui.DialogProgress()
            pd.create('Telefix', 'מוריד מערך מלא מ-GitHub...')
        try:
            req = urllib.request.Request(TELEFIX_FULL_ZIP_URL, headers={'User-Agent': 'Kodi/Telefix'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                total = int(resp.headers.get('Content-Length', 0)) or 0
                chunk_size = 1024 * 512
                read = 0
                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        read += len(chunk)
                        if total and use_bg:
                            pd.update(int(100 * read / total), message='%.1f MB' % (read / (1024 * 1024)))
        except Exception as e:
            xbmc.log('Telefix download error: %s' % str(e), xbmc.LOGERROR)
            if use_bg:
                pd.close()
            else:
                pd.close()
            return False
        if use_bg:
            pd.update(100, message='מחלץ...')
        else:
            pd.close()
            pd = xbmcgui.DialogProgress()
            pd.create('Telefix', 'מחלץ...')
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                for info in z.infolist():
                    path = info.filename.replace('\\', '/').rstrip('/')
                    if not path or path.startswith('__MACOSX'):
                        continue
                    target = os.path.join(KODI_ADDONS, path)
                    if path.endswith('/'):
                        if not os.path.exists(target):
                            os.makedirs(target, exist_ok=True)
                    else:
                        target_dir = os.path.dirname(target)
                        if target_dir and not os.path.exists(target_dir):
                            os.makedirs(target_dir, exist_ok=True)
                        with z.open(info.filename) as src:
                            with open(target, 'wb') as dst:
                                dst.write(src.read())
        except Exception as e:
            xbmc.log('Telefix extract error: %s' % str(e), xbmc.LOGERROR)
            if use_bg:
                pd.close()
            return False
        try:
            os.remove(zip_path)
        except Exception:
            pass
        if use_bg:
            pd.close()
        else:
            pd.close()
        return True
    except Exception as e:
        xbmc.log('Telefix download_full_zip: %s' % str(e), xbmc.LOGERROR)
        return False


def install_telefix_setup():
    """Install addons from resources/packages/*.zip into special://home/addons/"""
    if not xbmcvfs.exists(PACKAGES_DIR):
        if _download_full_zip_from_github():
            xbmcgui.Dialog().ok('Telefix', 'המערך המלא הורד מ-GitHub.\n\nלחץ שוב על "Telefix Bingie Skin" להתקנת כל התוספים.')
            return
        xbmcgui.Dialog().ok('Telefix',
            'לא נמצא מערך מקומי ולא ניתן להוריד מ-GitHub.\n\n'
            'הוסף מקור: https://almoglach.github.io/telefix/\nולחץ "התקן מקובץ zip".')
        xbmc.executebuiltin('InstallFromZip')
        return
    zips = [f for f in xbmcvfs.listdir(PACKAGES_DIR)[1] if f and f.lower().endswith('.zip')]
    if not zips:
        if _download_full_zip_from_github():
            xbmcgui.Dialog().ok('Telefix', 'המערך המלא הורד מ-GitHub.\n\nלחץ שוב על "Telefix Bingie Skin" להתקנת כל התוספים.')
            return
        xbmcgui.Dialog().ok('Telefix', 'אין קבצי zip בחבילות.\n\nהוסף מקור: https://almoglach.github.io/telefix/\nולחץ "התקן מקובץ zip".')
        xbmc.executebuiltin('InstallFromZip')
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
                names = z.namelist()
                if not names:
                    continue
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
    path = path.rstrip('/').rstrip('\\')
    if not path or xbmcvfs.exists(path):
        return
    parent = os.path.dirname(path)
    if parent and parent != path:
        _mkdirs(parent)
    xbmcvfs.mkdir(path)
