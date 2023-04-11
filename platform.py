# Copyright 2023 Waybyte Solutions
#
# SPDX-License-Identifier: MIT
#

from platformio.public import PlatformBase
from platformio.util import get_systype

class LogicromPlatform(PlatformBase):
    def configure_default_packages(self, variables, target):

        # configure script based on MCU type
        board_config = self.board_config(variables.get("board"))
        mcu = variables.get("board_build.mcu",
                            board_config.get("build.mcu", "MT2503"))
        if mcu in ("ASR1601", "ASR1603"):
            self.frameworks["logicromsdk"]["script"] = "builder/framework/asr160x/logicromsdk.py"
            self.frameworks["arduino"]["script"] = "builder/framework/asr160x/arduino.py"
        elif mcu not in ("MT2503", "MT6261", "MT2625"):
            self.frameworks["logicromsdk"]["script"] = "builder/framework/%s/logicromsdk.py" % (
                mcu.lower())
            self.frameworks["arduino"]["script"] = "builder/framework/%s/arduino.py" % (
                mcu.lower())

        if mcu == "RDA8955":
            self.packages["toolchain-gccarmnoneeabi"]["optional"] = True
            self.packages["toolchain-gccmipselfrda8955"]["optional"] = False

        return PlatformBase.configure_default_packages(self, variables,
                                                       target)
