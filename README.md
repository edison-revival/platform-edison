# platform-edison

A [PlatformIO](https://platformio.org) platform for the Intel Edison (Kit for Arduino)
running [edison-image](https://github.com/edison-revival/edison-image). Part of
[edison-revival](https://github.com/edison-revival).

It builds with [arduino-core-edison](https://github.com/edison-revival/arduino-core-edison),
the same core, compiler (Zig) and uploader as the Arduino IDE uses, installed from that
core's release archives. Sketches are compiled on your computer into a Linux program and
uploaded over SSH; edison-image runs it as the `edison-sketch` service.

Hosts: Windows x64, macOS (Apple silicon and Intel), Linux x64 and arm64.

## Use

`platformio.ini`:

```ini
[env:edison]
platform = https://github.com/edison-revival/platform-edison/archive/refs/tags/v0.1.0.zip
board = edison
framework = arduino
```

This installs a release (see [Releases](https://github.com/edison-revival/platform-edison/releases)
for the latest) without needing git. With git installed,
`https://github.com/edison-revival/platform-edison.git#v0.1.0` works too, and without the
`#v0.1.0` follows the development version.

See [examples/](examples) for Blink, Serial and elapsedMillis projects.

### Uploading

`pio run -t upload` uploads:

- **over USB** (the J16 port) when `upload_port` is unset or is the board's serial port,
  through the USB network link on the same cable;
- **over the network** when `upload_port` is the board's address, e.g.
  `upload_port = edison.local`.

The first upload from a computer needs the board's `edison` password, to install this
computer's key on the board; later uploads use the key. Give it once on the command line:

```sh
PLATFORMIO_UPLOAD_FLAGS="-password=YOUR_PASSWORD" pio run -t upload   # Linux/macOS
```

```powershell
$env:PLATFORMIO_UPLOAD_FLAGS = "-password=YOUR_PASSWORD"; pio run -t upload   # Windows
```

The key is shared with the Arduino IDE, so a computer that has uploaded from the IDE
doesn't need this. If the board at an address changes (a reflash, or another board), the
upload stops with a host key error; see the
[arduino-core-edison README](https://github.com/edison-revival/arduino-core-edison#uploading).

### Serial monitor

`Serial` is the board's USB serial port on J16: `pio device monitor`. If the computer has
other serial ports, set `monitor_port` (on Linux, `/dev/serial/by-id/usb-edison-revival_*`
picks the Edison).

## How the packages are pinned

[platform.py](platform.py) names the arduino-core-edison release (`CORE_VERSION`) and picks
this computer's archives from it: `framework-arduino-edison` (the core),
`tool-edison-sysroot` (libgpiod), `toolchain-zig` and `tool-edison` (the uploader). The
release's `SHA256SUMS` lists their checksums; PlatformIO doesn't check them itself for
packages installed by URL.

To build against local archives (from the core's `tools/package.sh`), override them in
`platformio.ini`:

```ini
platform_packages =
    framework-arduino-edison@file:///path/to/edison-core-0.1.0.tar.xz
    tool-edison-sysroot@file:///path/to/edison-sysroot-0.1.0.tar.xz
    toolchain-zig@file:///path/to/edison-zig-0.17.0-linux-amd64.tar.xz
    tool-edison@file:///path/to/edison-tools-0.1.0-linux-amd64.tar.xz
```

## Releasing

Update `CORE_VERSION` in [platform.py](platform.py) when the core has a new release, and
`version` in [platform.json](platform.json). Then point the `platform =` lines above and in
the examples at the new tag, push, and once CI passes, tag `vX.Y.Z` and create a GitHub
release for it.

## License

MIT; see [LICENSE](LICENSE). The core it installs is LGPL-2.1-or-later.
