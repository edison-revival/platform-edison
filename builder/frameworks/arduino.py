# The Arduino framework: arduino-core-edison, built as its platform.txt builds it. Sketches
# run as a Linux program on the board and link libgpiod (from tool-edison-sysroot).

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-edison")
SYSROOT_DIR = platform.get_package_dir("tool-edison-sysroot")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)
assert SYSROOT_DIR and isdir(SYSROOT_DIR)

CORE_DIR = join(FRAMEWORK_DIR, "cores", board.get("build.core"))
VARIANT_DIR = join(FRAMEWORK_DIR, "variants", board.get("build.variant"))

env.Append(
    CPPDEFINES=[
        "HOST",
        ("ARDUINO", 10819),
        "ARDUINO_" + board.get("build.board"),
        "ARDUINO_ARCH_EDISON",
    ],
    CCFLAGS=["-isystem", join(SYSROOT_DIR, "include")],
    CXXFLAGS=["-Wno-main"],
    CPPPATH=[
        CORE_DIR,
        join(CORE_DIR, "api", "deprecated"),
        join(CORE_DIR, "api", "deprecated-avr-comp"),
        VARIANT_DIR,
    ],
    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],
    LIBS=[env.File(join(SYSROOT_DIR, "lib", "libgpiod.so.3"))],
)

# The variant as objects (so its definitions always link), the core as a library.
env.BuildSources(join("$BUILD_DIR", "FrameworkArduinoVariant"), VARIANT_DIR)
env.Prepend(LIBS=[env.BuildLibrary(join("$BUILD_DIR", "FrameworkArduino"), CORE_DIR)])
