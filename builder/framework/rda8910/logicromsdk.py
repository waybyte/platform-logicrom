# Copyright 2021 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

from os.path import getsize, isdir, isfile, join
from shutil import copyfile
import json
from zlib import crc32
from platformio.util import get_systype

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-logicromsdk")
assert isdir(FRAMEWORK_DIR)

# Load core configuration
with open(join(FRAMEWORK_DIR, "lib", "rda8910", "core_config.json")) as f:
    core_config = json.load(f)
    f.close()

# RDA Tools
if "windows" in get_systype():
    systype = "win32"
else:
    systype = "linux"

tool_path = join(FRAMEWORK_DIR, "tools", "rda8910")

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
        FRAMEWORK_DIR, "lib", "rda8910", "app_flashimg.ld"
    ),
    env.VerboseAction(
        '$CC -I"' + join(FRAMEWORK_DIR, "lib", "rda8910") + '" -P -x c -E $SOURCE -o $TARGET',
        "Generating LD script $TARGET",
    ),
)
env.Depends(join("$BUILD_DIR", "$PROGNAME" + "$PROGSUFFIX"), linker_script)
env.Replace(LDSCRIPT_PATH="linkerscript_out.ld")

# Create Project Template
main_c = join(env.subst("$PROJECT_DIR"), "src", "main.c")
main_cpp = join(env.subst("$PROJECT_DIR"), "src", "main.cpp")
if (False == isfile(main_c)) and (False == isfile(main_cpp)):
    copyfile(join(FRAMEWORK_DIR, "template", "main.c"), main_c)


def gen_img_file(target, source, env):
    cmd = ["$OBJCOPY"]
    (target_firm, ) = target
    (source_elf, ) = source

    target_img = join(env.subst("$BUILD_DIR"), env.subst("$PROGNAME") + '.img')
    
    cmd.extend(["-O", "binary"])
    cmd.append(source_elf.get_abspath())
    cmd.append(target_img)
    env.Execute(env.VerboseAction(" ".join(cmd), " "))

    # fix bin size to 0x80 boundary
    binsz = getsize(target_img)
    f_binsz = (binsz + 0x7F) & ~0x7F
    print("Binary size: %d" % binsz)
    f = open(target_img, "rb")
    f_bin = bytearray(f.read())
    f.close()
    f_bin += bytes(f_binsz - binsz)
    # Fix header size
    f_bin[4:8] = f_binsz.to_bytes(4, "little")
    # Fix checksum
    f_bin[8:0xC] = crc32(f_bin).to_bytes(4, "little")
    # write final binary
    f = open(target_img, "wb")
    f.write(f_bin)
    f.close()


def gen_pac_file(target, source, env):
    (target_firm, ) = target
    (source_elf, ) = source

    # Generate image file
    if "darwin" in get_systype():
        print("Generating Firmware Image")
        gen_img_file(target, source, env)
    else:
        env.Execute(
            env.VerboseAction("$MKIMAGE " + source_elf.get_abspath() + ' ' + join("$BUILD_DIR", env.subst('$PROGNAME') + '.img'),
            "Generating Firmware Image")
        )

    # Generate pac file
    init_fdl = [
        'cfg-init', '--pname', '"UIX8910_MODEM"', '--palias', '"$PROGNAME"',
            '--pversion', '"8910 MODULE"', '--version', '"BP_R1.0.0"',
            '--flashtype', '1',
        'cfg-host-fdl', '-a', core_config["CONFIG_FDL1_IMAGE_START"], '-s', core_config["CONFIG_FDL1_IMAGE_SIZE"],
            '-p', join(FRAMEWORK_DIR, 'lib', 'rda8910', 'fdl1.img'),
        'cfg-fdl2', '-a', core_config["CONFIG_FDL2_IMAGE_START"], '-s', core_config["CONFIG_FDL2_IMAGE_SIZE"],
            '-p', join(FRAMEWORK_DIR, 'lib', 'rda8910', 'fdl2.img'),
    ]

    pac_nvitem = [
        'cfg-nvitem', '-n', '"Calibration"', '-i', '0xFFFFFFFF', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"GSM Calibration"', '-i', '0x26d', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"LTE Calibration"', '-i', '0x26e', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"IMEI"', '-i', '0xFFFFFFFF', '--use', '1', '--replace', '0', '--continue', '0', '--backup', '1',
        'cfg-nvitem', '-n', '"BT_Config"', '-i', '0x191', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"Logicrom"', '-i', '0x280', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
        'cfg-nvitem', '-n', '"Customer"', '-i', '0x27e', '--use', '1', '--replace', '0', '--continue', '1', '--backup', '1',
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
        ("__FILENAME_MAX__", "256")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "include"),
        join(FRAMEWORK_DIR, "include", "ril")
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
        "-Wl,--defsym,platform_init=platform_%s_init" % board.get("build.variant")
    ],

    LIBS=["logicrom4g", "c", "gcc", "m"],

    LIBPATH=[
        join(FRAMEWORK_DIR, "lib")
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
                "$SOURCES," + join(FRAMEWORK_DIR, 'lib', 'rda8910', 'fota8910.xml'),
                "$TARGET"
            ]), "Generating FOTA firmware $TARGET"),
            suffix=".bin"
        )
    )
)

if "darwin" in get_systype():
    env["BUILDERS"]["BinToFOTA"] = Builder(
        action=env.VerboseAction(" ".join([
            'echo',
            '"FOTA file generation is currently not supported. Please use Linux/Windows system."'
        ]), "Generating FOTA firmware $TARGET"),
        suffix=".bin"
    )

# uploader flag update
env.Prepend(
    UPLOAD_EXTRA_ARGS=[
        core_config["CONFIG_FDL1_IMAGE_START"],
        join(FRAMEWORK_DIR, "lib", "rda8910", "fdl1.img"),
        core_config["CONFIG_FDL2_IMAGE_START"],
        join(FRAMEWORK_DIR, "lib", "rda8910", "fdl2.img"),
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
