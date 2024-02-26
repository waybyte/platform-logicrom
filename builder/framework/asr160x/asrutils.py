# Copyright 2024 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

from os.path import getsize, join
from zipfile import ZipFile
from zlib import crc32
from json import load, dump


def makebin(target, source, env):
    cmd = ["$OBJCOPY"]
    cmd.extend(["-O", "binary"])
    cmd.append(source)
    cmd.append(target)
    env.Execute(env.VerboseAction(" ".join(cmd), " "))

    # fix bin size to 32 byte boundary
    binsz = getsize(target)
    f_binsz = (binsz + 0x1F) & ~0x1F
    f = open(target, "rb")
    f_bin = bytearray(f.read())
    f.close()
    f_bin += bytes(f_binsz - binsz)
    # Fix header size
    f_bin[4:8] = f_binsz.to_bytes(4, "little")
    # Fix checksum
    f_bin[8:0xC] = crc32(f_bin).to_bytes(4, "little")
    # write final binary
    f = open(target, "wb")
    f.write(f_bin)
    f.close()


def gen_fota_file(target, source, env):
    (target_bin, ) = target
    (source_elf, ) = source
    makebin(target_bin.get_abspath(), source_elf.get_abspath(), env)


def gen_release_file(target_firm, source_elf, imagepath, env):
    board = env.BoardConfig()
    mcu = board.get("build.mcu")
    flashsz = board.get("build.flashsz")
    # Generate image file
    print("Generating Firmware Binary")
    target_img = join(env.subst("$BUILD_DIR"), env.subst("$PROGNAME") + '.bin')
    makebin(target_img, source_elf.get_abspath(), env)
    target_binsz = getsize(target_img)
    print("Updating download.json")
    # Load and update download.json
    f = open(join(imagepath, "download.json"), "r")
    download = load(f)
    f.close()
    for cmd in download:
        if cmd["command"] == "require" and cmd["name"] == "product":
            cmd["value"] = "arom-tiny" if mcu == "ASR1603" else "arom|arom-tiny"
        elif cmd["command"] == "require" and cmd["name"] == "version-bootrom":
            cmd["value"] = "2020.07.30" if mcu == "ASR1603" else "2019.01.15"
        elif cmd["command"] == "progress":
            cmd["value"] = target_binsz
        elif cmd["command"] == "flash":
            cmd["weight"] = target_binsz
            cmd["image"] = env.subst("$PROGNAME") + '.bin'
    f = open(join(env.subst("$BUILD_DIR"), "download.json"), "w")
    dump(download, f, indent=4)
    f.close()
    # Update partition info, might not be needed
    print("Updating partition_" + flashsz + ".bin")
    f = open(join(imagepath, "partition_" + flashsz + ".bin"), "rb")
    part = bytearray(f.read())
    f.close()
    # Update app size
    part[0x3B8:0x3BC] = target_binsz.to_bytes(4, "little")
    # update CRC
    part[0x888:] = crc32(part[:(len(part) - 4)]).to_bytes(4, "little")
    f = open(join(env.subst("$BUILD_DIR"), "partition.bin"), "wb")
    f.write(part)
    f.close()
    # Generate zip file for flasher
    print("Creating final zip")
    firm = ZipFile(target_firm.get_abspath(), "w")
    firm.write(join(env.subst("$BUILD_DIR"), "download.json"), "download.json")
    firm.write(join(env.subst("$BUILD_DIR"), "partition.bin"), "partition.bin")
    firm.write(join(imagepath, mcu, "flasher.img"), "flasher.img")
    firm.write(join(imagepath, "flashinfo_" + flashsz + ".bin"), "flashinfo.bin")
    firm.write(join(imagepath, mcu, "preboot.img"), "preboot.img")
    firm.write(target_img, env.subst("$PROGNAME") + ".bin")

