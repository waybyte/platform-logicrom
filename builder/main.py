# Copyright 2021 WAYBYTE Solutions
#
# SPDX-License-Identifier: MIT
#

import sys
from platform import system
from platformio.util import get_systype
from os import makedirs
from os.path import basename, isdir, join

from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, AlwaysBuild,
                          Builder, Default, DefaultEnvironment)

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
flasher_path = platform.get_package_dir("tool-siwiflasher") or ""

def _get_board_mcu():
    return board.get("build.mcu")

env.Replace(
    __get_board_mcu=_get_board_mcu,

    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    GDB="arm-none-eabi-gdb",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ARFLAGS=["rc"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARM.exidx|\.ARM.extab|\.ll|\.initdata)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGSUFFIX=".elf"
)

# Setup tools based on system type
if "windows" in get_systype() and board.get("build.mcu") != "MT2625":
    env.Replace(
        SIWIFLASHER=join(flasher_path, "siwiflasher"),
        REFLASH_FLAGS=[
            "-r",
            "-b", "$UPLOAD_SPEED",
            "-p", '"$UPLOAD_PORT"',
        ],
        REFLASH_CMD='"$SIWIFLASHER" $REFLASH_FLAGS'
    )
else:
    env.Replace(
        SIWIFLASHER='"$PYTHONEXE" ' + join(flasher_path, "siwiflasher.py"),
        REFLASH_CMD='echo "Sorry! Reflashing is only supported on windows! :("'
    )

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.bin")
    target_firm_fota = join("$BUILD_DIR", "fota_${PROGNAME}.bin")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToBin(join("$BUILD_DIR", "${PROGNAME}"), target_elf)
    target_firm_fota = env.BinToFOTA(
        join("$BUILD_DIR", "fota_${PROGNAME}"), target_firm)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Build FOTA Binary
#

target_buildota = env.Alias("buildfota", target_firm_fota, target_firm_fota)
AlwaysBuild(target_buildota)

#
# Target: Print binary size
#

target_size = env.Alias("size", target_elf, env.VerboseAction(
    "$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Reflash core
#
AlwaysBuild(
    env.Alias("reflash", None, [
        env.VerboseAction("$REFLASH_CMD", "Reflashing core...")
    ]))

#
# Target: Upload by default .bin file
#
env.Replace(
    UPLOADER="$SIWIFLASHER",
    UPLOADERFLAGS=[
        "-b", "$UPLOAD_SPEED",
        "-p", '"$UPLOAD_PORT"',
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS $SOURCE'
)
upload_source = target_firm
upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

if "windows" not in get_systype() or board.get("build.mcu") == "MT2625":
    env.Append(
        UPLOADERFLAGS=[
            "-m", '"${__get_board_mcu()}"',
        ]
    )

if "windows" in get_systype() and board.get("build.mcu") != "MT2625" and env.subst("$UPLOAD_PORT") == "":
    env.Append(
        UPLOADERFLAGS=[
            "-u"
        ],
        REFLASH_FLAGS=[
            "-u"
        ]
    )
else:
    upload_actions.insert(0, env.VerboseAction(env.AutodetectUploadPort,
        "Looking for upload port..."))

AlwaysBuild(env.Alias("upload", upload_source, upload_actions))

#
# Setup default targets
#

Default([target_buildprog, target_buildota, target_size])
