# Copyright 2023 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

from os.path import isdir, isfile, join
from shutil import copyfile
from asrutils import gen_release_file, gen_fota_file
from platformio.util import get_systype

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-logicromsdk")
assert isdir(FRAMEWORK_DIR)

# RDA Tools
if "windows" in get_systype():
    systype = "win32"
else:
    systype = "linux"

# Generate linker script
linker_script = env.Command(
    join("$BUILD_DIR", "linkerscript_out.ld"),
    join(
        FRAMEWORK_DIR, "lib", "asr160x", "app_linker.ld"
    ),
    env.VerboseAction(
        '$CC -I"' + join(FRAMEWORK_DIR, "lib", "asr160x") + '" -DFLASHSZ_' + board.get("build.flashsz") + '  -P -x c -E $SOURCE -o $TARGET',
        "Generating LD script $TARGET",
    ),
)
env.Depends(join("$BUILD_DIR", "$PROGNAME" + "$PROGSUFFIX"), linker_script)
env.Replace(LDSCRIPT_PATH="linkerscript_out.ld")

# Create Project Template
main_c = join(env.subst("$PROJECT_DIR"), "src", "main.c")
main_cpp = join(env.subst("$PROJECT_DIR"), "src", "main.cpp")
if (False == isfile(main_c)) and (False == isfile(main_cpp)):
    copyfile(join(FRAMEWORK_DIR, "template", "main.c.tmpl"), main_c)

def gen_zip_file(target, source, env):
    (target_firm, ) = target
    (source_elf, ) = source
    imagepath = join(FRAMEWORK_DIR, "lib", "asr160x", "pack")
    gen_release_file(target_firm, source_elf, imagepath, env)


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
        "-mthumb",
        "-mthumb-interwork",
        "-mcpu=cortex-r4",
        "-march=armv7-r",
        "-mfloat-abi=soft",
        "-mno-unaligned-access",
    ],

    CFLAGS=[
        "-std=gnu11"
    ],

    CXXFLAGS=[
        "-std=gnu++11",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
        "-fno-threadsafe-statics",
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
        "-mthumb",
        "-mthumb-interwork",
        "-mcpu=cortex-r4",
        "-march=armv7-r",
        "-mfloat-abi=soft",
        "-mno-unaligned-access",
        "-Os",
        "-Wl,--gc-sections,--relax",
        "-nostartfiles",
        "-nostdlib",
        "-nostartfiles",
        "-nodefaultlibs",
    ],

    LIBS=["logicromasr", "c", "gcc", "m"],

    LIBPATH=[
        join(FRAMEWORK_DIR, "lib"),
        join(FRAMEWORK_DIR, "lib", "asr160x"),
    ],

    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(gen_zip_file, "Generating $TARGET"),
            suffix=".zip"
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
        if libs.startswith("logicrom"):
            env["LIBS"][i] = libs + "_debug"


if board.get("build.logicromtype") == "debug":
    load_logicrom_debug()

if env.GetBuildType() == "debug":
    load_logicrom_debug()
