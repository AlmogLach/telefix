# -*- coding: utf-8 -*-
# Telefix installer - Chameleon style: one build zip, extract to Kodi HOME

import os
import zipfile
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon

# Build zip URL (single zip with addons/ inside - extract to special://home)
TELEFIX_BUILD_ZIP_URL = 'https://github.com/AlmogLach/telefix/releases/download/v1.0.0/telefix-build.zip'

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
KODI_HOME = xbmcvfs.translatePath('special://home/')
if KODI_HOME:
    KODI_HOME = os.path.normpath(KODI_HOME.rstrip('/').rstrip('\\'))

# Don't overwrite wizard and repo when extracting build
SKIP_ADDONS = ('plugin.program.telefix', 'repository.telefix')


def _skip_path(path):
    """Skip our addons so we don't overwrite ourselves."""
    path = path.replace('\\', '/')
    for skip in SKIP_ADDONS:
        if '/%s/' % skip in path or path.startswith('%s/' % skip):
            return True
    return False


def install_telefix_setup():
    """Chameleon style: download one build zip, extract to Kodi HOME."""
    import urllib.request

    temp_dir = xbmcvfs.translatePath('special://temp/')
    zip_path = os.path.join(temp_dir, 'telefix_build.zip')
    if os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception:
            pass

    use_bg = hasattr(xbmcgui, 'DialogProgressBG')
    if use_bg:
        pd = xbmcgui.DialogProgressBG()
        pd.create('Telefix', 'מוריד בילד...')
    else:
        pd = xbmcgui.DialogProgress()
        pd.create('Telefix', 'מוריד בילד Telefix...', 'מתחבר...')

    def update_progress(percent, msg):
        if use_bg:
            pd.update(percent, message=msg)
        else:
            pd.update(percent, msg, '')

    # Download
    try:
        req = urllib.request.Request(TELEFIX_BUILD_ZIP_URL, headers={'User-Agent': 'Kodi/Telefix'})
        with urllib.request.urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get('Content-Length', 0)) or 0
            total_mb = total / (1024 * 1024) if total else 0
            chunk_size = 1024 * 512
            read = 0
            with open(zip_path, 'wb') as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    read += len(chunk)
                    if total and total > 0:
                        pct = min(100, int(100 * read / total))
                        if total_mb >= 1:
                            update_progress(pct, 'מוריד... %.1f / %.1f MB (%d%%)' % (read / (1024 * 1024), total_mb, pct))
                        else:
                            update_progress(pct, 'מוריד... %d%%' % pct)
                    if not use_bg and pd.iscanceled():
                        pd.close()
                        return
    except Exception as e:
        xbmc.log('Telefix download error: %s' % str(e), xbmc.LOGERROR)
        pd.close()
        xbmcgui.Dialog().ok('Telefix',
            'שגיאה בהורדה מ-GitHub.\n\n%s\n\nוודא שהקובץ telefix-build.zip קיים ב-Releases.' % str(e))
        return

    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        pd.close()
        xbmcgui.Dialog().ok('Telefix', 'ההורדה נכשלה או הקובץ ריק.')
        return

    # Extract to Kodi HOME (like Chameleon)
    update_progress(0, 'מחלץ...')
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            infolist = [i for i in z.infolist()
                        if i.filename.replace('\\', '/').strip('/')
                        and not i.filename.startswith('__MACOSX')]
            n_total = len(infolist)
            for idx, info in enumerate(infolist):
                path = info.filename.replace('\\', '/').rstrip('/')
                if not path:
                    continue
                if _skip_path(path):
                    continue
                xbmc.sleep(0)
                target = os.path.join(KODI_HOME, path)
                if path.endswith('/'):
                    if not os.path.exists(target):
                        os.makedirs(target, exist_ok=True)
                else:
                    target_dir = os.path.dirname(target)
                    if target_dir and not os.path.exists(target_dir):
                        os.makedirs(target_dir, exist_ok=True)
                    chunk_size = 1024 * 256
                    with z.open(info.filename) as src:
                        with open(target, 'wb') as dst:
                            while True:
                                chunk = src.read(chunk_size)
                                if not chunk:
                                    break
                                dst.write(chunk)
                if n_total > 0:
                    pct = int(100 * (idx + 1) / n_total)
                    update_progress(pct, 'מחלץ... קובץ %d מתוך %d (%d%%)' % (idx + 1, n_total, pct))
                if not use_bg and pd.iscanceled():
                    pd.close()
                    return
    except Exception as e:
        xbmc.log('Telefix extract error: %s' % str(e), xbmc.LOGERROR)
        pd.close()
        xbmcgui.Dialog().ok('Telefix', 'שגיאה בחילוץ:\n%s' % str(e))
        return
    try:
        os.remove(zip_path)
    except Exception:
        pass

    update_progress(100, 'הושלם!')
    xbmc.sleep(500)
    pd.close()
    xbmcgui.Dialog().ok('Telefix', 'ההתקנה הושלמה.\n\nהפעל מחדש את Kodi לשימוש בתוספים.')
    xbmc.executebuiltin('ReloadSkin()')
