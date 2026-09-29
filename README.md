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

Control HUAWEI FreeBuds from Windows and Linux: battery, noise control and more. A fork of OpenFreebuds with support for FreeBuds 4, 5 and 6 and model detection by model code. Android app: https://github.com/librebuds/librebuds.

### Differences from OpenFreebuds

- FreeBuds 4, FreeBuds 5 and FreeBuds 6 drivers;
- Model-code detection: when the earbuds' Bluetooth name is not recognized (for example renamed earbuds), the app connects with an info-only probe, reads the model code the earbuds report, and picks the matching driver;
- Test vectors shared with the LibreBuds Android project, decoded by the packet parser (the drivers themselves are not exercised by these vectors);
- No upstream self-updater; updates are distributed as GitHub releases of this repository instead;
- Multipoint connect and disconnect on the new drivers (unpair is not implemented).

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

## Remote control

The application runs a built-in HTTP server for remote control and scripting.
The server starts automatically with the first application instance and
listens on `http://127.0.0.1:19823` by default. Starting the application again
while it is already running does not start a second server; the new process
detects the running one and just brings the settings window to front (unless
started with `--client`).

Endpoints:

- `GET /` serves a small built-in page that lists the available shortcuts as
  clickable links and shows how to call the endpoints below from curl or
  JavaScript;
- `GET /list_shortcuts` returns the list of available shortcut names as JSON;
- `GET /<shortcut>` runs the named shortcut (for example `mode_normal`,
  `mode_cancellation`, `mode_awareness`, `enable_low_latency`, `next_mode`,
  `toggle_connect`, `connect`, `disconnect`, `show_main_window`) and returns
  `{"result": true}` on success;
- `POST /__rpc__/<method>` calls a method of the running manager directly, for
  example `set_property` or `get_property`, with a JSON body of
  `{"args": [...], "kwargs": {...}}`. This is the same internal RPC channel
  the application itself uses when a second instance connects to the first
  one.

By default the server only listens on localhost and does not require
authorization. Open the settings window, then the extra options menu (the
gear icon button, or the File menu on macOS) → **Remote access…**, to allow
connections from other machines on the network and to turn on secret key
verification. When secret key verification is enabled, every request must
include an `X-Secret` header with the configured key, otherwise the server
answers `401 Unauthorized`. These settings are only read when the application
starts, so restart it after changing them. Allowing remote connections
exposes control of the earbuds to anyone who can reach that port, so only
enable it on a trusted network and set a secret key.

Device compatibility
------------------------

See device page to get information about supported features.
If your device isn't listed here, you could try to use it with profile for other model.

- [HUAWEI FreeBuds 3](./docs/devices/HUAWEI_FreeBuds_3.md)
- HUAWEI FreeBuds 4 (LibreBuds), experimental: battery and noise control only
- [HUAWEI FreeBuds 4i](./docs/devices/HUAWEI_FreeBuds_4i.md)
  - **HONOR Earbuds 2 / 2 SE / 2 Lite** is same
- HUAWEI FreeBuds 5 (LibreBuds): reading battery, noise control, gestures,
  auto pause, equalizer presets and multipoint status is confirmed on
  hardware. The only writes confirmed on hardware are switching the noise
  control mode and multipoint connect and disconnect. Changing the preferred
  device, noise cancellation level, gestures, auto pause, equalizer preset
  selection and multipoint on/off is not yet confirmed. Custom equalizer
  presets and auto-connect are not offered on this model, and unpairing a
  host is not supported
- [HUAWEI FreeBuds 5i](./docs/devices/HUAWEI_FreeBuds_5i.md)
- HUAWEI FreeBuds 6 (LibreBuds): reading battery, noise control, gestures,
  auto pause, equalizer presets and multipoint status is confirmed on
  hardware. The only writes confirmed on hardware are switching the noise
  control mode and multipoint connect and disconnect. Changing the preferred
  device, noise cancellation level, gestures, auto pause, equalizer preset
  selection and multipoint on/off is not yet confirmed. Custom equalizer
  presets and auto-connect are not offered on this model, and unpairing a
  host is not supported
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

May also work with newer/older devices in same series. If you want to get better compatibility of some model, you could share a Bluetooth traffic capture in [this repository's issues](https://github.com/librebuds/librebuds-windows/issues) to help making LibreBuds better. The capture approach comes from the upstream OpenFreebuds project.

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
- [Python](https://www.python.org/downloads/) (3.14), [PDM](https://pdm-project.org/en/latest/);
  - Do not Python from Microsoft Store;
- (optional) [NSIS](https://nsis.sourceforge.io/Download), [UPX](https://upx.github.io/).

**Linux**:
- [Just](https://github.com/casey/just);
- Python (3.14), [PDM](https://pdm-project.org/en/latest/);
- Qt 6.0+ development tools, at least Linguist's `lrelease`.

**macOS** (experimental, tested only on Intel-based macOS):
- [Python](https://www.python.org/downloads/) (3.14), [PDM](https://pdm-project.org/en/latest/);
  - PDM with python from website can be added via `pip3 install -U pipx && python3 -m pipx install pdm && python3 -m pipx ensurepath`;
  - For now, if using python from homebrew, you must symlink it to `python` since scripts doesn't use `python3` command;
- [Just](https://github.com/casey/just) (`brew install just`);
- Qt 6.0+ development tools, at least Linguist's `lrelease` (`brew install qttools`).

### Prepare environment

1. Get the sources together with the `vendor/librebuds` submodule:
   `git clone --recursive https://github.com/librebuds/librebuds-windows.git`,
   or run `git submodule update --init` in an existing checkout;
2. Obtain dependencies: `pdm install`;
3. Try to run it: `just start`;
4. Make release binary:
  - Windows: `just win32`;
  - Linux: `just debian fedora`;
  - macOS: `just macos`.
