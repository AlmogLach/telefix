# -*- coding: utf-8 -*-
# Telefix Wizard - Install setup + Maintenance (Chameleon-style)

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_FANART = ADDON.getAddonInfo('fanart')


def _params(paramstring):
    return dict(parse_qsl(paramstring.lstrip('?'))) if paramstring else {}


def _url(mode, **kwargs):
    u = '%s?mode=%s' % (sys.argv[0], mode)
    for k, v in kwargs.items():
        if v is not None:
            u += '&%s=%s' % (k, str(v))
    return u


def _add_item(label, mode, is_folder=False, **kwargs):
    url = _url(mode, **kwargs)
    li = xbmcgui.ListItem(label)
    li.setArt({'icon': ADDON_ICON, 'fanart': ADDON_FANART})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, isFolder=is_folder)


def _L(id):
    return ADDON.getLocalizedString(id) or str(id)


def run_install():
    from resources.lib import installer
    installer.install_telefix_setup()


def maintenance_menu(handle):
    from resources.lib import config
    from resources.lib import clear
    from resources.lib import tools

    xbmcplugin.setContent(handle, 'files')
    # Sizes
    cache_size = clear.get_cache_size()
    pack_size = tools.get_size(config.PACKAGES) if __import__('os').path.exists(config.PACKAGES) else 0
    thumb_size = tools.get_size(config.THUMBNAILS) if __import__('os').path.exists(config.THUMBNAILS) else 0

    _add_item(_L(30004) + ' [%s]' % tools.convert_size(cache_size), 'clearcache')
    _add_item(_L(30005) + ' [%s]' % tools.convert_size(pack_size), 'clearpackages')
    _add_item(_L(30006) + ' [%s]' % tools.convert_size(thumb_size), 'clearthumbs')
    _add_item(_L(30007), 'totalclean')
    _add_item(_L(30008), 'clearcrash')
    # Auto-clean toggle
    autoclean = config.get_setting('autoclean', 'false') == 'true'
    on_off = 'ON' if autoclean else 'OFF'
    _add_item(_L(30009) % on_off, 'toggleautoclean')
    xbmcplugin.endOfDirectory(handle)


def main():
    handle = int(sys.argv[1])
    params = _params(sys.argv[2] if len(sys.argv) > 2 else '')
    mode = params.get('mode')

    # Actions (no list)
    if mode == 'install':
        run_install()
        return
    if mode == 'settings':
        ADDON.openSettings()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'clearcache':
        from resources.lib import clear
        clear.clear_cache()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'clearpackages':
        from resources.lib import clear
        clear.clear_packages()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'clearthumbs':
        from resources.lib import clear
        clear.clear_thumbs()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'totalclean':
        from resources.lib import clear
        clear.total_clean()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'clearcrash':
        from resources.lib import clear
        clear.clear_crash_logs()
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'toggleautoclean':
        from resources.lib import config
        cur = config.get_setting('autoclean', 'false')
        config.set_setting('autoclean', 'false' if cur == 'true' else 'true')
        xbmc.executebuiltin('Container.Refresh()')
        return
    if mode == 'installfromzip':
        # Open Kodi "Install from zip file" dialog
        xbmc.executebuiltin('InstallFromZip')
        return

    # Menus
    if mode == 'maint':
        maintenance_menu(handle)
        return

    # Main menu
    xbmcplugin.setContent(handle, 'files')
    _add_item(_L(30001), 'install')
    _add_item(_L(30015), 'installfromzip')
    _add_item(_L(30003), 'maint', is_folder=True)
    _add_item(_L(30002), 'settings')
    xbmcplugin.endOfDirectory(handle)


if __name__ == '__main__':
    main()
