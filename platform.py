# Copyright 2020 SiWi Embedded Solutions Pvt. Ltd.
#
# SPDX-License-Identifier: MIT
#

from platform import system
from platformio.managers.platform import PlatformBase

class SiwigsmPlatform(PlatformBase):
    def configure_default_packages(self, variables, target):
        return PlatformBase.configure_default_packages(self, variables,
                                                       target)
