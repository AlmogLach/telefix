# Telefix Wizard

Kodi wizard addon (Chameleon-style): one-click install of the Telefix setup (Bingie skin + Mando + Telemedia + all addons) and **maintenance tools** (clear cache, packages, thumbnails, total cleanup).

## Features

- **Install Telefix setup** – Installs all bundled addons from `resources/packages/*.zip` (skin, Mando, Telemedia, repos, scripts, etc.).
- **Maintenance** (like Chameleon):
  - Clear cache
  - Clear packages (leftover install zips)
  - Clear thumbnails
  - Total cleanup (cache + packages + thumbnails)
  - Clear crash logs
  - Toggle auto-clean on startup (in Settings)
- **Settings** – Auto-clean on startup options.

## Install from zip (local)

1. Zip the `plugin.program.telefix` folder so the **root of the zip is the addon folder** (e.g. `plugin.program.telefix/addon.xml` inside the zip).
2. In Kodi: **Add-ons** → box icon → **Install from zip file** → select the zip.
3. Run **Program add-ons** → **Telefix Wizard**.

To build the zip with correct structure (addon.xml first for Kodi):

```bash
python build_zip.py
```

Output: `plugin.program.telefix.zip` in your Kodi folder.

## Install from GitHub (repository)

### 1. Create the repo and enable GitHub Pages

1. Create a new GitHub repo (e.g. `telefix-repo`).
2. **Settings** → **Pages** → Source: **Deploy from a branch** → branch `main` / root → Save.
3. Clone the repo and add these files.

### 2. Repo structure

```
telefix-repo/
├── addons.xml          # Generated (see below)
├── addons.xml.md5      # MD5 of addons.xml
├── zips/
│   └── plugin.program.telefix/
│       └── 1.0.0/
│           └── plugin.program.telefix-1.0.0.zip
└── repository.telefix/ # Optional: ship repo addon in repo
```

### 3. Generate addons.xml

Use the same `addon.xml` from the wizard. Minimal `addons.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<addons>
  <addon id="plugin.program.telefix" name="[COLOR lime]Telefix[/COLOR] Wizard" version="1.0.0" provider-name="Telefix">
    <requires>
      <import addon="xbmc.python" version="3.0.0"/>
    </requires>
    <extension point="xbmc.python.pluginsource" library="default.py">
      <provides>executable</provides>
    </extension>
    <extension point="xbmc.addon.metadata">
      <summary lang="en">Telefix Wizard - Install + Maintenance</summary>
      <platform>all</platform>
      <assets>
        <icon>icon.png</icon>
        <fanart>fanart.jpg</fanart>
      </assets>
    </extension>
  </addon>
</addons>
```

Then:

```bash
# Create addons.xml.md5 (on Linux/Mac: md5sum addons.xml | awk '{print $1}' > addons.xml.md5)
# Or use Python:
import hashlib
with open('addons.xml') as f:
    with open('addons.xml.md5', 'w') as m:
        m.write(hashlib.md5(f.read().encode()).hexdigest())
```

Put `plugin.program.telefix-1.0.0.zip` at `zips/plugin.program.telefix/1.0.0/` (build it with `build_zip.py`, then rename to `plugin.program.telefix-1.0.0.zip`).

### 4. Install the repository addon

1. Edit `addons/repository.telefix/addon.xml`: replace `YOUR_GITHUB_USERNAME` with your GitHub username (and change URL if your repo name is not `telefix-repo`).
2. Zip `repository.telefix` (root = addon folder) and install that zip in Kodi (**Install from zip file**).
3. In Kodi: **Add-ons** → **Install from repository** → **Telefix Repository** → **Program add-ons** → **Telefix Wizard** → Install.

Repo URL format (GitHub Pages):

- `https://YOUR_USERNAME.github.io/telefix-repo/addons.xml`
- `https://YOUR_USERNAME.github.io/telefix-repo/addons.xml.md5`
- `https://YOUR_USERNAME.github.io/telefix-repo/zips`

## Bundling all addons (packages)

To refresh the 72 addon zips inside the wizard (e.g. after updates):

1. Close Kodi.
2. Run from PowerShell (in the packages folder):

```powershell
& "C:\Users\Almog\AppData\Roaming\Kodi\addons\plugin.program.telefix\resources\packages\build_all_addons.ps1"
```

Then rebuild the wizard zip with `python build_zip.py`.

## License

Use and modify as needed. Based on concepts from Chameleon/OpenWizard-style wizards.
