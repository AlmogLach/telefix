# Build telefix-build.zip - Chameleon style (addons/ inside zip, extract to Kodi HOME)
# Run with Kodi closed. Output: telefix-build.zip in same folder as this script.

import os
import zipfile

# When run from addon folder, parent dir is addons/
ADDONS_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUTPUT_ZIP = os.path.normpath(os.path.join(os.path.dirname(__file__), "telefix-build.zip"))

# Don't include wizard and repo in the build zip (user already has them)
EXCLUDE = {'plugin.program.telefix', 'repository.telefix'}

if os.path.exists(OUTPUT_ZIP):
    os.remove(OUTPUT_ZIP)

all_entries = []
for addon_name in os.listdir(ADDONS_ROOT):
    if addon_name in EXCLUDE:
        continue
    addon_path = os.path.join(ADDONS_ROOT, addon_name)
    if not os.path.isdir(addon_path):
        continue
    for root, dirs, files in os.walk(addon_path):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ADDONS_ROOT)
            arcname = "addons/" + rel.replace("\\", "/")
            all_entries.append((full, arcname))

# Sort so addon.xml etc come first per addon
all_entries.sort(key=lambda x: (x[1].count("/"), x[1]))

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for full, arcname in all_entries:
        zf.write(full, arcname)

print("First entry:", all_entries[0][1] if all_entries else "none")
print("Size MB:", round(os.path.getsize(OUTPUT_ZIP) / (1024 * 1024), 2))
print("Output:", OUTPUT_ZIP)
