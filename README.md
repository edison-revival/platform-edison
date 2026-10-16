# platform-edison

A [PlatformIO](https://platformio.org) platform for the Intel Edison (Kit for Arduino)
running [edison-image](https://github.com/open-edison/edison-image). Part of
[open-edison](https://github.com/open-edison).

It builds with [arduino-core-edison](https://github.com/open-edison/arduino-core-edison),
the same core, compiler (Zig) and uploader as the Arduino IDE uses, installed from that
core's release archives. Sketches are compiled on your computer into a Linux program and
uploaded over SSH; edison-image runs it as the `edison-sketch` service.

Hosts: Windows x64, macOS (Apple silicon and Intel), Linux x64 and arm64.

## Use

`platformio.ini`:

```ini
[env:edison]
platform = https://github.com/open-edison/platform-edison/archive/refs/tags/v0.1.1.zip
board = edison
framework = arduino
```

This installs a release (see [Releases](https://github.com/open-edison/platform-edison/releases)
for the latest) without needing git. With git installed,
`https://github.com/open-edison/platform-edison.git#v0.1.1` works too, and without the
`#v0.1.1` follows the development version.

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
[arduino-core-edison README](https://github.com/open-edison/arduino-core-edison#uploading).

### Serial monitor

`Serial` is the board's USB serial port on J16: `pio device monitor` finds it by its USB
ID (`1d6b:0104`), even with other serial ports connected. That ID is Linux's generic one
for USB gadgets, so if another Linux gadget device (a Raspberry Pi in gadget mode, say) is
connected too, set `monitor_port` (on Linux, `/dev/serial/by-id/usb-open-edison_*`
picks the Edison).

## How the packages are pinned

[platform.py](platform.py) names the arduino-core-edison release (`CORE_VERSION`) and picks
this computer's archives from it: `framework-arduino-edison` (the core),
`tool-edison-sysroot` (libgpiod), `toolchain-zig` and `tool-edison` (the uploader). The
release's `SHA256SUMS` lists their checksums; PlatformIO doesn't check them itself for
packages installed by URL.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for building against local packages, CI, releasing
and conventions.

## License

MIT; see [LICENSE](LICENSE). The core it installs is LGPL-2.1-or-later.
