# Copyright 2020 SiWi Embedded Solutions Pvt. Ltd.
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

from os.path import abspath, isdir, isfile, join, dirname, getsize
from os import remove
from shutil import copyfile
from hashlib import md5

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-siwiduino")
assert isdir(FRAMEWORK_DIR)

def fota_crc16(data:bytearray, length):
    crc = 0
    for i in range(length):
        data_byte = data[i] & 0xff
        crc = crc ^ (data_byte << 8)
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xffff

def gen_bin_file(target, source, env):
    cmd = ["$OBJCOPY"]
    (target_firm, ) = target
    (target_elf, ) = source

    temp_firm = dirname(target_firm.get_abspath()) + "/temp.bin"
    cmd.extend(["-O", "binary"])
    cmd.append(target_elf.get_abspath())
    cmd.append(temp_firm)
    env.Execute(env.VerboseAction(" ".join(cmd), " "))

    GFH_Header = bytearray([
        0x4D, 0x4D, 0x4D, 0x01, 0x40, 0x00, 0x00, 0x00,
        0x46, 0x49, 0x4C, 0x45, 0x5F, 0x49, 0x4E, 0x46,
        0x4F, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
        0x00, 0x70, 0x07, 0x00, 0x00, 0x00, 0x2E, 0x10,
        0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])
    firm_size = (getsize(temp_firm) + 64).to_bytes(4, "little")
    GFH_Header[0x20:0x23] = firm_size[0:3]

    with open(target_firm.get_abspath(), "wb") as out_firm:
        with open(temp_firm, "rb") as in_firm:
            buf = in_firm.read()
            crc32 = zlib.crc32(buf).to_bytes(4, "little")
            GFH_Header[0x3C:] = crc32
            out_firm.write(GFH_Header)
            out_firm.write(buf)
            in_firm.close()
        out_firm.close()
        remove(temp_firm)

def gen_fota_file(target, source, env):
    (fota_firm, ) = target
    (firm_bin, ) = source
    # 0x1c : Filesize
    # 0x4c : CRC16
    FOTA_Header = bytearray([
        0x53, 0x49, 0x57, 0x49, 0x5F, 0x41, 0x50, 0x50,
        0x5F, 0x46, 0x4F, 0x54, 0x41, 0x5F, 0x55, 0x50,
        0x44, 0x41, 0x54, 0x45, 0x00, 0x00, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x10, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00
    ])
    firm_size = getsize(firm_bin.get_abspath()).to_bytes(4, "little")
    FOTA_Header[0x1c:0x1f] = firm_size[0:3]
    crc = fota_crc16(FOTA_Header, len(FOTA_Header) - 4).to_bytes(4, "little")
    FOTA_Header[0x4c:0x4f] = crc[0:3]
    hash = md5()
    hash.update(FOTA_Header)
    with open(firm_bin.get_abspath(), "rb") as in_firm:
        in_firm_data = in_firm.read()
        hash.update(in_firm_data)
        with open(fota_firm.get_abspath(), "wb") as out_firm:
            out_firm.write(FOTA_Header)
            out_firm.write(in_firm_data)
            out_firm.write(hash.digest())
            out_firm.close()
        in_firm.close()

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
    ],

    CFLAGS=[
        "-std=gnu11",
		"-Wno-old-style-declaration"
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
        ("__FILENAME_MAX__", "256"),
        ("F_CPU", "$BOARD_F_CPU"),
		("ARDUINO", 10813),
		"ARDUINO_ARCH_ARM",
        ("ARDUINO_VARIANT", '\\"%s\\"' % board.get("build.variant").replace('"', "")),
        ("ARDUINO_BOARD", '\\"%s\\"' % board.get("name").replace('"', ""))
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "siwisdk", "include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "siwisdk", "include", "ril"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"))
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
        "-nodefaultlibs",
        "-u", "main",
        "-T", "linkerscript.ld",
        "-Wl,--defsym,platform_init=platform_%s_init" % board.get("build.variant")
    ],

    LIBPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "siwisdk", "lib")
    ],

    LIBS=[
        "siwisdk",
        "c",
        "gcc",
        "m",
        "stdc++"
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(gen_bin_file, "Generating $TARGET"),
            suffix=".bin"
        ),
        BinToFOTA=Builder(
            action=env.VerboseAction(gen_fota_file, "Generating FOTA firmware $TARGET"),
            suffix=".bin"
        )
    )
)

if board.get("build.newlib") == "nano":
    env.Append(
        LINKFLAGS=[
            "--specs=nano.specs",
            "-u", "_printf_float",
            "-u", "_scanf_float",
            "--specs=nosys.specs",
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

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
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
