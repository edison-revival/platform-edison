# Builds programs for the Edison with Zig (x86_64 Linux, Debian 13's glibc 2.41) and
# uploads them over SSH with edison-upload, as arduino-core-edison's platform.txt does.

import re
import subprocess
import sys
from os.path import join

from SCons.Script import ARGUMENTS, AlwaysBuild, Default, DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

TARGET = "x86_64-linux-gnu.2.41"

# "zig cc" etc. are split into two arguments, so zig goes on the PATH rather than being
# named by its full path (which may contain spaces).
env.PrependENVPath("PATH", platform.get_package_dir("toolchain-zig"))
env.Replace(
    AR="zig ar",
    AS="zig cc",
    CC="zig cc",
    CXX="zig c++",
    LINK="zig c++",
    RANLIB="zig ranlib",
    ARFLAGS=["rc"],
    PROGSUFFIX=".elf",
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

env.Append(
    ASFLAGS=["-target", TARGET],
    CCFLAGS=["-target", TARGET, "-Os", "-ffunction-sections", "-fdata-sections"],
    CFLAGS=["-std=gnu11"],
    CXXFLAGS=["-std=gnu++17"],
    LINKFLAGS=["-target", TARGET, "-Wl,--gc-sections", "-s"],
    LIBS=["pthread"],
)

#
# Target: Build executable program
#

target_elf = env.BuildProgram()

#
# Target: Upload
#

# A serial port means the board on the USB cable (edison-upload then uses the USB network
# link); anything else is the board's network address.
SERIAL_PORT = re.compile(r"^(COM\d+|/dev/|\\\\\.\\)", re.IGNORECASE)


def upload(target, source, env):  # pylint: disable=unused-argument
    port = env.subst("$UPLOAD_PORT")
    if port and not SERIAL_PORT.match(port):
        args = ["-protocol=network", "-port=" + port]
    else:
        args = ["-protocol=serial"]
    if int(ARGUMENTS.get("PIOVERBOSE", 0)):
        args.append("-v")
    flags = env.get("UPLOAD_FLAGS") or []
    if isinstance(flags, str):
        flags = flags.split()
    exe = "edison-upload.exe" if sys.platform == "win32" else "edison-upload"
    cmd = [join(platform.get_package_dir("tool-edison"), exe)]
    cmd += args + [env.subst(f) for f in flags] + [source[0].get_abspath()]
    return subprocess.call(cmd)


AlwaysBuild(env.Alias("upload", target_elf, env.VerboseAction(upload, "Uploading $SOURCE")))

#
# Default targets
#

Default([target_elf])
