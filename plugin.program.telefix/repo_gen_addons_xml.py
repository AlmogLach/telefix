# -*- coding: utf-8 -*-
"""Generate addons.xml and addons.xml.md5 for Telefix repo (GitHub Pages)."""
import os
import hashlib
import xml.etree.ElementTree as ET

ADDON_XML = os.path.join(os.path.dirname(__file__), 'addon.xml')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'repo_output')

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tree = ET.parse(ADDON_XML)
    root = tree.getroot()
    # Wrap in <addons>
    addons = ET.Element('addons')
    addons.append(root)
    tree = ET.ElementTree(addons)
    out_path = os.path.join(OUT_DIR, 'addons.xml')
    with open(out_path, 'wb') as f:
        tree.write(f, encoding='utf-8', default_namespace='', method='xml', xml_declaration=True)
    content = open(out_path, 'rb').read()
    md5_path = os.path.join(OUT_DIR, 'addons.xml.md5')
    with open(md5_path, 'w') as f:
        f.write(hashlib.md5(content).hexdigest())
    print('Written:', out_path, md5_path)
    print('Copy repo_output/* to your GitHub repo root (e.g. telefix-repo).')

if __name__ == '__main__':
    main()
