<div align="center">
<img src="docs/logo.png" width="192px" alt="" />
<h1>LibreBuds for Windows</h1>
<p>Desktop application to manage wireless headphones from HUAWEI/Honor</p>
<p>
<a href="https://github.com/librebuds/librebuds-windows/actions/workflows/on_push.yml">
<img src="https://github.com/librebuds/librebuds-windows/actions/workflows/on_push.yml/badge.svg" alt="Test build status"/>
</a>
</p>
<p>Based on <a href="https://github.com/melianmiko/OpenFreebuds">OpenFreebuds</a> by melianmiko and contributors (GPL-3.0).</p>
<p>
<a href="https://github.com/librebuds/librebuds-windows/releases"><b>💿 Download binaries</b></a> | <a href="https://github.com/librebuds/librebuds-windows/issues"><b>❓ Issues / help</b></a>
</p>
<p>
<img alt="Tray menu preview" src="docs/preview_0.png" />
</p>
</div>

This application allows to control HUAWEI FreeBuds earphone settings from PC. Check exact battery level, toggle noise cancellation, control built-in equalizer, change gestures, and all other in-device settings and features are now available without official mobile application.

Features
---------

- Dynamic system tray icon that shows current active noise cancellation mode and battery level;
- Tray menu with battery levels and active noise cancellation settings;
- Optional separate numeric tray icons for the left earbud, right earbud, and charging case;
- Ability to change voice language (not all devices supported);
- Device settings dialog, eg. change equalizer preset, gesture actions, etc;
- Built-in HTTP-server for remote control & scripting;
- Built-in global hotkeys support (for Windows and Xorg-Linux)

![Settings preview](docs/preview_1.png)

### Battery tray indicators

Enable **Application → Tray battery → Show battery percentages in the system tray**
to display each reported earbud/case level as a separate number, without a `%` sign.
The indicators are disabled by default. Each indicator has independent text and
background colors, optional transparency, Normal/Bold font weight (Bold by default),
and text size from 50% to 100% of the largest size that fits its tray icon. The preview uses sample battery levels;
changes are saved and applied immediately.

Hover over an indicator to identify the earbud or case. Left-click opens the
settings window, and right-click opens the existing tray menu. Indicators hide
when disconnected, disabled, or when their individual battery level is unavailable.
Devices reporting only an aggregate battery level do not get additional indicators.

The desktop controls tray visibility and ordering. On Windows, indicators may
initially appear in the hidden-icons (`^`) menu. The application creates them in
left/right/case order, but cannot force their final position in the Windows tray.

Device compatibility
------------------------

See device page to get information about supported features.
If your device isn't listed here, you could try to use it with profile for other model.

- [HUAWEI FreeBuds 3](./docs/devices/HUAWEI_FreeBuds_3.md)
- [HUAWEI FreeBuds 4i](./docs/devices/HUAWEI_FreeBuds_4i.md)
  - **HONOR Earbuds 2 / 2 SE / 2 Lite** is same
- [HUAWEI FreeBuds 5i](./docs/devices/HUAWEI_FreeBuds_5i.md)
- [HUAWEI FreeBuds 6i](./docs/devices/HUAWEI_FreeBuds_6i.md)
- [HUAWEI FreeBuds Pro](./docs/devices/HUAWEI_FreeBuds_Pro.md)
- [HUAWEI FreeBuds Pro 2](./docs/devices/HUAWEI_FreeBuds_Pro_2.md)
- [HUAWEI FreeBuds Pro 3](./docs/devices/HUAWEI_FreeBuds_Pro_3.md)
  - **HUAWEI FreeBuds Pro 4** is same
- [HUAWEI FreeBuds SE](./docs/devices/HUAWEI_FreeBuds_SE.md)
- [HUAWEI FreeBuds SE 2](./docs/devices/HUAWEI_FreeBuds_SE_2.md)
- [HUAWEI FreeBuds SE 4 ANC](./docs/devices/HUAWEI_FreeBuds_SE_4.md)
- [HUAWEI FreeBuds Studio](./docs/devices/HUAWEI_FreeBuds_Studio.md)
- [HUAWEI FreeClip](./docs/devices/HUAWEI_FreeClip.md)
- [HUAWEI FreeClip 2](./docs/devices/HUAWEI_FreeClip_2.md)
- [HUAWEI FreeLace Pro](./docs/devices/HUAWEI_FreeLace_Pro.md)
- [HUAWEI FreeLace Pro 2](./docs/devices/HUAWEI_FreeLace_Pro_2.md)

May also work with newer/older devices in same series. If you want to get better compatibility of some model, you could [create Bluetooth traffic dump](https://mmk.pw/en/posts/ofb-contribution/) to help making LibreBuds better.

Download & install
-----------------

LibreBuds for Windows is distributed from this repository's
[GitHub Releases](https://github.com/librebuds/librebuds-windows/releases).
It does not use the upstream OpenFreebuds package manager channels (Winget,
Scoop, Flathub, APT, DNF, AUR, NixPkgs) or update server; those install the
upstream OpenFreebuds application instead.

Most recent `dev`-binaries can be found as [GitHub Actions](https://github.com/librebuds/librebuds-windows/actions/workflows/on_push.yml) build artifacts.

Build from sources
-------------

### Build dependencies

**Windows 10/11**:
- [Just](https://github.com/casey/just);
- [Python](https://www.python.org/downloads/) (3.13+), [PDM](https://pdm-project.org/en/latest/);
  - Do not Python from Microsoft Store;
- (optional) [NSIS](https://nsis.sourceforge.io/Download), [UPX](https://upx.github.io/).

**Linux**:
- [Just](https://github.com/casey/just);
- Python (3.13+), [PDM](https://pdm-project.org/en/latest/);
- Qt 6.0+ development tools, at least Linguist's `lrelease`.

**macOS** (experimental, tested only on Intel-based macOS):
- [Python](https://www.python.org/downloads/) (3.13+), [PDM](https://pdm-project.org/en/latest/);
  - PDM with python from website can be added via `pip3 install -U pipx && python3 -m pipx install pdm && python3 -m pipx ensurepath`;
  - For now, if using python from homebrew, you must symlink it to `python` since scripts doesn't use `python3` command;
- [Just](https://github.com/casey/just) (`brew install just`);
- Qt 6.0+ development tools, at least Linguist's `lrelease` (`brew install qttools`).

### Prepare environment

1. Obtain dependencies: `pdm install`;
2. Try to run it: `just start`;
3. Make release binary:
  - Windows: `just win32`;
  - Linux: `just debian fedora`;
  - macOS: `just macos`.
