# Contributing to platform-edison

## Develop and test

Point a project at your checkout instead of a release:

```ini
platform = symlink:///path/to/platform-edison
```

To build against local packages (from arduino-core-edison's `tools/package.sh`, which
writes them to its `dist/release/`), override them too:

```ini
platform_packages =
    framework-arduino-edison@file:///path/to/edison-core-0.1.0.tar.xz
    tool-edison-sysroot@file:///path/to/edison-sysroot-0.1.0.tar.xz
    toolchain-zig@file:///path/to/edison-zig-0.17.0-linux-amd64.tar.xz
    tool-edison@file:///path/to/edison-tools-0.1.0-linux-amd64.tar.xz
```

Pick your computer's `toolchain-zig` and `tool-edison` archives. Set `PLATFORMIO_CORE_DIR`
to a scratch folder to keep test installs out of your own `~/.platformio`.

## Layout

| Path | Purpose |
|---|---|
| `platform.json` | The platform and its packages (versions filled in by `platform.py`) |
| `platform.py` | Picks the arduino-core-edison release (`CORE_VERSION`) and this host's archives |
| `boards/edison.json` | The board |
| `builder/main.py` | Zig toolchain flags (as the core's `platform.txt`) and the upload target |
| `builder/frameworks/arduino.py` | Builds the core and variant, links libgpiod |
| `examples/` | Example projects, built by CI |

## CI

`.github/workflows/examples.yml` builds every example on Linux, Windows and macOS (arm64 and
x86_64), with the examples pointed at the checkout and the packages downloaded from the
core release named in `platform.py`.

## Releasing

1. When the core has a new release, set `CORE_VERSION` in `platform.py` to it.
2. Set `version` in `platform.json`, and point the `platform =` lines in the README and the
   examples at the new tag's archive URL.
3. Push, and once CI is green and an upload has been tested on a real board, tag and push:
   `git tag -a v0.2.0 -m "platform-edison v0.2.0"` then `git push origin v0.2.0`.
4. Create the GitHub release, with the `platformio.ini` lines in its notes:
   `gh release create v0.2.0 --verify-tag --title "platform-edison v0.2.0" --notes-file NOTES.md`.

## Conventions

- **Commits:** [Conventional Commits](https://www.conventionalcommits.org)
  (`feat: ...`, `fix(upload): ...`, `docs: ...`).
- **Mirror the core:** build flags follow arduino-core-edison's `platform.txt`; change both
  together.
- **Workflow actions:** pin to the commit SHA of the latest release, with the version in a
  comment (`actions/checkout@<sha> # v7.0.1`). Actions published as immutable releases use
  their exact tag instead (`astral-sh/setup-uv@v10.3.0`). Dependabot opens one grouped pull
  request a month with updates.
- **Hardware changes need a hardware test.** Note what you tested on a real board in the
  pull request; findings go in
  [edison-docs](https://github.com/edison-revival/edison-docs).
