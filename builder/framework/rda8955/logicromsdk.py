# Copyright 2023 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

from os.path import isdir, isfile, join
from shutil import copyfile
from rdautils import gen_lod_file, gen_fota_file

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

tool_path = join(FRAMEWORK_DIR, "tools", "rda8955")

env.Replace(
    FOTACREATE=join(tool_path, systype, "genfota"),
)

# Generate linker script
linker_script = env.Command(
    join("$BUILD_DIR", "linkerscript_out.ld"),
    join(
        FRAMEWORK_DIR, "lib", "rda8955", "linkerscript.ld"
    ),
    env.VerboseAction(
        '$CC -I"' + join(FRAMEWORK_DIR, "lib", "rda8955") + '" -P -x c -E $SOURCE -o $TARGET',
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


# Setup ENV
env.Append(
    ASFLAGS=["-DCT_ASM"],

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
        ("__FILENAME_MAX__", "256")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "include"),
        join(FRAMEWORK_DIR, "include", "ril")
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
    ],

    LIBS=["rda_logicrom", "c", "gcc", "m"],

    LIBPATH=[
        join(FRAMEWORK_DIR, "lib", "rda8955")
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

# copy CCFLAGS to ASFLAGS
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

def load_logicrom_debug():
    for i, libs in enumerate(env["LIBS"]):
        if libs.startswith("rda_logicrom"):
            env["LIBS"][i] = libs + "_debug"

if board.get("build.logicromtype") == "debug":
    load_logicrom_debug()

if env.GetBuildType() == "debug":
    load_logicrom_debug()
