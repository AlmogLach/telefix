# Build plugin.program.telefix.zip with addon.xml as first entry (Kodi requirement)
import os
import zipfile

addon_path = os.path.normpath(r"C:\Users\Almog\AppData\Roaming\Kodi\addons\plugin.program.telefix")
zip_path = os.path.normpath(r"C:\Users\Almog\AppData\Roaming\Kodi\plugin.program.telefix.zip")
addon_id = "plugin.program.telefix"

if os.path.exists(zip_path):
    os.remove(zip_path)

all_files = []
for root, dirs, files in os.walk(addon_path):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, addon_path).replace("\\", "/")
        arcname = addon_id + "/" + rel
        all_files.append((full, arcname))

# Put addon.xml first
all_files.sort(key=lambda x: (0 if "addon.xml" in x[1] else 1, x[1]))

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for full, arcname in all_files:
        zf.write(full, arcname)

with zipfile.ZipFile(zip_path, "r") as zf:
    first = zf.namelist()[0]
    print("First entry:", first)
print("Size MB:", round(os.path.getsize(zip_path) / (1024 * 1024), 2))
