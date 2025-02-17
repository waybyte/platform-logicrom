# Copyright 2024 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join
from rdautils import gen_lod_file, gen_fota_file
from platformio.util import get_systype

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-logicromarduino")
assert isdir(FRAMEWORK_DIR)

LOGICROMSDK_DIR = join(FRAMEWORK_DIR, "cores", board.get("build.core"), "logicromsdk")
assert isdir(LOGICROMSDK_DIR)

# RDA Tools
if "windows" in get_systype():
    systype = "win32"
else:
    systype = "linux"

tool_path = join(LOGICROMSDK_DIR, "tools", "rda8955")

env.Replace(
    FOTACREATE=join(tool_path, systype, "genfota"),
)

# Generate linker script
linker_script = env.Command(
    join("$BUILD_DIR", "linkerscript_out.ld"),
    join(
        LOGICROMSDK_DIR, "lib", "rda8955", "linkerscript.ld"
    ),
    env.VerboseAction(
        '$CC -I"' + join(FRAMEWORK_DIR, "lib", "rda8955") + '" -P -x c -E $SOURCE -o $TARGET',
        "Generating LD script $TARGET",
    ),
)
env.Depends(join("$BUILD_DIR", "$PROGNAME" + "$PROGSUFFIX"), linker_script)
env.Replace(LDSCRIPT_PATH="linkerscript_out.ld")


# Setup ENV
env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-g",
        "-fmessage-length=0",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-fsigned-char",
        "-fno-strict-aliasing",
        "-Wall",
        "-march=xcpu",
        "-mtune=xcpu",
        "-Wa,-march=xcpu,-mtune=xcpu",
        "-mips16",
        "-minterlink-mips16",
        "-msoft-float",
        "-mexplicit-relocs",
        "-mmemcpy",
        "-mmips-tfile",
        "-DEL", "-EL", "-G0",
        "-ffixed-t3", "-ffixed-t4", "-ffixed-t5", "-ffixed-t6", "-ffixed-t7",
        "-ffixed-s2", "-ffixed-s3", "-ffixed-s4", "-ffixed-s5", "-ffixed-s6", "-ffixed-s7",
        "-ffixed-fp",
    ],

    CFLAGS=[
        "-std=gnu99"
    ],

    CXXFLAGS=[
        "-std=gnu++98",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
        "-fno-threadsafe-statics",
    ],

    CPPDEFINES=[
        ("__BUFSIZ__", "512"),
        ("__FILENAME_MAX__", "256"),
        ("F_CPU", "$BOARD_F_CPU"),
		("ARDUINO", 10816),
		"ARDUINO_ARCH_MIPS",
        ("ARDUINO_VARIANT", '\\"%s\\"' % board.get("build.variant").replace('"', "")),
        ("ARDUINO_BOARD", '\\"%s\\"' % board.get("name").replace('"', "")),
        ("SOC_%s" % board.get("build.mcu").upper().replace('"', ""), "1"),
        ("PLATFORM_%s" % board.get("build.variant").upper().replace('"', ""), "1"),
    ],

    CPPPATH=[
        join(LOGICROMSDK_DIR, "include"),
        join(LOGICROMSDK_DIR, "include", "ril"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core")),
    ],

    LINKFLAGS=[
        "-march=xcpu",
        "-mtune=xcpu",
        "-Wa,-march=xcpu,-mtune=xcpu",
        "-mips16",
        "-minterlink-mips16",
        "-msoft-float",
        "-mexplicit-relocs",
        "-mmemcpy",
        "-mmips-tfile",
        "-DEL", "-EL", "-G0",
        "-Os", "-g",
        "-Wl,--gc-sections,--relax",
        "--oformat=elf32-littlemips",
        "-nostartfiles",
        "-nostdlib",
        "-nostartfiles",
        "-nodefaultlibs",
        "-u", "main",
        "-u", "io_pin2gpio",
        "-u", "variant_init",
    ],

    LIBS=["rda_logicrom", "c", "gcc", "m"],

    LIBPATH=[
        join(LOGICROMSDK_DIR, "lib", "rda8955")
    ],

    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(gen_lod_file, "Generating $TARGET"),
            suffix=".lod"
        ),
        BinToFOTA=Builder(
            action=env.VerboseAction(gen_fota_file, "Generating FOTA firmware $TARGET"),
            suffix=".bin"
        )
    )
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])


def load_logicrom_debug():
    for i, libs in enumerate(env["LIBS"]):
        if libs.startswith("rda_logicrom"):
            env["LIBS"][i] = libs + "_debug"


if board.get("build.logicromtype") == "debug":
    load_logicrom_debug()

if env.GetBuildType() == "debug":
    load_logicrom_debug()

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"))
    ))

envsafe = env.Clone()

libs.append(envsafe.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", board.get("build.core"))
))

env.Prepend(LIBS=libs)
