# -*- coding: utf-8 -*-
"""Telefix Wizard - optional auto-clean on Kodi startup."""

def start():
    import xbmc
    xbmc.sleep(5000)
    try:
        from resources.lib import config
        if config.get_setting('autoclean', 'false') != 'true':
            return
        from resources.lib import clear
        if config.get_setting('clearcache', 'false') == 'true':
            clear.clear_cache(confirm=False)
        if config.get_setting('clearpackages', 'false') == 'true':
            clear.clear_packages(confirm=False)
        if config.get_setting('clearthumbs', 'false') == 'true':
            clear.clear_thumbs(confirm=False)
    except Exception:
        pass
