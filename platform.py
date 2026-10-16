# The packages are arduino-core-edison's release archives, the same ones the Arduino Boards
# Manager installs. platform.json names them; this picks the release and, for the
# host-specific ones, this computer's archive.

from platformio import util
from platformio.exception import UserSideException
from platformio.public import PlatformBase

# The arduino-core-edison release this platform uses, and the Zig version it ships.
CORE_VERSION = "0.1.2"
ZIG_VERSION = "0.17.0"
RELEASE_URL = (
    "https://github.com/open-edison/arduino-core-edison/releases/download/v" + CORE_VERSION
)

# PlatformIO's system type -> the release's name for that host.
HOSTS = {
    "linux_x86_64": "linux-amd64",
    "linux_aarch64": "linux-arm64",
    "darwin_x86_64": "darwin-amd64",
    "darwin_arm64": "darwin-arm64",
    "windows_amd64": "windows-amd64",
}


class EdisonPlatform(PlatformBase):
    def __init__(self, manifest_path):
        super().__init__(manifest_path)
        packages = self._manifest["packages"]
        packages["framework-arduino-edison"]["version"] = (
            "%s/edison-core-%s.tar.xz" % (RELEASE_URL, CORE_VERSION)
        )
        packages["tool-edison-sysroot"]["version"] = (
            "%s/edison-sysroot-%s.tar.xz" % (RELEASE_URL, CORE_VERSION)
        )
        host = HOSTS.get(util.get_systype())
        if host is None:
            return  # configure_default_packages says so
        packages["toolchain-zig"]["version"] = "%s/edison-zig-%s-%s.tar.xz" % (
            RELEASE_URL,
            ZIG_VERSION,
            host,
        )
        packages["tool-edison"]["version"] = "%s/edison-tools-%s-%s.tar.xz" % (
            RELEASE_URL,
            CORE_VERSION,
            host,
        )

    def configure_default_packages(self, options, targets):
        if util.get_systype() not in HOSTS:
            raise UserSideException(
                "The Edison toolchain isn't built for this computer (%s); it runs on %s."
                % (util.get_systype(), ", ".join(sorted(HOSTS)))
            )
        if "arduino" in options.get("pioframework", []):
            self.packages["tool-edison-sysroot"]["optional"] = False
        return super().configure_default_packages(options, targets)
