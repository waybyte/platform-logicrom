# Copyright 2020 SiWi Embedded Solutions Pvt. Ltd.
#
# SPDX-License-Identifier: MIT
#

import os
from os.path import isdir, isfile, join, dirname
from shutil import copyfile

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-siwisdk")
assert isdir(FRAMEWORK_DIR)

# Create Project Template
main_c = join(env.subst("$PROJECT_DIR"), "src", "main.c")
if False == isfile(main_c):
    copyfile(join(FRAMEWORK_DIR, "template", "main.c"), main_c)

GFH_Generator = join(FRAMEWORK_DIR,
                     "tools",
                     "GFH_Generator.exe")
FOTA_Generator = join(FRAMEWORK_DIR,
                      "tools",
                      "FOTA_Generator.exe")


def gen_bin_file(target, source, env):
    cmd = ["$OBJCOPY"]
    (target_firm, ) = target
    (target_elf, ) = source

    temp_firm = os.path.dirname(target_firm.get_abspath()) + "\\temp.bin"
    cmd.extend(["-O", "binary"])
    cmd.append(target_elf.get_abspath())
    cmd.append(temp_firm)
    env.Execute(env.VerboseAction(" ".join(cmd), "Elf to Binary"))

    cmd_gfh = [GFH_Generator]
    cmd_gfh.append(temp_firm)
    cmd_gfh.append(target_firm.get_abspath())
    env.Execute(env.VerboseAction(" ".join(cmd_gfh), "Adding GFH Header"))

    os.remove(temp_firm)


# Setup ENV
env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",  # optimize for size
                "-g",
                "-march=armv5te",
                "-mfloat-abi=soft",
                "-fmessage-length=0",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
                "-fsigned-char",
        "-Wall",
        "-mthumb",
                "-mthumb-interwork",
                "-std=gnu11"
    ],

    CXXFLAGS=[
        "-std=gnu++11",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
        "-fno-threadsafe-statics"
    ],

    CPPDEFINES=[
        ("__BUFSIZ__", "512"),
        ("__FILENAME_MAX__", "256")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "include"),
        join(FRAMEWORK_DIR, "include", "ril")
    ],

    LINKFLAGS=[
        "-march=armv5te",
        "-mthumb",
        "-mthumb-interwork",
        "-mfloat-abi=soft",
        "-Os",
        "-Wl,--gc-sections,--relax",
        "-nostartfiles",
        "-nostdlib",
        "-nostartfiles",
        "-nodefaultlibs"
    ],

    LIBS=["siwisdk", "c", "gcc", "m"],
    LDSCRIPT_PATH=join(FRAMEWORK_DIR, "lib", "linkerscript.ld"),
    LIBPATH=[
        join(FRAMEWORK_DIR, "lib")
    ],
    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(gen_bin_file, "Generating $TARGET"),
            suffix=".bin"
        ),
        BinToFOTA=Builder(
            action=env.VerboseAction(" ".join([
                FOTA_Generator,
                "$SOURCES",
                "$TARGET"
            ]), "Creating FOTA firmware $TARGET"),
            suffix=".bin"
        )
    )
)

if board.get("build.newlib") == "nano":
    env.Append(
        LINKFLAGS=[
            "--specs=nano.specs",
            "-u _printf_float",
            "-u _scanf_float",
            "--specs=nosys.specs"
        ]
    )

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])


def load_siwilib_debug():
    for i, libs in enumerate(env["LIBS"]):
        if libs == "siwisdk":
            env["LIBS"][i] = "siwisdk_debug"


if board.get("build.siwilib") == "debug":
    load_siwilib_debug()

if env.GetBuildType() == "debug":
    load_siwilib_debug()
