# Copyright 2021 Waybyte Solutions
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
from json import load
from rdautils import mkimage, gen_fota_file
from platformio.util import get_systype

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-logicromarduino")
assert isdir(FRAMEWORK_DIR)

LOGICROMSDK_DIR = join(FRAMEWORK_DIR, "cores", board.get("build.core"), "logicromsdk")
assert isdir(LOGICROMSDK_DIR)

# Load core configuration
with open(join(LOGICROMSDK_DIR, "lib", "rda8910", "core_config.json")) as f:
    core_config = load(f)
    f.close()

# RDA Tools
if "windows" in get_systype():
    systype = "win32"
else:
    systype = "linux"

tool_path = join(LOGICROMSDK_DIR, "tools", "rda8910")

env.Replace(
    DTOOLS=join(tool_path, systype, "dtools"),
    MKIMAGE='$DTOOLS' + " mkappimg",
    PACGEN='$PYTHONEXE ' + join(tool_path, "pacgen.py"),
    FOTAGEN='$DTOOLS' + " fotacreate2",
)

# Generate linker script
linker_script = env.Command(
    join("$BUILD_DIR", "linkerscript_out.ld"),
    join(
        LOGICROMSDK_DIR, "lib", "rda8910", "app_flashimg.ld"
    ),
    env.VerboseAction(
        '$CC -I"' + join(FRAMEWORK_DIR, "lib", "rda8910") + '" -P -x c -E $SOURCE -o $TARGET',
        "Generating LD script $TARGET",
    ),
)
env.Depends(join("$BUILD_DIR", "$PROGNAME" + "$PROGSUFFIX"), linker_script)
env.Replace(LDSCRIPT_PATH="linkerscript_out.ld")


def gen_pac_file(target, source, env):
    (target_firm, ) = target
    (source_elf, ) = source

    # Generate image file
    if "darwin" in get_systype():
        print("Generating Firmware Image")
        mkimage(target, source, env)
    else:
        env.Execute(
            env.VerboseAction("$MKIMAGE " + source_elf.get_abspath() + ' ' + join("$BUILD_DIR", env.subst("$PROGNAME") + '.img'),
                              "Generating Firmware Image")
        )

    # Generate pac file
    init_fdl = [
        'cfg-init', '--pname', '"UIX8910_MODEM"', '--palias', '"$PROGNAME"',
        '--pversion', '"8910 MODULE"', '--version', '"BP_R1.0.0"',
        '--flashtype', '1',
        'cfg-host-fdl', '-a', core_config["CONFIG_FDL1_IMAGE_START"], '-s', core_config["CONFIG_FDL1_IMAGE_SIZE"],
        '-p', join(LOGICROMSDK_DIR, 'lib', 'rda8910', 'fdl1.img'),
        'cfg-fdl2', '-a', core_config["CONFIG_FDL2_IMAGE_START"], '-s', core_config["CONFIG_FDL2_IMAGE_SIZE"],
        '-p', join(LOGICROMSDK_DIR, 'lib', 'rda8910', 'fdl2.img'),
    ]

    pac_nvitem = [
        'cfg-nvitem', '-n', '"Calibration"', '-i', '0xFFFFFFFF', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"GSM Calibration"', '-i', '0x26d', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"LTE Calibration"', '-i', '0x26e', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"IMEI"', '-i', '0xFFFFFFFF', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"BT_Config"', '-i', '0x191', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"Logicrom"', '-i', '0x280', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"Customer"', '-i', '0x27e', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"System Proxy"', '-i', '0x281', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
    ]

    pac_app = [
        'cfg-image', '-i', 'APPIMG', '-a', core_config["CONFIG_APPIMG_FLASH_ADDRESS"], '-s', core_config["CONFIG_APPIMG_FLASH_SIZE"],
  		    '-p', join("$BUILD_DIR", env.subst("$PROGNAME") + '.img')
    ]

    pac_cmd = [
        "$PACGEN",
        " ".join(init_fdl),
        " ".join(pac_nvitem),
        " ".join(pac_app),
        "pac-gen", target_firm.get_abspath()
    ]
    env.Execute(env.VerboseAction(" ".join(pac_cmd), " "))


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
        "-mcpu=cortex-a5",
        "-mtune=generic-armv7-a",
        "-mfpu=neon-vfpv4",
        "-mfloat-abi=hard",
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
        ("__FILENAME_MAX__", "256"),
        ("F_CPU", "$BOARD_F_CPU"),
		("ARDUINO", 10816),
		"ARDUINO_ARCH_ARM",
        ("ARDUINO_VARIANT", '\\"%s\\"' % board.get("build.variant").replace('"', "")),
        ("ARDUINO_BOARD", '\\"%s\\"' % board.get("name").replace('"', "")),
    ],

    CPPPATH=[
        join(LOGICROMSDK_DIR, "include"),
        join(LOGICROMSDK_DIR, "include", "ril"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core")),
    ],

    LINKFLAGS=[
        "-mthumb",
        "-mthumb-interwork",
        "-mcpu=cortex-a5",
        "-mtune=generic-armv7-a",
        "-mfpu=neon-vfpv4",
        "-mfloat-abi=hard",
        "-mno-unaligned-access",
        "-Os",
        "-Wl,--gc-sections,--relax",
        "-nostartfiles",
        "-nostdlib",
        "-nostartfiles",
        "-nodefaultlibs",
        "-u", "main",
        "-Wl,--defsym,platform_init=platform_%s_init" % board.get("build.variant")
    ],

    LIBS=["logicrom4g", "c", "gcc", "m", "stdc++"],

    LIBPATH=[
        join(LOGICROMSDK_DIR, "lib")
    ],

    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(gen_pac_file, "Generating $TARGET"),
            suffix=".pac"
        ),
        BinToFOTA=Builder(
            action=env.VerboseAction(" ".join([
                '$FOTAGEN',
                "--single-pac",
                "$SOURCES," + join(LOGICROMSDK_DIR, 'lib', 'rda8910', 'fota8910.xml'),
                "$TARGET"
            ]), "Generating FOTA firmware $TARGET"),
            suffix=".bin"
        )
    )
)

if "darwin" in get_systype():
    env["BUILDERS"]["BinToFOTA"] = Builder(
        action=env.VerboseAction(gen_fota_file, "Generating FOTA firmware $TARGET"),
        suffix=".bin"
    )

# uploader flag update
env.Prepend(
    UPLOAD_EXTRA_ARGS=[
        core_config["CONFIG_FDL1_IMAGE_START"],
        join(LOGICROMSDK_DIR, "lib", "rda8910", "fdl1.img"),
        core_config["CONFIG_FDL2_IMAGE_START"],
        join(LOGICROMSDK_DIR, "lib", "rda8910", "fdl2.img"),
        core_config["CONFIG_APPIMG_FLASH_ADDRESS"],
    ]
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
