# Telefix

Kodi wizard + repository: one-click install of the Telefix setup (Bingie skin, Mando, Telemedia, and addons) and Chameleon-style maintenance (clear cache, packages, thumbnails).

## Contents

- **plugin.program.telefix** – Telefix Wizard addon (install + maintenance menu)
- **repository.telefix** – Kodi repository addon so you can install the wizard from this GitHub repo

## Install from GitHub

1. **Install the repository addon once (from zip)**
   - Download [repository.telefix](https://github.com/AlmogLach/telefix/archive/refs/heads/main.zip), extract, zip the `repository.telefix` folder (so the zip contains `repository.telefix/addon.xml`).
   - In Kodi: Add-ons → Install from zip file → select that zip.
   - Edit the repo URL: in `addon.xml` replace `YOUR_GITHUB_USERNAME` with `AlmogLach` and use this repo’s raw/Pages URL for `addons.xml` (see below).

2. **Or use GitHub Pages (recommended)**
   - In this repo: Settings → Pages → Source: Deploy from branch → main → Save.
   - Add `addons.xml` and `addons.xml.md5` to the repo root (generate with `python plugin.program.telefix/repo_gen_addons_xml.py`).
   - Put the wizard zip at `zips/plugin.program.telefix/1.0.0/plugin.program.telefix-1.0.0.zip`.
   - In `repository.telefix/addon.xml` set:
     - `info`: `https://almoglach.github.io/telefix/addons.xml`
     - `checksum`: `https://almoglach.github.io/telefix/addons.xml.md5`
     - `datadir`: `https://almoglach.github.io/telefix/zips`
   - Then in Kodi: Install from repository → Telefix Repository → Program add-ons → Telefix Wizard.

## Build wizard zip (for “Install from zip”)

From the `plugin.program.telefix` folder:

```bash
python build_zip.py
```

Output: `plugin.program.telefix.zip` (use in Kodi: Add-ons → Install from zip file).

## Bundle all addons (packages)

To include the full set of addons in the wizard, close Kodi and run:

```powershell
& ".\plugin.program.telefix\resources\packages\build_all_addons.ps1"
```

Then run `build_zip.py` again. See `plugin.program.telefix/README.md` for details.
