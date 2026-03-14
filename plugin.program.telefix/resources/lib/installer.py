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
if ADDON_PATH:
    ADDON_PATH = os.path.normpath(ADDON_PATH.rstrip('/').rstrip('\\'))
if not ADDON_PATH or not xbmcvfs.exists(ADDON_PATH):
    _special = xbmcvfs.translatePath('special://home/addons/plugin.program.telefix')
    if _special:
        ADDON_PATH = os.path.normpath(_special.rstrip('/').rstrip('\\'))
if not ADDON_PATH or not xbmcvfs.exists(ADDON_PATH):
    try:
        _script = os.path.normpath(os.path.abspath(__file__))
        if 'plugin.program.telefix' in _script.replace('\\', '/'):
            ADDON_PATH = os.path.normpath(_script.split('plugin.program.telefix')[0] + 'plugin.program.telefix')
    except Exception:
        pass
PACKAGES_DIR = os.path.join(ADDON_PATH, 'resources', 'packages')
PACKAGES_DIR_VFS = PACKAGES_DIR.replace('\\', '/')
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
            pd.create('Telefix', 'מתחבר ל-GitHub...')
        else:
            pd = xbmcgui.DialogProgress()
            pd.create('Telefix', 'מתחבר ל-GitHub...', 'הכנה...')

        def _update_progress(percent, line1, line2='', line3=''):
            if use_bg:
                msg = line1
                if line2:
                    msg = line1 + ' | ' + line2
                pd.update(percent, message=msg)
            else:
                pd.update(percent, line1, line2 or line3)

        try:
            req = urllib.request.Request(TELEFIX_FULL_ZIP_URL, headers={'User-Agent': 'Kodi/Telefix'})
            with urllib.request.urlopen(req, timeout=120) as resp:
                total = int(resp.headers.get('Content-Length', 0)) or 0
                total_mb = total / (1024 * 1024) if total else 0
                chunk_size = 1024 * 512
                read = 0
                _update_progress(0, 'מוריד מערך מלא...', '0 MB', 'הורדה מתחילה...')
                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        read += len(chunk)
                        if total and total > 0:
                            pct = min(100, int(100 * read / total))
                            read_mb = read / (1024 * 1024)
                            if total_mb >= 1:
                                _update_progress(pct, 'מוריד מ-GitHub...', '%.1f / %.1f MB (%d%%)' % (read_mb, total_mb, pct), '')
                            else:
                                _update_progress(pct, 'מוריד...', '%d%%' % pct, '')
                        else:
                            _update_progress(0, 'מוריד...', '%.1f MB הורדו' % (read / (1024 * 1024)), '')
                        if not use_bg and pd.iscanceled():
                            return False
        except Exception as e:
            xbmc.log('Telefix download error: %s' % str(e), xbmc.LOGERROR)
            pd.close()
            return False

        _update_progress(0, 'מחלץ קבצים...', 'מעבד...', 'חילוץ מתחיל...')
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                infolist = [i for i in z.infolist() if i.filename.replace('\\', '/').rstrip('/') and not i.filename.startswith('__MACOSX')]
                n_total = len(infolist)
                for idx, info in enumerate(infolist):
                    path = info.filename.replace('\\', '/').rstrip('/')
                    if not path:
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
                    if n_total > 0:
                        pct = int(100 * (idx + 1) / n_total)
                        _update_progress(pct, 'מחלץ...', 'קובץ %d מתוך %d (%d%%)' % (idx + 1, n_total, pct), '')
                    if not use_bg and pd.iscanceled():
                        pd.close()
                        return False
        except Exception as e:
            xbmc.log('Telefix extract error: %s' % str(e), xbmc.LOGERROR)
            pd.close()
            return False
        try:
            os.remove(zip_path)
        except Exception:
            pass
        _update_progress(100, 'הושלם!', 'המערך מוכן.', '')
        xbmc.sleep(500)
        pd.close()
        return True
    except Exception as e:
        xbmc.log('Telefix download_full_zip: %s' % str(e), xbmc.LOGERROR)
        try:
            pd.close()
        except Exception:
            pass
        return False


def install_telefix_setup():
    """Install addons from resources/packages/*.zip into special://home/addons/"""
    pkg_dir = PACKAGES_DIR_VFS if xbmcvfs.exists(PACKAGES_DIR_VFS) else PACKAGES_DIR
    if not xbmcvfs.exists(pkg_dir):
        pkg_dir = PACKAGES_DIR
    if not xbmcvfs.exists(pkg_dir):
        pkg_dir = None
    if pkg_dir is None or not xbmcvfs.exists(pkg_dir):
        if not _download_full_zip_from_github():
            xbmcgui.Dialog().ok('Telefix',
                'לא נמצא מערך מקומי ולא ניתן להוריד מ-GitHub.\n\n'
                'הוסף מקור: https://almoglach.github.io/telefix/\nולחץ "התקן מקובץ zip".')
            xbmc.executebuiltin('InstallFromZip')
            return
        pkg_dir = os.path.join(KODI_ADDONS.rstrip('/').rstrip('\\'), 'plugin.program.telefix', 'resources', 'packages')
        if not os.path.exists(pkg_dir):
            pkg_dir = PACKAGES_DIR
    zips = []
    if xbmcvfs.exists(pkg_dir):
        try:
            zips = [f for f in xbmcvfs.listdir(pkg_dir)[1] if f and f.lower().endswith('.zip')]
        except Exception:
            pass
    if not zips and os.path.exists(pkg_dir):
        try:
            zips = [f for f in os.listdir(pkg_dir) if f and f.lower().endswith('.zip')]
        except Exception:
            pass
    if not zips:
        if not _download_full_zip_from_github():
            xbmcgui.Dialog().ok('Telefix', 'אין קבצי zip בחבילות.\n\nהוסף מקור: https://almoglach.github.io/telefix/\nולחץ "התקן מקובץ zip".')
            xbmc.executebuiltin('InstallFromZip')
            return
        pkg_dir = os.path.join(KODI_ADDONS.rstrip('/').rstrip('\\'), 'plugin.program.telefix', 'resources', 'packages')
        if not os.path.exists(pkg_dir):
            pkg_dir = PACKAGES_DIR
        zips = [f for f in os.listdir(pkg_dir) if f and f.lower().endswith('.zip')] if os.path.exists(pkg_dir) else []
    if not zips:
        xbmcgui.Dialog().ok('Telefix', 'לא נמצאו חבילות להתקנה.')
        return
    use_bg = hasattr(xbmcgui, 'DialogProgressBG')
    if use_bg:
        pd = xbmcgui.DialogProgressBG()
        pd.create('Telefix', 'Installing...')
    else:
        pd = xbmcgui.DialogProgress()
        pd.create('Telefix', 'Installing...')
    total = len(zips)
    pkg_dir_os = pkg_dir.replace('/', os.sep) if pkg_dir else PACKAGES_DIR
    for i, name in enumerate(zips):
        if use_bg:
            pd.update(int(100 * (i + 1) / total), message=name)
        else:
            pd.update(int(100 * (i + 1) / total), name)
        zip_path = os.path.join(pkg_dir_os, name)
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                names = z.namelist()
                if not names:
                    continue
                for info in z.infolist():
                    path = info.filename.replace('\\', '/').rstrip('/')
                    if not path or path.startswith('__MACOSX'):
                        continue
                    target_path = os.path.join(KODI_ADDONS, path)
                    target_dir = os.path.dirname(target_path)
                    if path.endswith('/'):
                        dir_to_make = target_path.rstrip('/').rstrip('\\')
                        if dir_to_make and not xbmcvfs.exists(dir_to_make):
                            _mkdirs(dir_to_make)
                        continue
                    if target_dir and not xbmcvfs.exists(target_dir):
                        _mkdirs(target_dir)
                    chunk_size = 1024 * 256
                    with z.open(info.filename) as src:
                        f = xbmcvfs.File(target_path, 'wb')
                        try:
                            while True:
                                chunk = src.read(chunk_size)
                                if not chunk:
                                    break
                                if isinstance(chunk, str):
                                    chunk = chunk.encode('utf-8')
                                f.write(chunk)
                        finally:
                            f.close()
        except Exception as e:
            xbmc.log('Telefix installer error %s: %s' % (name, str(e)), xbmc.LOGERROR)
            if use_bg:
                pd.close()
            else:
                pd.close()
            xbmcgui.Dialog().ok('Telefix', 'שגיאה בהתקנת %s:\n%s' % (name, str(e)))
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
